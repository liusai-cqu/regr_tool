import importlib.util
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
            # 配置文件路径：运行目录的上一级目录的 cfg 文件夹
            script_working_dir = os.getcwd()  # 当前工作目录
            cfg_dir = os.path.join(script_working_dir, "../cfg")
            regress_file_path = os.path.join(cfg_dir, "regress_list.py")

            self.logger.info(f"Looking for configuration file at: {regress_file_path}")

            if not os.path.exists(regress_file_path):
                raise FileNotFoundError(f"regress_list.py not found in {cfg_dir}!")

            # 动态加载模块
            spec = importlib.util.spec_from_file_location("regress_list", regress_file_path)
            regress_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(regress_module)

            # 检查是否存在指定类
            if not hasattr(regress_module, class_name):
                raise AttributeError(f"Class {class_name} not found in regress_list.py")
            regress_class = getattr(regress_module, class_name)

            self.logger.info(f"Configuration class {class_name} loaded successfully.")
            return regress_class

        except Exception as e:
            self.logger.error(f"Failed to load configuration class: {e}")
            raise