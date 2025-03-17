#!/bin/bash
# 模拟 SIMV 行为，运行用例并生成日志文件

LOG_FILE=$1  # 第一个参数为日志文件路径
TC_NAME=$2   # 第二个参数为测试用例名称
SEED=$3      # 第三个参数为种子值

# 检查日志文件路径是否提供
if [ -z "$LOG_FILE" ] || [ -z "$TC_NAME" ] || [ -z "$SEED" ]; then
  echo "Usage: $0 <log_file> <testcase> <seed>" >&2
  exit 1
fi

# 模拟日志输出
echo "[INFO] Simulation Started" > "$LOG_FILE"
echo "[INFO] Running test case: $TC_NAME" >> "$LOG_FILE"
echo "[INFO] Random Seed: $SEED" >> "$LOG_FILE"
sleep 1
if [ $RANDOM -gt 20000 ]; then  # 随机模拟错误
  echo "[ERROR] Simulation failed during $TC_NAME" >> "$LOG_FILE"
  exit 1
fi
echo "[INFO] Simulation completed successfully" >> "$LOG_FILE"
exit 0