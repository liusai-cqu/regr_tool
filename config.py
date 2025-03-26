import os
import json
import time
from logger import Logger
from regress_loader import RegressLoader


class GConf:
    """
    全局配置管理类，用于解析命令行参数、动态加载用户配置，并管理工具的全局状态
    """

    def __init__(self, args):
        """
        初始化 GConf 配置
        :param args: 从命令行解析的参数
        """
        # 初始化日志
        self.logger = Logger(log_dir="./logs", log_level=args.log_level)

        # 解析命令行参数
        self.name = args.name or f"regression_{time.strftime('%Y%m%d%H%M%S')}"  # 如果未指定名称，则按当前日期命名
        self.mode = args.mode
        self.parallel = args.parallel or 20
        self.skip_cmp = args.skip_cmp
        self.skip_sim = args.skip_sim
        self.skip_cov_gen = args.skip_cov_gen
        self.skip_cov_rpt = args.skip_cov_rpt
        self.ccov = args.ccov
        self.disable_cov = args.disable_cov
        self.random_seed = args.random_seed

        # 动态加载用户配置类（如 regress_cfg）
        self.logger.info("Loading regression configuration from regress_list.py...")
        loader = RegressLoader(self.logger)
        config_class = loader.load_regress_class("regress_cfg")

        # 从配置类中动态获取 ERR_KEYWORD
        self.err_keyword = getattr(config_class, "ERR_KEYWORD", "Failed|Error|FAILED|ERROR")
        self.logger.info(f"Loaded error keywords for log parsing: {self.err_keyword}")

        # 配置类加载的参数
        if args.mode:
            self.mode = args.mode  # 使用命令行模式列表
        else:
            # 从 TC_LIST 中提取 MODE 字段
            self.mode = self._extract_modes_from_testcases(config_class)

        # 检测 mode 是否为空
        if not self.mode:
            raise ValueError("[ERROR] Mode list is empty. Check '--mode' or TC_LIST configuration!")

        # 调试日志
        self.logger.info(f"[DEBUG] Final mode list: {self.mode}")

        # 加载测试用例并规范化键名为小写
        testcases = self._load_testcases(args.testcases, config_class)
        self.tc_list = self._normalize_case_keys(testcases)

        # 从配置类中动态获取其他参数
        self.blk_name = getattr(config_class, "BLK_NAME", "default_block")  # 测试块名称
        self.common_timeout_lmt = getattr(config_class, "COMMON_TIMEOUT_LMT", 15)  # 超时限制
        self.wave = getattr(config_class, "WAVE", "off")  # 波形配置
        self.ccov = getattr(config_class, "CCOV", "on")  # 覆盖率配置
        
        # 配置覆盖率功能
        if self.disable_cov:
            self.logger.warning("Coverage functionality has been disabled by the user!")
            self.ccov = "off"

        # 设置回归任务主目录路径
        self.base_dir = "../"
        self.result_path = os.path.join(self.base_dir, self.name)  # 回归任务目录

        # 初始化目录结构
        self._prepare_directories()

    def _normalize_case_keys(self, testcases):
        """
        将测试用例中的所有键名转换为小写，并补充默认值
        """
        normalized_testcases = []

        default_fields = {
            "wave": "off",  # 默认关闭波形
            "ccov": "on"    # 默认开启覆盖率
        }
        for case in testcases:
            if isinstance(case, dict):
                # 将键转换为小写并补充默认值
                normalized_case = {key.lower(): value for key, value in case.items()}
                for key, default in default_fields.items():
                    normalized_case.setdefault(key, default)  # 插入默认值
                normalized_testcases.append(normalized_case)
            else:
                self.logger.warning(f"[WARNING] Skipping invalid testcase: {case}")
        self.logger.info(f"[INFO] Normalized {len(normalized_testcases)} testcases with defaults.")
        return normalized_testcases

    def _extract_modes_from_testcases(self, config_class):
        """
        从 TC_LIST 提取唯一模式列表
        """
        tc_list = getattr(config_class, "TC_LIST", [])
        modes = set()

        if not isinstance(tc_list, list):
            self.logger.error(f"[ERROR] TC_LIST is not a list: {tc_list}")
            raise ValueError("TC_LIST must be a list of testcases.")

        for tc in tc_list:
            if not isinstance(tc, dict):  # 每个用例必须是字典
                self.logger.warning(f"[WARNING] Testcase is not a dict: {tc}")
                continue  # 跳过格式错误的用例

            mode_value = tc.get("MODE", None)

            if isinstance(mode_value, list):
                modes.update(mode_value)  # 如果 MODE 是列表，解包并去重
            elif isinstance(mode_value, str):
                modes.add(mode_value)  # 如果 MODE 是字符串，直接添加
            elif mode_value is None:
                self.logger.warning(f"[WARNING] MODE is missing for testcase: {tc}")
            else:
                self.logger.warning(f"[WARNING] Unexpected MODE type in testcase: {tc}")

        self.logger.info(f"[INFO] Extracted modes from TC_LIST: {modes}")
        return list(modes)

    def _load_testcases(self, testcase_file, config_class):
        """
        加载测试用例列表
        :param testcase_file: 用户指定的测试用例文件路径（JSON 格式）
        :param config_class: 动态加载的配置类
        :return: 测试用例列表
        """
        if testcase_file:
            try:
                self.logger.info(f"Loading testcases from file: {testcase_file}")
                with open(testcase_file, "r") as f:
                    testcases = json.load(f)
                self.logger.info(f"Successfully loaded {len(testcases)} testcases from file.")
                return testcases
            except Exception as e:
                self.logger.error(f"Failed to load testcases from file: {testcase_file}. Error: {e}")
                raise
        # 如果未提供文件，使用配置类中的默认 TC_LIST
        return getattr(config_class, "TC_LIST", [])

    def _prepare_directories(self):
        """
        创建回归任务的主目录及必要的子目录结构
        """
        try:
            # 创建主结果目录
            os.makedirs(self.result_path, exist_ok=True)

            # 创建日志目录
            # log_dir = os.path.join(self.result_path, "logs")
            # os.makedirs(log_dir, exist_ok=True)

            self.logger.info(f"Result directory initialized: {self.result_path}")
            # self.logger.info(f"Logs directory initialized: {log_dir}")

        except Exception as e:
            self.logger.error(f"Failed to initialize directories: {e}")
            raise