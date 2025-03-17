import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

class SimulationManager:
    """
    仿真任务管理器，使用 make ncrun 提交仿真测试用例
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path
        self.max_tasks = 20  # 最大并行任务数

    def run_case(self, mode, case):
        """
        执行单个测试用例
        """
        # 校验 case 是否包含必须的键
        required_keys = ["tc", "seed", "wave", "ccov"]
        for key in required_keys:
            if key not in case:
                self.logger.error(f"Missing key '{key}' in case: {case}")
                return False

        # 提取参数
        tc, seed, wave, ccov = case["tc"], case["seed"], case["wave"], case["ccov"]
        self.logger.info(f"Running simulation - Mode: {mode}, Testcase: {tc}, Seed: {seed}")

        log_file = os.path.join(self.result_path, mode, "log", f"{tc}_{seed}.log")

        # 构造 make ncrun 命令
        cmd = [
            "make", "ncrun",
            f"mode={mode}",
            f"tc={tc}",
            f"seed={seed}",
            f"wave={wave}",
            f"ccov={ccov}",
        ]

        try:
            process = subprocess.run(cmd, cwd=self.result_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if process.returncode != 0:
                self.logger.error(f"Simulation failed - Testcase: {tc}, Seed: {seed}. Check log: {log_file}")
                return False
            self.logger.info(f"Simulation passed - Testcase: {tc}, Seed: {seed}. Log: {log_file}")
            return True
        except Exception as e:
            self.logger.error(f"Simulation error - Testcase: {tc}, Seed: {seed}. Exception: {str(e)}")
            return False

    def run_simulations(self):
        """
        执行多个测试用例，支持多线程并行运行
        """
        case_list = self.gconf.tc_list
        self.logger.info(f"Case list: {case_list}")  # 输出测试用例列表

        for mode in self.gconf.mode:
            self.logger.info(f"Starting simulations for mode: {mode}")
            with ThreadPoolExecutor(max_workers=self.max_tasks) as executor:
                results = executor.map(lambda case: self.run_case(mode, case), case_list)

            failed_cases = [case for case, result in zip(case_list, results) if not result]
            self.logger.info(f"Simulation completed for mode: {mode}. Failed cases: {len(failed_cases)}")