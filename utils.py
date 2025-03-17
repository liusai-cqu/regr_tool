import subprocess

def run_shell_command(cmd, return_output=True):
    """执行系统命令，返回结果"""
    try:
        result = subprocess.run(
            cmd, shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception(f"Command failed: {cmd}\n{result.stderr.strip()}")
        return result.stdout.strip() if return_output else None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None