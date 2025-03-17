import os
import shutil
import subprocess
from datetime import datetime

class RegressionDirectoryBuilder:
    """
    负责创建回归目录，处理Makefile复制，以及通过编译生成子目录
    """

    def __init__(self, base_dir=None):
        """
        初始化
        :param base_dir: 父目录路径；若为 None，则使用当前工作目录
        """
        self.base_dir = base_dir or os.getcwd()
        self.regression_dir = None

    def create_regression_directory(self):
        """
        创建回归目录，格式为 regression_YYYYMMDD
        """
        date_str = datetime.now().strftime("%Y%m%d")
        self.regression_dir = os.path.join(self.base_dir, f"regression_{date_str}")

        # 如果目录不存在，则创建
        os.makedirs(self.regression_dir, exist_ok=True)
        print(f"[INFO] Created regression directory: {self.regression_dir}")

    def copy_makefile(self):
        """
        拷贝当前目录下的 Makefile 到回归目录
        """
        source_makefile = os.path.join(self.base_dir, "Makefile")
        target_makefile = os.path.join(self.regression_dir, "Makefile")

        if not os.path.exists(source_makefile):
            raise FileNotFoundError(f"Makefile not found in current directory: {source_makefile}")

        shutil.copy(source_makefile, target_makefile)
        print(f"[INFO] Copied Makefile to regression directory: {target_makefile}")

    def compile_modes(self, modes):
        """
        使用 Makefile 编译生成模式目录及其子目录
        :param modes: 一个包含所有模式名称的列表
        """
        if not os.path.exists(self.regression_dir):
            raise RuntimeError("Regression directory does not exist. Please create it first.")

        for mode in modes:
            # 使用 make 创建每个模式的目录及子目录
            print(f"[INFO] Compiling mode: {mode} using Makefile...")
            process = subprocess.run(
                ["make", f"mode={mode}"],
                cwd=self.regression_dir,  # 指定编译目录
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            if process.returncode != 0:
                # 输出错误日志
                print(f"[ERROR] Makefile compilation failed for mode: {mode}")
                print(process.stdout.decode("utf-8"))
                continue
            print(f"[INFO] Compilation successful for mode: {mode}")