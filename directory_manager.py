import os
import shutil
from datetime import datetime
import logging


class DirectoryManager:
    """
    管理回归目录的创建与初始化。
    """

    def __init__(self, base_dir, logger=None):
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

        date_str = datetime.now().strftime("%Y%m%d")  # 获取当前日期 YYYYMMDD 格式
        self.regression_dir = os.path.join(self.base_dir, f"regression_{date_str}")

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

        self.copy_file("./Makefile", "Makefile")
        self.copy_file("./mock_vcs.sh", "mock_vcs.sh")
        self.copy_file("./mock_simv.sh", "mock_simv.sh")

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