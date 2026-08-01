#!/bin/bash
# ============================================================
# 益阳高新区智慧招商平台 — HTTPS 证书初始化脚本
# 使用方法:
#   1. 将 DOMAIN 替换为实际域名
#   2. 确保域名 DNS 已指向服务器 IP
#   3. 以 root 运行: sudo bash deploy/setup_https.sh
# ============================================================
set -e

DOMAIN="${DOMAIN:-invest.yiyang-hitech.example.com}"
EMAIL="${EMAIL:-admin@example.com}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== 益阳高新区智慧招商平台 HTTPS 初始化 ===${NC}"
echo "域名: ${DOMAIN}"
echo "邮箱: ${EMAIL}"
echo ""

# ---- 1. 安装依赖 ----
echo -e "${YELLOW}[1/5] 安装依赖...${NC}"
if command -v apt-get &> /dev/null; then
    apt-get update -qq
    apt-get install -y -qq certbot python3-certbot-nginx nginx
elif command -v yum &> /dev/null; then
    yum install -y epel-release
    yum install -y certbot python3-certbot-nginx nginx
elif command -v dnf &> /dev/null; then
    dnf install -y epel-release
    dnf install -y certbot python3-certbot-nginx nginx
else
    echo -e "${RED}不支持的包管理器，请手动安装 certbot 和 nginx${NC}"
    exit 1
fi

# ---- 2. 创建 ACME 验证目录 ----
echo -e "${YELLOW}[2/5] 创建 ACME 验证目录...${NC}"
mkdir -p /var/www/certbot

# ---- 3. 复制 Nginx 配置 ----
echo -e "${YELLOW}[3/5] 部署 Nginx 配置...${NC}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cp "${SCRIPT_DIR}/nginx.conf" /etc/nginx/sites-available/yiyang_invest
sed -i "s/invest.yiyang-hitech.example.com/${DOMAIN}/g" /etc/nginx/sites-available/yiyang_invest

# 适配不同 Nginx 目录结构
if [ -d /etc/nginx/sites-enabled ]; then
    ln -sf /etc/nginx/sites-available/yiyang_invest /etc/nginx/sites-enabled/yiyang_invest
elif [ -d /etc/nginx/conf.d ]; then
    ln -sf /etc/nginx/sites-available/yiyang_invest /etc/nginx/conf.d/yiyang_invest.conf
fi

# ---- 4. 先以 HTTP 模式启动 Nginx（用于验证） ----
echo -e "${YELLOW}[4/5] 启动 Nginx（HTTP 验证模式）...${NC}"
# 临时去掉 SSL 相关指令做验证
sed -i 's/listen 443 ssl http2;/#listen 443 ssl http2;/g' /etc/nginx/sites-available/yiyang_invest
sed -i 's/listen \[::\]:443 ssl http2;/#listen [::]:443 ssl http2;/g' /etc/nginx/sites-available/yiyang_invest
nginx -t && systemctl reload nginx

# ---- 5. 申请证书 ----
echo -e "${YELLOW}[5/5] 申请 Let's Encrypt 证书...${NC}"
certbot certonly --webroot \
    -w /var/www/certbot \
    -d "${DOMAIN}" \
    --email "${EMAIL}" \
    --agree-tos \
    --no-eff-email \
    --force-renewal

# ---- 6. 恢复完整 HTTPS 配置 ----
echo -e "${YELLOW}恢复 HTTPS 配置...${NC}"
sed -i 's/#listen 443 ssl http2;/listen 443 ssl http2;/g' /etc/nginx/sites-available/yiyang_invest
sed -i 's/#listen \[::\]:443 ssl http2;/listen [::]:443 ssl http2;/g' /etc/nginx/sites-available/yiyang_invest
nginx -t && systemctl reload nginx

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  HTTPS 配置完成！${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "  站点地址: https://${DOMAIN}"
echo "  证书路径: /etc/letsencrypt/live/${DOMAIN}/"
echo ""
echo "  证书将在 90 天后到期，已配置自动续期。"
echo "  手动续期命令: sudo certbot renew --dry-run"
echo ""
