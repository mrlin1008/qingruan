#!/bin/bash
# ============================================================
# 益阳高新区智慧招商平台 — PostgreSQL 恢复脚本
#
# 使用方法:
#   1. 列出可用备份:  bash deploy/restore.sh list
#   2. 恢复到原库:    bash deploy/restore.sh /opt/backups/yiyang_invest/daily/yiyang_invest_20260730_020000.dump
#   3. 恢复到新库:    bash deploy/restore.sh /path/to/backup.dump --new-db yiyang_invest_restored
#   4. 仅恢复特定表:  bash deploy/restore.sh /path/to/backup.dump --table yy_companies
# ============================================================
set -euo pipefail

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-yiyang_invest}"
DB_USER="${DB_USER:-yiyang}"
DB_PASS="${DB_PASS:-changeme}"
BACKUP_ROOT="${BACKUP_ROOT:-/opt/backups/yiyang_invest}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ---- 列出可用备份 ----
list_backups() {
    echo -e "${YELLOW}可用备份列表:${NC}"
    echo ""
    for dir in daily weekly monthly; do
        local path="${BACKUP_ROOT}/${dir}"
        if [ -d "${path}" ]; then
            local count=$(ls -1 "${path}"/*.dump 2>/dev/null | wc -l)
            if [ "${count}" -gt 0 ]; then
                echo -e "${GREEN}[${dir}]${NC} ${count} 个备份:"
                ls -1lh "${path}"/*.dump | while read -r line; do
                    echo "  ${line}"
                done
                echo ""
            fi
        fi
    done
}

if [ "${1:-}" = "list" ]; then
    list_backups
    exit 0
fi

# ---- 参数解析 ----
BACKUP_FILE="${1:-}"
if [ -z "${BACKUP_FILE}" ]; then
    echo "用法: $0 <backup_file.dump> [--new-db DBNAME] [--table TABLENAME]"
    echo "       $0 list  列出所有可用备份"
    exit 1
fi

if [ ! -f "${BACKUP_FILE}" ]; then
    echo -e "${RED}错误: 备份文件不存在: ${BACKUP_FILE}${NC}"
    echo ""
    echo "使用 '$0 list' 查看可用备份"
    exit 1
fi

shift
TARGET_DB="${DB_NAME}"
RESTORE_TABLE=""
while [ $# -gt 0 ]; do
    case "$1" in
        --new-db) TARGET_DB="$2"; shift 2 ;;
        --table)  RESTORE_TABLE="--table=$2"; shift 2 ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
done

# ---- 确认操作 ----
BACKUP_SIZE=$(ls -lh "${BACKUP_FILE}" | awk '{print $5}')
echo ""
echo -e "${YELLOW}============================================${NC}"
echo -e "${YELLOW}  数据恢复确认${NC}"
echo -e "${YELLOW}============================================${NC}"
echo "  备份文件: ${BACKUP_FILE}"
echo "  备份大小: ${BACKUP_SIZE}"
echo "  目标库:   ${TARGET_DB}"
if [ -n "${RESTORE_TABLE}" ]; then
    echo "  恢复表:   ${RESTORE_TABLE#--table=}"
fi
echo ""

if [ "${TARGET_DB}" = "${DB_NAME}" ]; then
    echo -e "${RED}⚠️  警告: 将覆盖当前生产数据库 ${DB_NAME}！${NC}"
    echo -e "${RED}  所有现有数据将被替换为备份内容。${NC}"
    echo ""
fi

read -p "确认恢复? (输入 yes 继续): " CONFIRM
if [ "${CONFIRM}" != "yes" ]; then
    echo "已取消"
    exit 0
fi

# ---- 检查连接 ----
if ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -q 2>/dev/null; then
    echo -e "${RED}错误: 无法连接到 PostgreSQL${NC}"
    exit 1
fi

# ---- 执行恢复 ----
echo ""
echo -e "${GREEN}开始恢复...${NC}"
START_TS=$(date +%s)

export PGPASSWORD="${DB_PASS}"

if [ -n "${RESTORE_TABLE}" ]; then
    # 仅恢复指定表（先清空）
    echo "  清空目标表并恢复..."
    pg_restore \
        -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" \
        -d "${TARGET_DB}" \
        --clean --if-exists \
        --no-owner --no-privileges \
        "${RESTORE_TABLE}" \
        "${BACKUP_FILE}"
else
    # 全库恢复
    echo "  断开现有连接..."
    psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -c \
        "SELECT pg_terminate_backend(pg_stat_activity.pid)
         FROM pg_stat_activity
         WHERE pg_stat_activity.datname = '${TARGET_DB}' AND pid <> pg_backend_pid();" 2>/dev/null || true

    # 如果恢复到新库，先创建
    if [ "${TARGET_DB}" != "${DB_NAME}" ]; then
        echo "  创建数据库 ${TARGET_DB}..."
        psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres -c \
            "CREATE DATABASE \"${TARGET_DB}\" OWNER ${DB_USER};" 2>/dev/null || \
            echo "  (数据库可能已存在，将覆盖)"
    fi

    echo "  恢复全库..."
    pg_restore \
        -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" \
        -d "${TARGET_DB}" \
        --clean --if-exists \
        --no-owner --no-privileges \
        --jobs=2 \
        --verbose \
        "${BACKUP_FILE}"
fi

unset PGPASSWORD
END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  恢复完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo "  目标库: ${TARGET_DB}"
echo "  耗时:   ${ELAPSED}s"
echo ""
echo "  建议验证:"
echo "    psql -h ${DB_HOST} -U ${DB_USER} -d ${TARGET_DB} -c 'SELECT count(*) FROM yy_companies;'"
echo ""
