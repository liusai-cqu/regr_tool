import os
import re


class CoverageParser:
    """
    覆盖率报告解析工具类
    """

    def __init__(self, regr_dir, mode):
        self.regr_dir = regr_dir
        self.mode = mode
        self.dashboard_path = os.path.join(regr_dir, mode, "cov", "urgReport", "dashboard.txt")
        self.coverage_data = {
            "summary": {},   # Total Coverage Summary 数据
            "hierarchical": []  # Hierarchical coverage data 数据
        }

    def parse_dashboard(self):
        """
        解析 dashboard.txt 文件，提取覆盖率数据
        """
        if not os.path.exists(self.dashboard_path):
            raise FileNotFoundError(f"Dashboard file not found at {self.dashboard_path}")

        section = None   # 当前处理的章节状态
        with open(self.dashboard_path, "r") as file:
            for line in file:
                line = line.strip()  # 去除空白字符

                # 检测 Total Coverage Summary 起始点
                if re.match(r"^Total Coverage Summary", line):
                    section = "summary"
                    continue

                # 检测 Hierarchical coverage data 起始点
                if re.match(r"^Hierarchical coverage data", line):
                    section = "hierarchical"
                    continue

                # 处理数据内容
                if section == "summary":
                    self._parse_summary(line)
                elif section == "hierarchical":
                    self._parse_hierarchical(line)

        return self.coverage_data

    def _parse_summary(self, line):
        """
        解析 Total Coverage Summary 部分
        示例行:
        SCORE   LINE            COND        TOGGLE          ASSERT       
        80.23  100.00 200/200  --     0/0   97.84 317/324   42.86 18/42
        """
        match = re.match(
            r"^\s*(\d+\.\d+)\s+"            # SCORE: 80.23
            r"(\d+\.\d+)\s+"                # LINE: 100.00
            r"([\d\-/]+)\s+"                # LINE: 200/200 (覆盖/总数)
            r"(--|\d+\.\d+)\s+"             # COND: -- 或 浮点数
            r"([\d\-/]+)\s+"                # COND Details: 0/0
            r"(\d+\.\d+)\s+"                # TOGGLE: 97.84
            r"([\d\-/]+)\s+"                # TOGGLE Details: 317/324
            r"(\d+\.\d+)\s+"                # ASSERT: 42.86
            r"([\d\-/]+)\s*$",              # ASSERT Details: 18/42
            line
        )
        if match:
            groups = match.groups()
            self.coverage_data["summary"] = {
                "SCORE": float(groups[0]),     # 总分
                "LINE": float(groups[1]),      # 行覆盖率
                "TOGGLE": float(groups[5]),    # 切换覆盖率
                "ASSERT": float(groups[7])     # 断言覆盖率
            }

    def _parse_hierarchical(self, line):
        """
        解析 Hierarchical coverage data 部分
        line 示例: "80.23  100.00 200/200  --     --       97.84 317/324   42.86 18/42  tb_jk_ff"
        """
        match = re.match(
            r"^\s*(\d+\.\d+)\s+"            # SCORE
            r"(\d+\.\d+)\s+"                # LINE
            r"([\d\-]+/[\d\-]+)\s+"         # COND
            r"(--|[\d\-]+/[\d\-]+)\s+"      # OPTIONAL COND
            r"(--|[\d\-]+/[\d\-]+)\s+"      # TOGGLE
            r"(\d+\.\d+)\s+"                # TOGGLE %
            r"([\d\-]+/[\d\-]+)\s+"         # ASSERT
            r"(\d+\.\d+)\s+"                # ASSERT %
            r"(\d+/[\d\-]+)\s+"             # Final Details
            r"(\S+)",                       # NAME (最后一个字段)
            line
        )
        if match:
            groups = match.groups()
            self.coverage_data["hierarchical"].append({
                "SCORE": float(groups[0]),
                "LINE": float(groups[1]),
                "TOGGLE": float(groups[5]),
                "ASSERT": float(groups[7]),
                "NAME": groups[9]
            })


def merge_coverage_data(modes_coverage):
    """
    汇总多个 mode 的覆盖率结果
    :param modes_coverage: List[Dict] 各 mode 的覆盖率数据
    :return: Dict 汇总后的覆盖率数据
    """
    merged_data = {"summary": {}, "hierarchical": []}
    summary_fields = set()

    # 获取所有模式下的覆盖率字段
    for coverage in modes_coverage:
        summary_fields.update(coverage["summary"].keys())

    # 汇总 Total Coverage Summary
    for field in summary_fields:
        merged_data["summary"][field] = round(
            sum(coverage["summary"].get(field, 0) for coverage in modes_coverage) / len(modes_coverage),
            2  # 精确到小数点后两位
        )

    # 汇总 Hierarchical coverage data
    for coverage in modes_coverage:
        merged_data["hierarchical"].extend(coverage["hierarchical"])

    return merged_data


def display_coverage_summary(coverage_result):
    """
    格式化汇总后的覆盖率数据以便输出
    """
    print("============== Coverage Summary ==============")
    print("\nTotal Coverage Summary:")
    for key, value in coverage_result["summary"].items():
        print(f"  {key}: {value}%")

    print("\nHierarchical Coverage Data:")
    for entry in coverage_result["hierarchical"]:
        print(f"  {entry['NAME']} -> SCORE: {entry['SCORE']}%, LINE: {entry['LINE']}%, TOGGLE: {entry['TOGGLE']}%, ASSERT: {entry['ASSERT']}%")
    print("==============================================")