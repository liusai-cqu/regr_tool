import subprocess
import os

class CoverageManager:
    """
    覆盖率管理工具，支持覆盖率数据生成与分析
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path

    def generate_coverage_report(self, mode):
        """
        使用 make urg 生成覆盖率报告
        :param mode: 当前模式名称
        """
        self.logger.info(f"Generating coverage report for mode: {mode}")
        cmd = ["make", "urg", f"mode={mode}"]

        try:
            process = subprocess.run(cmd, cwd=self.result_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if process.returncode != 0:
                self.logger.error(f"Coverage generation failed for mode: {mode}")
                raise RuntimeError("Urg command error")
            self.logger.info(f"Coverage report successfully generated for mode: {mode}")
        except Exception as e:
            self.logger.error(f"Coverage generation error for mode: {mode}. Exception: {str(e)}")
            raise

    def generate_testplan_annotation(self, mode):
        """
        使用 make vplan 生成测试计划注解
        :param mode: 当前模式名称
        """
        self.logger.info(f"Generating testplan annotation for mode: {mode}")
        module_name = self.gconf.regr_list.BLK_NAME
        cmd = ["make", "vplan", f"mode={mode}", f"module_name={module_name}"]

        try:
            process = subprocess.run(cmd, cwd=self.result_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if process.returncode != 0:
                self.logger.error(f"Testplan generation failed for mode: {mode}")
                raise RuntimeError("Vplan command error")
            self.logger.info(f"Testplan annotation successfully generated for mode: {mode}")
        except Exception as e:
            self.logger.error(f"Testplan generation error for mode: {mode}. Exception: {str(e)}")
            raise