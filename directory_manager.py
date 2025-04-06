import os
import shutil
from datetime import datetime
import logging


class DirectoryManager:
    """
    管理回归目录的创建与初始化。
    """

    def __init__(self, base_dir, name, logger=None):
        """
        初始化回归目录管理器
        :param base_dir: 基础目录路径（字符串）
        :param logger: 日志记录器（可选）
        """
        if not isinstance(base_dir, str):
            raise TypeError("[ERROR] base_dir must be a string representing the path!")

        self.base_dir = base_dir.rstrip("/")  # 移除路径末尾的斜杠
        self.regression_dir = None  # 回归目录路径
        self.logger = logger if logger else self._default_logger()
        self.name = name  # 回归任务名称

    @staticmethod
    def _default_logger():
        """
        默认日志记录器
        """
        logger = logging.getLogger("DirectoryManager")
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    def create_regression_directory(self):
        """
        创建回归目录，格式为 regression_YYYYMMDD。
        """
        if self.regression_dir:
            # 如果回归目录已经存在，防止重复调用
            self.logger.warning("Regression directory is already initialized.")
            return

        # Use the current working directory as the base for finding the parent
        current_dir = os.getcwd()  # Get the current working directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) # Calculate parent from current directory
        self.regression_dir = os.path.join(parent_dir, self.name)
        # 生成回归目录名称
        # 创建目录
        os.makedirs(self.regression_dir, exist_ok=True)
        self.logger.info(f"Created regression directory: {self.regression_dir}")

    def copy_file(self, source_path, dest_name):
        """
        辅助方法，复制文件并记录日志。
        :param source_path: 源文件路径
        :param dest_name: 在回归目录中的目标文件名
        """
        if not self.regression_dir:
            raise ValueError("Regression directory is not initialized. Call `create_regression_directory` first!")

        target_path = os.path.join(self.regression_dir, dest_name)
        if not os.path.exists(source_path):
            self.logger.error(f"Source file not found: {source_path}")
            raise FileNotFoundError(f"Source file not found: {source_path}")

        shutil.copy(source_path, target_path)
        self.logger.info(f"Copied {source_path} to {target_path}")

    def copy_makefile(self):
        """
        将 Makefile 和相关脚本复制到回归目录
        """
        # 确保回归目录已经被初始化
        if not self.regression_dir:
            raise ValueError("Regression directory is not initialized. Call `create_regression_directory` first!")

        # Get the directory of the current script (m_regress.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        makefile_source = os.path.join(script_dir, "Makefile") # Construct the Makefile source path

        self.copy_file(makefile_source, "Makefile") # Copy from the correct source path

    def create_mode_directories(self, modes):
        """
        创建模式目录及其子文件夹。
        :param modes: 模式列表，例如 ["axi3", "axi4"]
        """
        if not self.regression_dir:
            raise ValueError("Regression directory is not initialized. Call `create_regression_directory` first!")

        for mode in modes:
            mode_path = os.path.join(self.regression_dir, mode)
            os.makedirs(mode_path, exist_ok=True)  # 为每个模式创建目录
            self.logger.info(f"Created mode directory: {mode_path}")