import os
import json
import subprocess
import re
from coverage_parser import CoverageParser


class ReportGenerator:
    """
    汇总仿真结果、解析覆盖率并生成最终报告
    """

    def __init__(self, gconf):
        self.gconf = gconf
        self.logger = gconf.logger
        self.result_path = gconf.result_path

        # 定义排除模式和错误关键词的正则
        self.exclusion_patterns = r"NO UVM_ERROR|UVM_ERROR\s+:\s+0"  # 忽略的模式
        self.error_patterns = gconf.err_keyword  # 重点匹配的错误关键词列表（例如: UVM_ERROR|ASSERTION|FAIL|ERROR）

    def log_contains_error(self, log_path):
        """
        使用 grep 检查日志文件是否包含错误关键词
        """
        try:
            # 构造 grep 命令：先排除模式，再匹配错误
            cmd = f"grep -vE '{self.exclusion_patterns}' {log_path} | grep -E '{self.error_patterns}'"

            # 执行 grep 命令并获取结果
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # 如果返回码为 0，说明命中错误关键词
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error while processing log file {log_path}: {e}")
            return False

    def generate_final_report(self):
        """
        收集日志和仿真结果，结合覆盖率数据、编译结果和回归统计，生成最终的综合报告
        """
        final_report = {"modes": {}}  # 初始化最终报告结构

        for mode in self.gconf.mode:
            self.logger.info(f"Generating report for mode: {mode}")
            mode_report = {
                "coverage": {},  # 覆盖率数据仅包含 summary
                "results": {},  # 测试用例结果
                "statistics": {},  # 汇总统计
                "compilation": {},  # 编译结果
            }

            # 模式的日志目录和覆盖率目录
            log_dir = os.path.join(self.result_path, mode, "log")
            cov_dir = os.path.join(self.result_path, mode, "cov")

            # 解析覆盖率数据 (仅解析 summary)
            try:
                dashboard_path = os.path.join(cov_dir, "urgReport", "dashboard.txt")
                if os.path.exists(dashboard_path):
                    self.logger.info(f"Parsing coverage summary for mode: {mode}")
                    parser = CoverageParser(self.result_path, mode)
                    coverage_data = parser.parse_dashboard()
                    mode_report["coverage"] = coverage_data.get("summary", {})
                else:
                    self.logger.warning(f"Dashboard file not found for mode: {mode}")
            except Exception as e:
                self.logger.error(f"Error parsing coverage data for mode {mode}: {str(e)}")

            # 编译日志处理
            try:
                cmp_log_path = os.path.join(log_dir, "cmp.log")
                if os.path.exists(cmp_log_path):
                    self.logger.info(f"Processing compilation log for mode: {mode}")
                    # 检查编译日志是否存在错误
                    has_errors = self.log_contains_error(cmp_log_path)
                    mode_report["compilation"] = {
                        "log_file": "cmp.log",
                        "status": "fail" if has_errors else "pass",
                    }
                else:
                    self.logger.warning(f"Compilation log not found for mode: {mode}")
            except Exception as e:
                self.logger.error(f"Error processing compilation log for mode {mode}: {str(e)}")

            # 测试用例日志处理
            try:
                if os.path.exists(log_dir):
                    logs = [log for log in os.listdir(log_dir) if log.endswith(".log") and log != "cmp.log"]
                    test_case_logs = []  # 存放日志文件解析结果
                    stats_summary = {}  # 统计结果

                    for log in logs:
                        # 假设日志文件名格式为 "<用例名>_<seed>.log"
                        match = re.match(r"^(.*)_([0-9]+)\.log$", log)
                        if match:
                            test_case = match.group(1)  # 提取用例名
                            seed = match.group(2)  # 提取种子
                            log_path = os.path.join(log_dir, log)

                            # 初始化统计结果
                            if test_case not in stats_summary:
                                stats_summary[test_case] = {
                                    "total_runs": 0,
                                    "pass_count": 0,
                                    "fail_count": 0,
                                }

                            # 更新总运行次数
                            stats_summary[test_case]["total_runs"] += 1

                            # 是否包含错误
                            if self.log_contains_error(log_path):
                                stats_summary[test_case]["fail_count"] += 1
                            else:
                                stats_summary[test_case]["pass_count"] += 1

                            # 添加日志文件到结果列表
                            test_case_logs.append({"test_case": test_case, "seed": seed, "file": log})

                    # 汇总测试用例日志和统计结果
                    mode_report["results"] = {"test_cases": test_case_logs}
                    mode_report["statistics"] = stats_summary
                else:
                    self.logger.warning(f"Log directory not found for mode: {mode}")
            except Exception as e:
                self.logger.error(f"Error collecting log files for mode {mode}: {str(e)}")

            # 添加该模式的报告到最终报告
            final_report["modes"][mode] = mode_report

        # 输出最终综合报告为 JSON 文件
        report_file = os.path.join(self.result_path, "final_report.json")
        try:
            with open(report_file, "w") as f:
                json.dump(final_report, f, indent=4)
            self.logger.info(f"Final report generated at: {report_file}")
        except Exception as e:
            self.logger.error(f"Error writing final report: {str(e)}")