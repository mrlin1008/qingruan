#!/bin/bash
# 益阳高新区智慧招商平台 — 每日数据同步脚本
# 建议: 每天上午7:00通过cron自动执行
# crontab: 0 7 * * * /opt/yiyang_invest/deploy/daily_sync.sh >> /var/log/yiyang_invest/sync.log 2>&1

set -e
cd /opt/yiyang_invest
source venv/bin/activate

echo "=== 每日数据同步 $(date '+%Y-%m-%d %H:%M:%S') ==="

# 1. 更新入驻企业信息（天眼查）
echo "--- 更新企业信息 ---"
python3 -c "
from app import app, db
from models import Company, BiddingRecord
from utils.data_fetcher import sync_bidding_for_company

with app.app_context():
    companies = Company.query.filter_by(company_type='settled', status='active').all()
    total = 0
    for c in companies:
        try:
            n = sync_bidding_for_company(c.name, db, BiddingRecord, Company)
            total += n
        except Exception as e:
            print(f'  同步失败: {c.name} - {e}')
    print(f'  共新增 {total} 条招投标记录')
" 2>&1

# 2. 更新园区统计
echo "--- 更新园区统计 ---"
python3 -c "
from app import app, db
from models import ParkInfo, Company, Project
from sqlalchemy import func

with app.app_context():
    park = ParkInfo.query.first()
    if park:
        park.settled_count = Company.query.filter_by(company_type='settled', status='active').count()
        park.investment_total = db.session.query(func.sum(Project.amount)).filter_by(stage='签约').scalar() or 0
        db.session.commit()
        print(f'  入驻企业: {park.settled_count}, 签约金额: {park.investment_total}万')
" 2>&1

echo "=== 同步完成 $(date '+%Y-%m-%d %H:%M:%S') ==="
