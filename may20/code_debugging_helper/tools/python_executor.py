import asyncio
import contextlib
import io
import re

class PythonExecutor:
    name = "PythonExecutor"

    def clean_code(self, code: str) -> str:
        # Remove ```python ... ``` or ``` ... ```
        return re.sub(r"^```(?:python)?\n([\s\S]+?)\n```$", r"\1", code.strip())

    async def run(self, code: str) -> str:
        try:
            cleaned = self.clean_code(code)
            loop = asyncio.get_running_loop()
            output = await loop.run_in_executor(None, self._execute_code, cleaned)
            return f"✅ Execution Output:\n```\n{output}\n```"
        except Exception as e:
            return f"❌ Runtime Error: {e}"

    def _execute_code(self, code):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            exec(code, {})
        return f.getvalue()
