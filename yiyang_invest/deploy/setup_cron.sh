#!/bin/bash
# ============================================================
# 益阳高新区智慧招商平台 — Cron 定时任务安装脚本
# 以 root 运行: sudo bash deploy/setup_cron.sh
# ============================================================
set -e

PROJECT_ROOT="/opt/yiyang_invest"
LOG_DIR="/var/log/yiyang_invest"

mkdir -p "${LOG_DIR}"

# 读取当前 crontab，追加任务
CURRENT=$(crontab -l 2>/dev/null || true)

# 检查是否已安装
if echo "${CURRENT}" | grep -q "yiyang_invest"; then
    echo "检测到已有 yiyang_invest 相关 cron 任务，将替换..."
    CURRENT=$(echo "${CURRENT}" | grep -v "yiyang_invest")
fi

cat <<EOF | crontab - <(echo "${CURRENT}")

# ===== 益阳高新区智慧招商平台 定时任务 =====

# 每日数据同步（天眼查招投标 + 园区统计）— 每天 7:00
0 7 * * * ${PROJECT_ROOT}/deploy/daily_sync.sh >> ${LOG_DIR}/sync.log 2>&1

# PostgreSQL 每日备份 — 每天凌晨 2:00
0 2 * * * ${PROJECT_ROOT}/deploy/backup.sh daily >> ${LOG_DIR}/backup.log 2>&1

# PostgreSQL 每周全量备份 — 每周日凌晨 3:00
0 3 * * 0 ${PROJECT_ROOT}/deploy/backup.sh weekly >> ${LOG_DIR}/backup.log 2>&1

# PostgreSQL 每月归档备份 — 每月 1 号凌晨 4:00
0 4 1 * * ${PROJECT_ROOT}/deploy/backup.sh monthly >> ${LOG_DIR}/backup.log 2>&1

# Let's Encrypt 证书自动续期 — 每天凌晨 3:30
30 3 * * * ${PROJECT_ROOT}/deploy/certbot_renew.sh >> ${LOG_DIR}/certbot_renew.log 2>&1

EOF

echo "Cron 任务已安装:"
echo ""
crontab -l | grep "yiyang_invest" | while read -r line; do
    echo "  ${line}"
done
echo ""
echo "日志目录: ${LOG_DIR}"
echo ""
echo "可手动执行:"
echo "  备份: bash ${PROJECT_ROOT}/deploy/backup.sh daily"
echo "  恢复: bash ${PROJECT_ROOT}/deploy/restore.sh list"
