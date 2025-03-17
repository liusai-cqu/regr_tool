import logging
import os

class Logger:
    """
    全局日志管理类，用于统一控制日志记录功能
    """
    def __init__(self, log_dir=None, log_file="regression_tool.log", log_level=logging.INFO):
        """
        初始化日志器
        :param log_dir: 日志存储目录
        :param log_file: 默认日志文件名
        :param log_level: 日志等级
        """
        self.log_dir = log_dir or os.getcwd()
        self.log_file = os.path.join(self.log_dir, log_file)

        # 创建日志目录（如果不存在）
        os.makedirs(self.log_dir, exist_ok=True)

        # 配置日志基础属性
        self.logger = logging.getLogger("RegressionTool")
        self.logger.setLevel(log_level)

        # 创建日志格式
        log_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # StreamHandler 负责控制台日志输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

        # FileHandler 负责文件日志输出
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """记录 INFO 日志"""
        self.logger.info(message)

    def debug(self, message):
        """记录 DEBUG 日志"""
        self.logger.debug(message)

    def warning(self, message):
        """记录 WARNING 日志"""
        self.logger.warning(message)

    def error(self, message):
        """记录 ERROR 日志"""
        self.logger.error(message)