import subprocess
import shlex
from typing import Annotated
from pydantic import Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test tools")


# subprocess.run()
# subprocess.Popen

@mcp.tool(name="run_shell", description="Run a shell command")
def run_shell_command(command: Annotated[str, Field(description="The shell command to run", examples=["ls -la"])]) -> str:
    try:
        # 需要设置 shell=False
        # args = shlex.split(command)
        # print(args)

        args_arr = shlex.split(command)
        if "rm" in args_arr:
            raise Exception("rm command is not allowed")

        res = subprocess.run(command, shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            return res.stderr
        return res.stdout
    except Exception as e:
        return str(e)


def run_shell_command_by_popen(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = popen.communicate()
    return stdout, stderr


if __name__ == "__main__":
    # resp = run_shell_command("rm - asdf")
    # success, failed = run_shell_command_by_popen("ls -la")
    mcp.run(transport="stdio")
    # print(success)
