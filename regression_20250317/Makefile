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

# 日志文件
cmp_log = $(log_dir)/cmp.log
ncrun_log = $(log_dir)/$(tc)_$(seed).log
urg_log = $(cov_dir)/urg.log
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
	@./mock_vcs.sh $(cmp_log)
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
	@./mock_simv.sh $(ncrun_log) $(tc) $(seed)
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
	@mkdir -p $(cov_dir)
	@echo "Generating coverage report for mode: $(mode)" > $(urg_log)
	@sleep 1  # 模拟处理时间
	@echo "Line Coverage: 82.5%" >> $(report_file)
	@echo "Functional Coverage: 88.9%" >> $(report_file)
	@echo "Toggle Coverage: 91.7%" >> $(report_file)
	@echo "[INFO] Coverage report generated at $(report_file)"
	@echo "[INFO] Log file generated at $(urg_log)"

# -------------------------------------------------
# 清理命令 - make clean
# -------------------------------------------------
clean:
	@echo "Cleaning all files for mode: $(mode)"
	@rm -rf $(mode)