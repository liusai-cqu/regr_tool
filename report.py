import os
import json

class ReportGenerator:
    """
    汇总仿真结果、覆盖率生成最终报告
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path

    def generate_final_report(self):
        """
        收集日志和结果，生成最终报告
        """
        final_report = {"modes": {}}

        for mode in self.gconf.mode:
            mode_report = {"coverage": {}, "results": []}
            log_dir = os.path.join(self.result_path, mode, "log")
            cov_dir = os.path.join(self.result_path, mode, "cov")

            # 收集覆盖率数据
            dashboard_path = os.path.join(cov_dir, "urgReport", "dashboard.txt")
            if os.path.exists(dashboard_path):
                with open(dashboard_path, "r") as dashboard_file:
                    mode_report["coverage"] = dashboard_file.read()

            # 汇总仿真案例结果
            case_results = [
                log for log in os.listdir(log_dir) if log.endswith(".log")
            ]
            mode_report["results"] = case_results

            final_report["modes"][mode] = mode_report

        report_file = os.path.join(self.result_path, "final_report.json")
        with open(report_file, "w") as f:
            json.dump(final_report, f, indent=4)
        self.logger.info(f"Final report generated at: {report_file}")