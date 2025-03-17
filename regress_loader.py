import importlib
import os

class RegressLoader:
    """
    动态加载 regress_list.py 并解析用户定义的配置类
    """

    def __init__(self, logger):
        self.logger = logger

    def load_regress_class(self, class_name):
        """
        动态加载配置类
        :param class_name: 配置类名称（默认加载 regress_cfg）
        :return: 用户定义的配置类
        """
        try:
            self.logger.info(f"Loading configuration class: {class_name}")
            if not os.path.exists("regress_list.py"):
                raise FileNotFoundError("regress_list.py not found in the current directory!")

            # 动态导入模块
            regress_module = importlib.import_module("regress_list")

            # 获取指定类
            if not hasattr(regress_module, class_name):
                raise AttributeError(f"Class {class_name} not found in regress_list.py")
            regress_class = getattr(regress_module, class_name)

            self.logger.info(f"Configuration class {class_name} loaded successfully.")
            return regress_class
        except Exception as e:
            self.logger.error(f"Failed to load configuration class: {e}")
            raise