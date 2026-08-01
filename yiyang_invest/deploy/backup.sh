#!/bin/bash
# ============================================================
# 益阳高新区智慧招商平台 — PostgreSQL 自动备份脚本
#
# 策略:
#   - 每日增量: pg_dump 自定义格式，保留 7 天
#   - 每周全量: 每周日凌晨，保留 4 周
#   - 每月归档: 每月1号，保留 6 个月
#
# cron 配置:
#   0 2 * * * /opt/yiyang_invest/deploy/backup.sh daily  >> /var/log/yiyang_invest/backup.log 2>&1
#   0 3 * * 0 /opt/yiyang_invest/deploy/backup.sh weekly >> /var/log/yiyang_invest/backup.log 2>&1
#   0 4 1 * * /opt/yiyang_invest/deploy/backup.sh monthly >> /var/log/yiyang_invest/backup.log 2>&1
# ============================================================
set -euo pipefail

# ---- 配置 ----
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-yiyang_invest}"
DB_USER="${DB_USER:-yiyang}"
DB_PASS="${DB_PASS:-changeme}"

BACKUP_ROOT="${BACKUP_ROOT:-/opt/backups/yiyang_invest}"
REMOTE_BACKUP="${REMOTE_BACKUP:-}"  # user@host:/path 或留空跳过
RETENTION_DAILY="${RETENTION_DAILY:-7}"
RETENTION_WEEKLY="${RETENTION_WEEKLY:-4}"
RETENTION_MONTHLY="${RETENTION_MONTHLY:-6}"

MODE="${1:-daily}"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
WEEK=$(date '+%Y-W%U')
MONTH=$(date '+%Y-%m')

LOG_TAG="[backup-${MODE}]"

# ---- 确保目录存在 ----
for dir in daily weekly monthly; do
    mkdir -p "${BACKUP_ROOT}/${dir}"
done

# ---- 备份文件路径 ----
case "${MODE}" in
    daily)   BACKUP_DIR="${BACKUP_ROOT}/daily";   BACKUP_FILE="yiyang_invest_${TIMESTAMP}.dump" ;;
    weekly)  BACKUP_DIR="${BACKUP_ROOT}/weekly";  BACKUP_FILE="yiyang_invest_${WEEK}.dump" ;;
    monthly) BACKUP_DIR="${BACKUP_ROOT}/monthly"; BACKUP_FILE="yiyang_invest_${MONTH}.dump" ;;
    *)
        echo "用法: $0 {daily|weekly|monthly}"
        exit 1
        ;;
esac

BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"
LOG_PATH="${BACKUP_ROOT}/backup_history.log"

# ---- 备份前检查 ----
echo "=== ${LOG_TAG} $(date '+%Y-%m-%d %H:%M:%S') 开始 ${MODE} 备份 ===" | tee -a "${LOG_PATH}"

# 检查 PostgreSQL 是否运行
if ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -q 2>/dev/null; then
    echo "${LOG_TAG} 错误: PostgreSQL 未运行或无法连接" | tee -a "${LOG_PATH}" >&2
    exit 1
fi

# 检查磁盘空间（至少需要 1GB）
AVAIL_KB=$(df -k "${BACKUP_ROOT}" | tail -1 | awk '{print $4}')
if [ "${AVAIL_KB}" -lt 1048576 ]; then
    echo "${LOG_TAG} 警告: 磁盘可用空间不足 1GB (剩余 ${AVAIL_KB}KB)" | tee -a "${LOG_PATH}" >&2
fi

# ---- 执行备份 ----
START_TS=$(date +%s)

export PGPASSWORD="${DB_PASS}"
pg_dump \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    --format=custom \
    --compress=9 \
    --verbose \
    --no-owner \
    --no-privileges \
    -f "${BACKUP_PATH}" \
    2>&1 | tee -a "${LOG_PATH}"

unset PGPASSWORD
END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))

# ---- 备份文件信息 ----
BACKUP_SIZE=$(stat -f%z "${BACKUP_PATH}" 2>/dev/null || stat -c%s "${BACKUP_PATH}" 2>/dev/null || echo 0)
BACKUP_SIZE_MB=$(echo "scale=1; ${BACKUP_SIZE}/1048576" | bc 2>/dev/null || echo "?")

echo "${LOG_TAG} 备份完成: ${BACKUP_PATH}" | tee -a "${LOG_PATH}"
echo "${LOG_TAG} 大小: ${BACKUP_SIZE_MB}MB, 耗时: ${ELAPSED}s" | tee -a "${LOG_PATH}"

# ---- 备份完整性校验 ----
echo "${LOG_TAG} 校验备份..." | tee -a "${LOG_PATH}"
export PGPASSWORD="${DB_PASS}"
if pg_restore -l "${BACKUP_PATH}" > /dev/null 2>&1; then
    echo "${LOG_TAG} 校验通过 ✓" | tee -a "${LOG_PATH}"
else
    echo "${LOG_TAG} 校验失败 ✗ — 备份文件可能损坏！" | tee -a "${LOG_PATH}" >&2
    unset PGPASSWORD
    exit 1
fi
unset PGPASSWORD

# ---- 清理过期备份 ----
cleanup() {
    local dir=$1
    local keep=$2
    local label=$3
    local count=$(ls -1 "${dir}"/*.dump 2>/dev/null | wc -l)
    local del=$((count - keep))
    if [ "${del}" -gt 0 ]; then
        echo "${LOG_TAG} 清理 ${label} 备份: 保留 ${keep}/${count}，删除 ${del} 个" | tee -a "${LOG_PATH}"
        ls -1t "${dir}"/*.dump | tail -n "${del}" | while read -r f; do
            echo "  删除: $(basename "${f}")" | tee -a "${LOG_PATH}"
            rm -f "${f}"
        done
    fi
}

cleanup "${BACKUP_ROOT}/daily"   "${RETENTION_DAILY}"   "每日"
cleanup "${BACKUP_ROOT}/weekly"  "${RETENTION_WEEKLY}"  "每周"
cleanup "${BACKUP_ROOT}/monthly" "${RETENTION_MONTHLY}" "每月"

# ---- 远程同步（可选） ----
if [ -n "${REMOTE_BACKUP}" ]; then
    echo "${LOG_TAG} 同步到远程: ${REMOTE_BACKUP}" | tee -a "${LOG_PATH}"
    rsync -avz --delete "${BACKUP_ROOT}/" "${REMOTE_BACKUP}/" 2>&1 | tail -3 | tee -a "${LOG_PATH}" || {
        echo "${LOG_TAG} 警告: 远程同步失败，本地备份不受影响" | tee -a "${LOG_PATH}" >&2
    }
fi

# ---- 汇总报告 ----
echo "---" | tee -a "${LOG_PATH}"
echo "${LOG_TAG} 备份汇总:" | tee -a "${LOG_PATH}"
for dir in daily weekly monthly; do
    count=$(ls -1 "${BACKUP_ROOT}/${dir}"/*.dump 2>/dev/null | wc -l)
    size=$(du -sh "${BACKUP_ROOT}/${dir}" 2>/dev/null | awk '{print $1}')
    echo "  ${dir}: ${count} 个文件, ${size}" | tee -a "${LOG_PATH}"
done
echo "=== ${LOG_TAG} $(date '+%Y-%m-%d %H:%M:%S') 完成 ===" | tee -a "${LOG_PATH}"
