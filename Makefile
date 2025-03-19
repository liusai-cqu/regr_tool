# 使用 bash 作为 Shell
SHELL := /bin/bash

# 默认的参数配置
mode ?= default
ccov ?= off
tc ?= default_tc
seed ?= 123456789
wave ?= off
module_name ?= default_module

# 文件夹设置
exec_dir = $(mode)/exec
log_dir = $(mode)/log
cov_dir = $(mode)/cov
wave_dir = $(mode)/wave
urg_report_dir = $(cov_dir)/urgReport

# 日志文件
cmp_log = $(log_dir)/cmp.log
ncrun_log = $(log_dir)/$(tc)_$(seed).log
urg_log = $(cov_dir)/urg.log
dashboard_file = $(urg_report_dir)/dashboard.txt
report_file = $(cov_dir)/coverage_report.txt

# 测试目录
.PHONY: all cmp ncrun urg clean

all: cmp ncrun urg

# -------------------------------------------------
# 编译命令 - make cmp
# -------------------------------------------------
cmp:
	@echo "Compiling mode: $(mode)"
	@mkdir -p $(exec_dir) $(log_dir) $(cov_dir) $(wave_dir)
	@{ \
		echo "[INFO] Compilation started"; \
		sleep 1; \
		if [ $$RANDOM -gt 20000 ]; then \
			echo "[ERROR] Compilation failed for mode $(mode)" > $(cmp_log); \
			exit 1; \
		else \
			echo "[INFO] Compilation successful" > $(cmp_log); \
		fi; \
	}
	@if grep -q "Error" $(cmp_log); then \
		echo "[ERROR] Compilation failed. Check $(cmp_log)"; \
		exit 1; \
	else \
		echo "[INFO] Compilation successful. Log: $(cmp_log)"; \
	fi

# -------------------------------------------------
# 仿真命令 - make ncrun
# -------------------------------------------------
ncrun:
	@echo "Running test case: $(tc), seed: $(seed), mode: $(mode)"
	@mkdir -p $(log_dir)
	@{ \
		echo "[INFO] Simulation Started" > $(ncrun_log); \
		echo "[INFO] Running test case: $(tc)" >> $(ncrun_log); \
		echo "[INFO] Random Seed: $(seed)" >> $(ncrun_log); \
		sleep 1; \
		if [ $$RANDOM -gt 20000 ]; then \
			echo "[ERROR] Simulation failed during $(tc)" >> $(ncrun_log); \
			exit 1; \
		fi; \
		echo "[INFO] Simulation completed successfully" >> $(ncrun_log); \
		echo "[INFO] UVM_ERROR :    0" >> $(ncrun_log); \
		echo "NO UVM_ERROR" >> $(ncrun_log); \
	}
	@echo "[INFO] UVM_ERROR :    0"
	@echo "NO UVM_ERROR"
	@if grep -q "Error" $(ncrun_log); then \
		echo "[ERROR] Simulation failed. Check $(ncrun_log)"; \
		exit 1; \
	else \
		echo "[INFO] Simulation successful. Log: $(ncrun_log)"; \
	fi

# -------------------------------------------------
# 覆盖率生成 - make urg
# -------------------------------------------------
urg:
	@echo "[INFO] Starting coverage generation for mode: $(mode)"
	@mkdir -p $(cov_dir) $(urg_report_dir)
	@echo "Generating coverage report for mode: $(mode)" > $(urg_log)
	@sleep 1  # 模拟处理时间

	# 生成覆盖率报告 dashboard.txt 文件
	@echo "Dashboard" > $(dashboard_file)
	@echo "Date: $$(date)" >> $(dashboard_file)
	@echo "User: $$(whoami)" >> $(dashboard_file)
	@echo "Version: L-2016.06" >> $(dashboard_file)
	@echo "Command line: urg -dir simv.vdb -show ratios -format text -metric line+fsm+cond+tgl+assert -attribute attr.list" >> $(dashboard_file)
	@echo "Number of tests: 2" >> $(dashboard_file)
	@echo "-------------------------------------------------------------------------------" >> $(dashboard_file)
	@echo "Total Coverage Summary" >> $(dashboard_file)
	@echo "SCORE   LINE            COND        TOGGLE          ASSERT       " >> $(dashboard_file)
	@echo " 80.23  100.00 200/200  --     0/0   97.84 317/324   42.86 18/42 " >> $(dashboard_file)
	@echo "-------------------------------------------------------------------------------" >> $(dashboard_file)
	@echo "Hierarchical coverage data for top-level instances" >> $(dashboard_file)
	@echo "SCORE   LINE            COND           TOGGLE          ASSERT        NAME     " >> $(dashboard_file)
	@echo " 80.23  100.00 200/200  --     --       97.84 317/324   42.86 18/42  tb_jk_ff " >> $(dashboard_file)
	@echo "-------------------------------------------------------------------------------" >> $(dashboard_file)
	@echo "Total Module Definition Coverage Summary" >> $(dashboard_file)
	@echo "SCORE   LINE          COND        TOGGLE        ASSERT     " >> $(dashboard_file)
	@echo " 78.87  100.00 78/78  --     0/0   93.75 30/32   42.86 3/7" >> $(dashboard_file)

	@echo "[INFO] Dashboard report generated at $(dashboard_file)"
	@echo "[INFO] Coverage report generated at $(report_file)"

# -------------------------------------------------
# 清理命令 - make clean
# -------------------------------------------------
clean:
	@echo "Cleaning all files for mode: $(mode)"
	@rm -rf $(mode)