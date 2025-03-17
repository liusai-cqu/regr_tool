import os
import subprocess
from datetime import datetime


class CoverageManager:
    """
    覆盖率管理工具，支持覆盖率数据生成与分析
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path

    def _run_command(self, cmd, mode, task_name):
        """
        通用命令运行工具
        :param cmd: 命令列表
        :param mode: 当前模式
        :param task_name: 任务名称，用于日志记录
        :return: None
        """
        self.logger.info(f"Starting {task_name} for mode: {mode} with command: {' '.join(cmd)}")
        try:
            process = subprocess.run(
                cmd,
                cwd=self.result_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # 确保输出为文本格式
            )
            if process.returncode != 0:
                self.logger.error(f"{task_name} failed for mode: {mode}")
                self.logger.error(f"Command output: {process.stdout}")
                self.logger.error(f"Command error: {process.stderr}")
                raise RuntimeError(f"{task_name} command error for mode: {mode}. Returned {process.returncode}")
            self.logger.info(f"{task_name} successfully completed for mode: {mode}")
        except Exception as e:
            self.logger.error(f"{task_name} error for mode: {mode}. Exception: {str(e)}")
            raise

    def generate_coverage_report(self, mode):
        """
        使用 make urg 生成覆盖率报告
        :param mode: 当前模式名称
        """
        task_name = "Coverage Generation"
        cmd = ["make", "urg", f"mode={mode}"]

        # 执行命令并处理
        try:
            self._run_command(cmd, mode, task_name)

            # 检查覆盖率报告目录是否生成
            cov_dir = os.path.join(self.result_path, mode, "cov")
            if not os.path.exists(cov_dir):
                self.logger.error(f"Coverage directory not found: {cov_dir}")
                raise FileNotFoundError(f"Coverage directory not found for mode: {mode}")

        except Exception as e:
            self.logger.error(f"Failed to generate coverage report for mode: {mode}. Error: {str(e)}")
            return False

        return True

    def generate_testplan_annotation(self, mode):
        """
        使用 make vplan 生成测试计划注解
        :param mode: 当前模式名称
        """
        task_name = "Testplan Annotation Generation"
        module_name = self.gconf.regr_list.BLK_NAME  # 从配置类获取模块名称
        cmd = ["make", "vplan", f"mode={mode}", f"module_name={module_name}"]

        # 执行命令并处理
        try:
            self._run_command(cmd, mode, task_name)

            # 检查测试计划注解目录是否生成
            vplan_dir = os.path.join(self.result_path, mode, "vplan")
            if not os.path.exists(vplan_dir):
                self.logger.error(f"Testplan annotation directory not found: {vplan_dir}")
                raise FileNotFoundError(f"Testplan annotation directory not found for mode: {mode}")

        except Exception as e:
            self.logger.error(f"Failed to generate testplan annotation for mode: {mode}. Error: {str(e)}")
            return False

        return True