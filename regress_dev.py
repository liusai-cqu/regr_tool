import argparse
import os
import time
from coverage_parser import CoverageParser
from task_manager import TaskManager

__version__ = "1.0.0"  # 程序版本

# 参数解析
def parse_arguments():
    parser = argparse.ArgumentParser(description="RegressionTool for RTL testing automation.")

    # 参数选项
    parser.add_argument("-v", "--version", action="store_true", help="显示程序版本")
    parser.add_argument("-sc", "--skip_cmp", action="store_true", help="跳过编译阶段")
    parser.add_argument("-ss", "--skip_sim", action="store_true", help="跳过仿真阶段")
    parser.add_argument("-scg", "--skip_cov_gen", action="store_true", help="跳过覆盖率生成阶段")
    parser.add_argument("-scr", "--skip_cov_rpt", action="store_true", help="跳过覆盖率报告解析")
    parser.add_argument("-l", "--regr_list", type=str, help="指定回归列表类名")
    parser.add_argument("-n", "--name", type=str, help="指定回归路径（运行目录）")
    parser.add_argument("-m", "--mode", action="append", default=[], help="追加 mode 参数，用于编译配置")
    parser.add_argument("-r", "--rerun", action="store_true", help="对非 PASS 的案例进行 rerun 测试")

    return parser.parse_args()


# 参数验证
def validate_arguments(args):
    """
    根据参数的功能和约束关系验证参数的有效性
    """
    if args.skip_cmp or args.skip_sim or args.skip_cov_gen or args.skip_cov_rpt:
        if not args.name:
            raise ValueError("当使用 --skip_cmp, --skip_sim, --skip_cov_gen 或 --skip_cov_rpt 参数时，必须通过 -n 指定一个回归路径。")

    if args.skip_cmp:
        path = os.path.join(args.name, "env")
        if not os.path.exists(path):
            raise FileNotFoundError(f"环境目录未找到：{path}. 必须确保路径下的环境已编译。")

    if args.skip_sim:
        path = os.path.join(args.name, "case_list.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"仿真案例文件未找到：{path}. 必须确保路径下包含 case_list.json 文件。")

    if args.skip_cov_gen:
        path = os.path.join(args.name, "coverage_data")
        if not os.path.exists(path):
            raise FileNotFoundError(f"覆盖率数据路径未找到：{path}. 请确认指定的路径中包含覆盖率数据。")

    if args.skip_cov_rpt:
        path = os.path.join(args.name, "dashboard.txt")
        if not os.path.exists(path):
            raise FileNotFoundError(f"覆盖率报告文件未找到：{path}. 请确认指定的路径中包含覆盖率报告。")


# 处理参数主逻辑
def main():
    args = parse_arguments()

    # 如果用户请求版本信息，直接显示并退出
    if args.version:
        print(f"RegressionTool Version: {__version__}")
        return

    try:
        # 先验证参数合法性
        validate_arguments(args)

        # 处理 -n (回归路径)，如果未指定，自动生成路径
        regr_path = args.name or f"regression_{int(time.time())}"
        if not os.path.exists(regr_path):
            os.makedirs(regr_path)
            print(f"[INFO] Created regression directory: {regr_path}")
        else:
            print(f"[INFO] Using existing regression directory: {regr_path}")

        # 根据参数处理不同功能
        if not args.skip_cmp:
            print("[INFO] 开始编译阶段...")
            # 调用编译逻辑函数
            run_compilation(regr_path, args.mode)

        if not args.skip_sim:
            print("[INFO] 开始仿真阶段...")
            # 调用仿真逻辑函数
            run_simulation(regr_path)

        if not args.skip_cov_gen:
            print("[INFO] 开始生成覆盖率数据...")
            # 调用生成覆盖率数据的函数
            generate_coverage(regr_path)

        if not args.skip_cov_rpt:
            print("[INFO] 开始解析覆盖率报告...")
            # 调用解析覆盖率报告的函数
            parse_coverage_reports(regr_path)

        if args.rerun:
            print("[INFO] 开始 rerun 测试...")
            # 调用重新运行失败案例的函数
            rerun_failed_cases(regr_path)

    except Exception as e:
        print(f"[ERROR] {str(e)}")


def run_compilation(regr_path, modes):
    """编译阶段逻辑"""
    print(f"[DEBUG] Compiling with modes: {modes}")
    # 模拟编译操作
    for mode in modes:
        print(f"Compiling mode: {mode}")
        time.sleep(1)  # 模拟耗时


def run_simulation(regr_path):
    """仿真阶段逻辑"""
    print(f"[DEBUG] Running simulation in {regr_path}...")
    # 模拟仿真操作
    time.sleep(2)  # 模拟耗时


def generate_coverage(regr_path):
    """生成覆盖率阶段逻辑"""
    print(f"[DEBUG] Generating coverage data in {regr_path}...")
    # 模拟覆盖率生成操作
    time.sleep(2)  # 模拟耗时


def parse_coverage_reports(regr_path):
    """解析覆盖率报告阶段逻辑"""
    print(f"[DEBUG] Parsing coverage reports in {regr_path}...")
    parser = CoverageParser(regr_path, "default_mode")
    coverage_data = parser.parse_dashboard()
    print(f"[INFO] Parsed coverage: {coverage_data}")


def rerun_failed_cases(regr_path):
    """rerun 失败案例逻辑"""
    case_list_path = os.path.join(regr_path, "case_list_result.json")
    if not os.path.exists(case_list_path):
        raise FileNotFoundError(f"case_list_result.json not found in {regr_path}")

    print("[DEBUG] Parsing failed cases and generating rerun file...")
    # 模拟读取和生成 case_list_rerun.json 文件
    time.sleep(1)
    print("[INFO] Rerun completed and updated results.")


if __name__ == "__main__":
    main()