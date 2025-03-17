import os
import subprocess

class Compiler:
    """
    编译管理模块
    """

    def __init__(self, gconf):
        """
        :param gconf: GConf 实例
        """
        self.gconf = gconf
        self.logger = gconf.logger

    def compile_mode(self, mode):
        self.logger.info(f"Compiling mode: {mode}...")

        # 准备目录结构
        result_mode_dir = os.path.join(self.gconf.result_path, mode)
        log_dir = os.path.join(result_mode_dir, "log")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "cmp.log")

        self.logger.info(f"[DEBUG] Log path: {log_path}")

        try:
            # 调用 Makefile
            process = subprocess.run(
                ["make", "cmp", f"mode={mode}", f"ccov={self.gconf.ccov}"],
                cwd=self.gconf.result_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True  # 以文本形式解码输出
            )

            # 实时打印 Makefile 输出
            make_output = process.stdout
            print(make_output)

            # 保存日志到文件
            with open(log_path, "w") as log_file:
                log_file.write(make_output)

            # 检查错误关键字或返回码
            if process.returncode != 0 or "Error" in make_output:
                self.logger.error(f"Compilation failed for mode: {mode}. Log: {log_path}")
                raise RuntimeError(f"Compilation failed for mode: {mode}")

            self.logger.info(f"Compilation successful for mode: {mode}. Log: {log_path}")

        except Exception as e:
            self.logger.error(f"Error during compilation for mode: {mode}: {e}")
            raise