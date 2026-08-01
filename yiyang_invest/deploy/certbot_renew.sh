#!/bin/bash
# ============================================================
# 益阳高新区智慧招商平台 — 证书续期脚本
# 建议: 每天凌晨 3:00 执行一次
# crontab: 0 3 * * * /opt/yiyang_invest/deploy/certbot_renew.sh >> /var/log/yiyang_invest/certbot_renew.log 2>&1
# ============================================================
set -e

LOG_TAG="[certbot-renew $(date '+%Y-%m-%d %H:%M:%S')]"

echo "=== ${LOG_TAG} 开始检查证书续期 ==="

# 续期（只续 30 天内到期的证书）
certbot renew --quiet --post-hook "systemctl reload nginx"

if [ $? -eq 0 ]; then
    echo "${LOG_TAG} 续期检查完成（无需更新或已更新）"
else
    echo "${LOG_TAG} 续期失败！请检查 certbot 日志" >&2
    exit 1
fi

# 显示证书到期时间
echo "${LOG_TAG} 当前证书状态:"
certbot certificates 2>/dev/null | grep -E "Domains|Expiry" | paste - - | sed 's/Domains:/  域名: /; s/Expiry Date:/  到期: /'

echo "=== ${LOG_TAG} 完成 ==="
