import os
import re

class CoverageParser:
    """
    负责解析覆盖率报告的工具类
    """
    def __init__(self, regr_dir, mode):
        self.regr_dir = regr_dir
        self.mode = mode
        self.dashboard_path = os.path.join(regr_dir, mode, "cov", "urgReport", "dashboard.txt")
        self.coverage_data = {
            "summary": {},   # Total Coverage Summary 数据
            "details": {}    # Hierarchical coverage data 具体数据
        }

    def parse_dashboard(self):
        """
        解析 dashboard.txt 文件，提取覆盖率数据
        """
        if not os.path.exists(self.dashboard_path):
            raise FileNotFoundError(f"Dashboard file not found at {self.dashboard_path}")

        section = None  # 当前处理的章节状态
        with open(self.dashboard_path, "r") as file:
            for line in file:
                # 检测 Total Coverage Summary 起始点
                if re.match(r"Total Coverage Summary", line):
                    section = "summary"
                    continue

                # 检测 Hierarchical coverage data 起始点
                if re.match(r"Hierarchical coverage data", line):
                    section = "details"
                    continue

                # 处理数据内容
                if section == "summary":
                    self._parse_summary(line)
                elif section == "details":
                    self._parse_details(line)

        return self.coverage_data

    def _parse_summary(self, line):
        """
        解析 Total Coverage Summary 部分
        """
        # 匹配字段和数值，例如 "ASSERT_C : 92" 或 "LINE : 100%"
        match = re.match(r"(\w+)\s+:\s+([\d.]+)%?", line)
        if match:
            key, value = match.groups()
            self.coverage_data["summary"][key.upper()] = float(value)

    def _parse_details(self, line):
        """
        解析 Hierarchical coverage data 部分
        """
        # 匹配覆盖率详细字段，例如 "COND : 78.3%" 或 "GROUP : 95%"
        match = re.match(r"(\w+)\s+:\s+([\d.]+)%?", line)
        if match:
            key, value = match.groups()
            self.coverage_data["details"][key.upper()] = float(value)


def merge_coverage_data(modes_coverage):
    """
    汇总多个 mode 的覆盖率结果
    :param modes_coverage: List[Dict] 各 mode 的覆盖率数据
    :return: Dict 汇总后的覆盖率数据
    """
    merged_data = {"summary": {}, "details": {}}
    summary_fields = set()
    detail_fields = set()

    # 获取所有模式下的覆盖率字段
    for coverage in modes_coverage:
        summary_fields.update(coverage["summary"].keys())
        detail_fields.update(coverage["details"].keys())

    # 汇总每个字段的值
    for field in summary_fields:
        merged_data["summary"][field] = round(
            sum(coverage["summary"].get(field, 0) for coverage in modes_coverage) / len(modes_coverage),
            2  # 精确到小数点后两位
        )

    for field in detail_fields:
        merged_data["details"][field] = round(
            sum(coverage["details"].get(field, 0) for coverage in modes_coverage) / len(modes_coverage),
            2
        )

    return merged_data


def display_coverage_summary(coverage_result):
    """
    格式化汇总后的覆盖率数据以便输出
    """
    print("============== Coverage Summary ==============")
    print("Total Coverage Summary:")
    for key, value in coverage_result["summary"].items():
        print(f"  {key}: {value}%")

    print("\nHierarchical Coverage Data:")
    for key, value in coverage_result["details"].items():
        print(f"  {key}: {value}%")
    print("==============================================")