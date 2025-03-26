import os
import subprocess
from datetime import datetime
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

    def run_case_single(self, mode, case, run_idx, seed=None):
        """
        Execute a single run of a test case
        """
        tc = case["tc"]
        wave, ccov = case["wave"], case["ccov"]
        
        # Generate seed if not provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), "big")
        
        self.logger.info(f"Run {run_idx}/{case['run_times']} for Testcase: {tc}, Seed: {seed}")
        
        # Create log directory
        log_dir = os.path.join(self.result_path, mode, "log")
        os.makedirs(log_dir, exist_ok=True)
        
        # Generate unique log file
        log_file = os.path.join(log_dir, f"{tc}_{seed}.log")
        
        # Construct make ncrun command
        cmd = [
            "make", "ncrun",
            f"mode={mode}",
            f"tc={tc}",
            f"seed={seed}",
            f"wave={wave}",
            f"ccov={ccov}",
        ]
        
        try:
            self.logger.info(f"Starting simulation for Testcase: {tc}, Seed: {seed}, Log: {log_file}")
            process = subprocess.run(cmd, cwd=self.result_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            # Save run log to log_file
            with open(log_file, "wb") as log:
                log.write(process.stdout)
            
            if process.returncode != 0:
                self.logger.error(f"Simulation failed - Testcase: {tc}, Seed: {seed}. Check log: {log_file}")
                return False
            else:
                self.logger.info(f"Simulation passed - Testcase: {tc}, Seed: {seed}. Log: {log_file}")
                return True
        except Exception as e:
            self.logger.error(f"Simulation error - Testcase: {tc}, Seed: {seed}. Exception: {str(e)}")
            return False

    def run_case(self, mode, case):
        """
        Execute a test case with multiple runs in parallel
        """
        # Validate required keys
        required_keys = ["tc", "wave", "ccov", "run_times"]
        for key in required_keys:
            if key not in case:
                self.logger.error(f"Missing key '{key}' in case: {case}")
                return False
        
        tc = case["tc"]
        run_times = case["run_times"]
        
        self.logger.info(f"Running simulation - Mode: {mode}, Testcase: {tc}, Run Times: {run_times}")
        
        # Prepare run configurations
        run_configs = []
        for run_idx in range(1, run_times + 1):
            seed = case.get("seed", None)
            if seed is None:
                seed = int.from_bytes(os.urandom(4), "big")
            run_configs.append((run_idx, seed))
        
        # Run in parallel using thread pool
        with ThreadPoolExecutor(max_workers=self.max_tasks) as executor:
            futures = [
                executor.submit(self.run_case_single, mode, case, run_idx, seed) 
                for run_idx, seed in run_configs
            ]
            results = [future.result() for future in futures]
        
        # Check if any run failed
        all_success = all(results)
        if not all_success:
            self.logger.error(f"Some runs failed for Testcase: {tc}")
        else:
            self.logger.info(f"All runs completed successfully for Testcase: {tc}")
        
        return all_success

    def run_simulations(self):
        """
        Execute multiple test cases with resource management
        """
        case_list = self.gconf.tc_list
        self.logger.info(f"Case list: {case_list}")
        
        for mode in self.gconf.mode:
            self.logger.info(f"Starting simulations for mode: {mode}")
            
            # Create a flat list of all run configurations
            all_run_configs = []
            for case_idx, case in enumerate(case_list):
                for run_idx in range(1, case["run_times"] + 1):
                    seed = case.get("seed", None)
                    if seed is None:
                        seed = int.from_bytes(os.urandom(4), "big")
                    all_run_configs.append((case_idx, run_idx, seed))
            
            # Run all configurations in parallel with resource constraints
            results_by_case = [[] for _ in case_list]
            with ThreadPoolExecutor(max_workers=self.max_tasks) as executor:
                futures = []
                for case_idx, run_idx, seed in all_run_configs:
                    future = executor.submit(
                        self.run_case_single, 
                        mode, 
                        case_list[case_idx], 
                        run_idx, 
                        seed
                    )
                    futures.append((future, case_idx))
                
                # Collect results
                for future, case_idx in futures:
                    result = future.result()
                    results_by_case[case_idx].append(result)
            
            # Process results by case
            failed_cases = []
            for case_idx, case_results in enumerate(results_by_case):
                if not all(case_results):
                    failed_cases.append(case_list[case_idx])
                    self.logger.error(f"Case failed: {case_list[case_idx]['tc']}")
            
            self.logger.info(f"Simulation completed for mode: {mode}. Failed cases: {len(failed_cases)}")