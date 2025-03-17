class TaskManager:
    def __init__(self, cfg, logger):
        self.cfg = cfg  # 全局配置
        self.logger = logger  # 日志模块
        self.tasks = []  # 存储所有任务

    def add_task(self, tc, seed, sim_opts, timeout, mode):
        """
        增加单个测试任务
        """
        task = {
            "name": tc,
            "seed": seed,
            "sim_opts": sim_opts,
            "timeout": timeout,
            "mode": mode,
        }
        self.tasks.append(task)

    def execute_tasks(self):
        """
        执行所有测试任务，支持日志记录
        """
        self.logger.info(f"Total tasks to execute: {len(self.tasks)}")

        for task in self.tasks:
            try:
                # 记录任务开始的日志
                self.logger.info("Starting task", **task)

                # 模拟执行任务
                self.run_task(task)

                # 记录任务完成的日志
                self.logger.info("Task completed successfully", **task)

            except Exception as e:
                # 记录任务失败的错误日志
                self.logger.error(f"Task execution failed: {str(e)}", **task)

    def run_task(self, task):
        """
        执行单个任务，模拟任务执行逻辑
        """
        self.logger.debug(f"Running task: {task['name']} with seed {task['seed']}")
        # 模拟任务执行
        import time
        time.sleep(2)  # 假设每个任务花费 2 秒完成

        # 模拟异常
        if task['seed'] % 2 == 0:  # 假设 seed 为偶数时会失败
            raise ValueError("Simulated task failure")