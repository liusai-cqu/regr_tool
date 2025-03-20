#!/usr/bin/env python3
from config import GConf
from directory_manager import DirectoryManager
from compiler import Compiler
from simulation import SimulationManager
from coverage import CoverageManager
from report import ReportGenerator

def main():
    import argparse

    # 创建参数解析器
    parser = argparse.ArgumentParser(description="Regression Tool for Verification")

    # 基础参数
    parser.add_argument("-n", "--name", help="指定回归任务名称", default=None)
    parser.add_argument("-m", "--mode", action="append", help="模式列表，例如: base_fun, axi3, axi4")
    parser.add_argument("--parallel", type=int, default=20, help="设置并行任务上限 (默认: 20)")

    # 阶段控制参数
    parser.add_argument("--skip_cmp", action="store_true", help="跳过编译阶段")
    parser.add_argument("--skip_sim", action="store_true", help="跳过仿真阶段")
    parser.add_argument("--skip_cov_gen", action="store_true", help="跳过覆盖率生成阶段")
    parser.add_argument("--skip_cov_rpt", action="store_true", help="跳过覆盖率报告生成阶段")

    # 覆盖率相关参数
    parser.add_argument("--ccov", choices=["on", "off"], default="on", help="覆盖率开关 (默认: on)")
    parser.add_argument("--disable_cov", action="store_true", help="禁用覆盖率相关功能")

    # 测试用例参数
    parser.add_argument("--testcases", type=str, help="从测试用例文件加载测试用例列表 (JSON 格式)")
    parser.add_argument("--random_seed", type=int, default=1234, help="设置随机种子 (默认: 1234)")

    # 通用参数
    parser.add_argument("--log_level", choices=["INFO", "DEBUG", "WARNING", "ERROR"], default="DEBUG",
                        help="设置日志级别 (默认: INFO)")

    # 解析参数
    args = parser.parse_args()

    # 全局配置
    gconf = GConf(args)

    # 初始化功能模块
    # 初始化目录管理器（传入 gconf.base_dir）
    dm = DirectoryManager(gconf.base_dir)
    compiler = Compiler(gconf)
    simulator = SimulationManager(gconf)
    coverage = CoverageManager(gconf)
    reporter = ReportGenerator(gconf)

    # 主流程
    # 创建回归目录
    dm.create_regression_directory()
    dm.copy_makefile()
    # 创建模式目录
    modes = gconf.mode or ["default_mode"]  # 默认模式可以是 ["default_mode"] 或从 gconf.mode 读取
    dm.create_mode_directories(modes)

    if not gconf.skip_cmp:
        for mode in gconf.mode:
            compiler.compile_mode(mode)

    if not gconf.skip_sim:
        simulator.run_simulations()

    if not gconf.skip_cov_gen:
        for mode in gconf.mode:
            # 为每个模式生成覆盖率报告
            if not coverage.generate_coverage_report(mode):
                gconf.logger.error(f"Failed to generate coverage report for mode: {mode}")

    reporter.generate_final_report()

if __name__ == "__main__":
    main()