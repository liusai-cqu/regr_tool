#!/bin/bash
# 模拟 VCS 命令的编译行为，生成日志文件

LOG_FILE=$1  # 第一个参数为日志文件路径

# 检查日志文件路径是否提供
if [ -z "$LOG_FILE" ]; then
  echo "Usage: $0 <log_file>" >&2
  exit 1
fi

# 模拟日志输出
echo "[INFO] VCS Compilation Started" > "$LOG_FILE"
sleep 1  # 模拟编译的时间
echo "[INFO] Compiling file1.sv" >> "$LOG_FILE"
echo "[INFO] Compiling file2.sv" >> "$LOG_FILE"
sleep 1
if [ $RANDOM -gt 20000 ]; then  # 随机模拟错误
  echo "[INFO] Compilation failed at module file2.sv" >> "$LOG_FILE"
  exit 0
fi
echo "[INFO] Compilation completed successfully" >> "$LOG_FILE"
exit 0