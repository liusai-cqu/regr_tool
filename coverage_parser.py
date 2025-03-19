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
            "meta": {},                     # 文件元信息
            "summary": {},                  # Total Coverage Summary 数据
            "hierarchical": [],             # Hierarchical coverage data 数据
            "module_definition": []         # Total Module Definition Coverage 数据
        }

    def parse_dashboard(self):
        """
        解析 dashboard.txt 文件，提取覆盖率数据
        """
        if not os.path.exists(self.dashboard_path):
            raise FileNotFoundError(f"Dashboard file not found at {self.dashboard_path}")

        section = None  # 当前处理的章节状态

        with open(self.dashboard_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()  # 去除空白字符

                # 忽略分隔线或空行
                if not line or re.match(r"^-+$", line):
                    continue

                # 文件元信息 (Meta 信息)
                if line.startswith("Date:") or line.startswith("User:") or line.startswith("Version:") or line.startswith("Command line:") or line.startswith("Number of tests:"):
                    self._parse_meta(line)
                    continue

                # 段落标题检测并切换解析状态
                if re.match(r"^Total Coverage Summary", line):
                    section = "summary"
                    continue

                if re.match(r"^Hierarchical coverage data", line):
                    section = "hierarchical"
                    continue

                if re.match(r"^Total Module Definition Coverage Summary", line):
                    section = "module_definition"
                    continue

                # 忽略表头行
                if re.match(r"^SCORE\s+", line) or "NAME" in line:
                    continue

                # 处理数据内容
                try:
                    if section == "summary":
                        self._parse_data(line, line_number, "summary", has_name=False)
                    elif section == "hierarchical":
                        self._parse_data(line, line_number, "hierarchical", has_name=True)
                    elif section == "module_definition":
                        self._parse_data(line, line_number, "module_definition", has_name=False)
                    else:
                        # 忽略无关部分
                        continue
                except ValueError as e:
                    print(f"[ERROR] Line {line_number}: {e} -> Section: {section} -> Content: '{line}'")

        return self.coverage_data

    def _parse_meta(self, line):
        """
        提取文件元信息
        """
        if line.startswith("Date:"):
            self.coverage_data["meta"]["Date"] = line.split("Date:", 1)[1].strip()
        elif line.startswith("User:"):
            self.coverage_data["meta"]["User"] = line.split("User:", 1)[1].strip()
        elif line.startswith("Version:"):
            self.coverage_data["meta"]["Version"] = line.split("Version:", 1)[1].strip()
        elif line.startswith("Command line:"):
            self.coverage_data["meta"]["Command"] = line.split("Command line:", 1)[1].strip()
        elif line.startswith("Number of tests:"):
            self.coverage_data["meta"]["Tests"] = int(line.split("Number of tests:", 1)[1].strip())

    def _parse_data(self, line, line_number, section, has_name=False):
        """
        通用数据解析逻辑，适配不同段落
        """
        # 动态生成正则表达式，根据是否需要匹配 NAME 字段
        regex = (
            r"^\s*(\d+\.\d+)\s+"            # SCORE
            r"(\d+\.\d+)\s+"                # LINE percentage
            r"([\d\-]+/[\d\-]+)\s+"         # LINE Details
            r"(\d+\.\d+|--)\s+"             # COND percentage
            r"([\d\-]+/[\d\-]+|--)\s+"      # COND Details
            r"(\d+\.\d+|--)\s+"             # TOGGLE percentage
            r"([\d\-]+/[\d\-]+|--)\s+"      # TOGGLE Details
            r"(\d+\.\d+|--)\s+"             # FSM percentage
            r"([\d\-]+/[\d\-]+|--)\s+"      # FSM Details
            r"(\d+\.\d+|--)\s+"             # ASSERT percentage
            r"([\d\-]+/[\d\-]+|--)"         # ASSERT Details
        )
        if has_name:
            regex += r"\s+(\S+)$"           # NAME (只有 hierarchical 有 NAME 字段)
        else:
            regex += r"$"                   # module_definition 和 summary 不需要 NAME

        # 匹配正则表达式
        match = re.match(regex, line)
        if not match:
            raise ValueError(f"Failed to match {section} line format")

        # 解析匹配的字段
        groups = match.groups()
        data_entry = {
            "SCORE": float(groups[0]),
            "LINE": float(groups[1]),
            "LINE_DETAILS": groups[2],
            "COND": float(groups[3]) if groups[3] != "--" else None,
            "COND_DETAILS": groups[4] if groups[4] != "--" else None,
            "TOGGLE": float(groups[5]) if groups[5] != "--" else None,
            "TOGGLE_DETAILS": groups[6] if groups[6] != "--" else None,
            "FSM": float(groups[7]) if groups[7] != "--" else None,
            "FSM_DETAILS": groups[8] if groups[8] != "--" else None,
            "ASSERT": float(groups[9]) if groups[9] != "--" else None,
            "ASSERT_DETAILS": groups[10] if groups[10] != "--" else None
        }

        if has_name:
            data_entry["NAME"] = groups[11]  # 添加 NAME 字段

        # 根据段落类型存储解析结果
        if section == "summary":
            self.coverage_data["summary"] = data_entry
        elif section == "hierarchical":
            self.coverage_data["hierarchical"].append(data_entry)
        elif section == "module_definition":
            self.coverage_data["module_definition"].append(data_entry)

    def display_coverage_summary(self):
        """
        格式化汇总后的覆盖率数据以便输出
        """
        print("============== Coverage Summary ==============")
        print("\nMeta Information:")
        for key, value in self.coverage_data["meta"].items():
            print(f"  {key}: {value}")
        print("\nTotal Coverage Summary:")
        for key, value in self.coverage_data["summary"].items():
            print(f"  {key}: {value if value is not None else '--'}%")

        print("\nHierarchical Coverage Data:")
        for entry in self.coverage_data["hierarchical"]:
            print(f"  {entry['NAME']} -> SCORE: {entry['SCORE']}%, "
                  f"LINE: {entry['LINE']}%, COND: {entry['COND']}%, "
                  f"FSM: {entry['FSM']}%, TOGGLE: {entry['TOGGLE']}%, ASSERT: {entry['ASSERT']}%")

        print("\nModule Definition Coverage Summary:")
        for entry in self.coverage_data["module_definition"]:
            print(f"  SCORE: {entry['SCORE']}%, LINE: {entry['LINE']}%, "
                  f"COND: {entry['COND']}%, ASSERT: {entry['ASSERT']}%")
        print("==============================================")