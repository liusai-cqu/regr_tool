from collections import defaultdict

class RegressionResult:
    """回归测试结果处理模块"""
    def __init__(self):
        self.total_count = defaultdict(int)
        self.pass_count = defaultdict(int)
        self.fail_count = defaultdict(int)
        self.details = []

    def record_result(self, name, status, log_path):
        """记录单个测试结果"""
        self.total_count[name] += 1
        if status == "PASSED":
            self.pass_count[name] += 1
        else:
            self.fail_count[name] += 1
        self.details.append({"name": name, "status": status, "log_path": log_path})

    def show_summary(self):
        """输出回归测试统计结果"""
        print("Summary Report:")
        for name in self.total_count.keys():
            total = self.total_count[name]
            passed = self.pass_count[name]
            failed = self.fail_count[name]
            print(f"Test: {name} | Total: {total} | Passed: {passed} | Failed: {failed}")