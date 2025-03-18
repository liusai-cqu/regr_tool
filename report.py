import os
import json
from coverage_parser import CoverageParser


class ReportGenerator:
    """
    汇总仿真结果、解析覆盖率并生成最终报告
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path

    def generate_final_report(self):
        """
        收集日志和仿真结果，结合覆盖率数据，生成最终的综合报告
        """
        final_report = {"modes": {}}  # 初始化最终报告结构

        for mode in self.gconf.mode:
            self.logger.info(f"Generating report for mode: {mode}")
            mode_report = {"coverage": {"summary": {}, "hierarchical": []}, "results": {}}  # 每个模式的报告结构

            # 模式的日志目录和覆盖率目录
            log_dir = os.path.join(self.result_path, mode, "log")
            cov_dir = os.path.join(self.result_path, mode, "cov")

            # 解析覆盖率数据
            try:
                dashboard_path = os.path.join(cov_dir, "urgReport", "dashboard.txt")
                if os.path.exists(dashboard_path):
                    self.logger.info(f"Parsing coverage data for mode: {mode}")
                    parser = CoverageParser(self.result_path, mode)
                    coverage_data = parser.parse_dashboard()
                    mode_report["coverage"]["summary"] = coverage_data.get("summary", {})
                    mode_report["coverage"]["hierarchical"] = coverage_data.get("hierarchical", [])
                else:
                    self.logger.warning(f"Dashboard file not found for mode: {mode}")
            except Exception as e:
                self.logger.error(f"Error parsing coverage data for mode {mode}: {str(e)}")

            # 汇总仿真案例结果
            try:
                if os.path.exists(log_dir):
                    cmp_logs = [log for log in os.listdir(log_dir) if log == "cmp.log"]
                    test_case_logs = [
                        log for log in os.listdir(log_dir) if log.startswith("Test_Case_")
                    ]
                    mode_report["results"] = {
                        "cmp": cmp_logs,
                        "test_cases": test_case_logs
                    }
                else:
                    self.logger.warning(f"Log directory not found for mode: {mode}")
            except Exception as e:
                self.logger.error(f"Error collecting log files for mode {mode}: {str(e)}")

            # 添加该模式的报告到最终报告
            final_report["modes"][mode] = mode_report

        # 输出最终综合报告为 JSON 文件
        report_file = os.path.join(self.result_path, "final_report.json")
        with open(report_file, "w") as f:
            json.dump(final_report, f, indent=4)
        self.logger.info(f"Final report generated at: {report_file}")