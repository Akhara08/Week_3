import subprocess
import tempfile
import re

class PylintLinter:
    name = "PylintLinter"

    def clean_code(self, code: str) -> str:
        # Remove ```python ... ``` or ``` ... ```
        return re.sub(r"^```(?:python)?\n([\s\S]+?)\n```$", r"\1", code.strip())

    async def run(self, code: str) -> str:
        cleaned = self.clean_code(code)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(cleaned)
            f.flush()
            try:
                result = subprocess.run(
                    ["pylint", f.name, "--disable=all", "--enable=W,C,E"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                return f"🧹 Pylint Linter Output:\n```\n{result.stdout}\n```"
            except Exception as e:
                return f"❌ Linting Error: {e}"
