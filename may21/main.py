import os
import pandas as pd
import matplotlib.pyplot as plt
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=GOOGLE_API_KEY)

class Agent:
    async def run(self, context):
        raise NotImplementedError

class DataFetcher(Agent):
    async def run(self, context):
        path_or_url = context.get("data_source")
        print(f"[DataFetcher] Fetching data from: {path_or_url}")

        try:
            if path_or_url.startswith("http"):
                df = pd.read_csv(path_or_url)
            else:
                df = pd.read_csv(path_or_url.strip('"'))  # Handle path with quotes

            context["dataframe"] = df
            print("[DataFetcher] Data fetched successfully.")
        except Exception as e:
            print(f"[DataFetcher] Failed to read data: {e}")
            context["error"] = str(e)
        return context

class Analyst(Agent):
    async def run(self, context):
        if "error" in context:
            print("[Analyst] Skipping analysis due to previous error.")
            return context

        df = context.get("dataframe")
        prompt = context.get("analysis_prompt") or "Generate suitable charts for this dataset."

        # Ask LLM for multiple chart types (comma separated)
        llm_input = (
            f"You are a data analyst. Based on this prompt: '{prompt}', "
            f"consider the sample data:\n{df.head(5).to_string()}\n\n"
            f"Column data types:\n{df.dtypes.to_string()}\n\n"
            "Suggest up to 3 chart types to visualize this data from: histogram, bar, line, pie, scatter. "
            "Respond only with chart types separated by commas."
        )

        print(f"[Analyst] Prompt to LLM:\n{llm_input}\n")
        response = await gemini.ainvoke([HumanMessage(content=llm_input)])
        chart_types = [ct.strip().lower() for ct in response.content.split(",")]

        valid_chart_types = {"histogram", "bar", "line", "pie", "scatter"}
        selected_charts = [ct for ct in chart_types if ct in valid_chart_types]
        if not selected_charts:
            print("[Analyst] No valid charts suggested, defaulting to histogram.")
            selected_charts = ["histogram"]

        # Save paths of generated charts
        plot_paths = []

        # For line and scatter, ask user which columns to use for X/Y if multiple numeric columns
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        for i, chart_type in enumerate(selected_charts, 1):
            plt.figure(figsize=(10, 6))
            try:
                if chart_type == "histogram":
                    if numeric_cols:
                        df[numeric_cols[0]].hist(bins=20)
                        plt.title(f"Histogram of {numeric_cols[0]}")
                        plt.xlabel(numeric_cols[0])
                        plt.ylabel("Frequency")
                    else:
                        raise ValueError("No numeric column for histogram.")

                elif chart_type == "bar":
                    if cat_cols:
                        df[cat_cols[0]].value_counts().plot(kind='bar')
                        plt.title(f"Bar Chart of {cat_cols[0]}")
                        plt.xlabel(cat_cols[0])
                        plt.ylabel("Count")
                    else:
                        raise ValueError("No categorical column for bar chart.")

                elif chart_type == "line":
                    if len(numeric_cols) < 2:
                        raise ValueError("Not enough numeric columns for line chart.")
                    print(f"[Analyst] Available numeric columns for line chart: {numeric_cols}")
                    x_col = input("Choose X-axis column for line chart: ").strip()
                    y_col = input("Choose Y-axis column for line chart: ").strip()
                    if x_col not in numeric_cols or y_col not in numeric_cols:
                        raise ValueError("Invalid column selection for line chart.")
                    df.plot(x=x_col, y=y_col, kind='line')
                    plt.title(f"Line Chart of {y_col} vs {x_col}")
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)

                elif chart_type == "pie":
                    if cat_cols:
                        df[cat_cols[0]].value_counts().plot(kind='pie', autopct='%1.1f%%')
                        plt.title(f"Pie Chart of {cat_cols[0]}")
                    else:
                        raise ValueError("No categorical column for pie chart.")

                elif chart_type == "scatter":
                    if len(numeric_cols) < 2:
                        raise ValueError("Not enough numeric columns for scatter plot.")
                    print(f"[Analyst] Available numeric columns for scatter plot: {numeric_cols}")
                    x_col = input("Choose X-axis column for scatter plot: ").strip()
                    y_col = input("Choose Y-axis column for scatter plot: ").strip()
                    if x_col not in numeric_cols or y_col not in numeric_cols:
                        raise ValueError("Invalid column selection for scatter plot.")
                    df.plot.scatter(x=x_col, y=y_col)
                    plt.title(f"Scatter Plot of {y_col} vs {x_col}")
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)

            except Exception as e:
                print(f"[Analyst] Error creating {chart_type} chart: {e}")
                # fallback: plot first numeric column histogram
                plt.clf()
                if numeric_cols:
                    df[numeric_cols[0]].hist(bins=20)
                    plt.title(f"Fallback Histogram of {numeric_cols[0]}")
                    plt.xlabel(numeric_cols[0])
                    plt.ylabel("Frequency")
                else:
                    plt.text(0.5, 0.5, "No data to plot", ha='center', va='center')

            plt.tight_layout()
            plot_path = f"output_plot_{i}_{chart_type}.png"
            plt.savefig(plot_path)
            plt.close()
            plot_paths.append(plot_path)
            print(f"[Analyst] Saved {chart_type} chart as {plot_path}")

        context["plot_paths"] = plot_paths
        return context

class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents

    async def run(self, context):
        for agent in self.agents:
            context = await agent.run(context)
        return context

async def main():
    print("Please enter the CSV file path or URL:")
    file_path = input().strip()

    print("Enter analysis prompt (or press enter for default):")
    analysis_prompt = input().strip()

    context = {
        "data_source": file_path,
        "analysis_prompt": analysis_prompt,
    }

    agents = [DataFetcher(), Analyst()]
    group_chat = RoundRobinGroupChat(agents)
    context = await group_chat.run(context)

    if "plot_paths" in context:
        print("[Main] Generated plots:")
        for path in context["plot_paths"]:
            print(" -", path)
    else:
        print("[Main] Failed to generate any plots.")

if __name__ == "__main__":
    asyncio.run(main())
