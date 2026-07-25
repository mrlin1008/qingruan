"""
批量从天眼查更新所有客户的招投标数据
用法: python3 bulk_update_bidding.py
"""
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Customer, BiddingRecord


def main():
    with app.app_context():
        customers = Customer.query.order_by(Customer.id).all()
        total = len(customers)
        total_imported = 0
        total_errors = 0
        total_skipped = 0  # 无记录

        print(f'📊 共 {total} 个客户，开始批量更新招投标数据...\n')

        for i, customer in enumerate(customers):
            name = customer.name
            print(f'[{i+1}/{total}] 🔍 {name} ...', end=' ', flush=True)

            try:
                from tianyancha_api import fetch_bidding
                data = fetch_bidding(name)
            except Exception as e:
                print(f'❌ 模块错误: {e}')
                total_errors += 1
                continue

            if isinstance(data, dict) and 'error' in data:
                msg = data.get('message', str(data))
                print(f'⚠️  {msg}')
                total_errors += 1
                # 遇到限流就等一下
                if '频率' in msg or '限流' in msg or 'too many' in msg.lower():
                    time.sleep(5)
                continue

            if not data:
                print(f'📭 无记录')
                total_skipped += 1
                continue

            imported = 0
            for r in data:
                existing = BiddingRecord.query.filter_by(
                    project_name=r.get('project_name', ''),
                    bidder_name=r.get('bidder_name', name),
                ).first()
                if existing:
                    continue
                record = BiddingRecord(
                    customer_id=customer.id,
                    project_name=r.get('project_name', ''),
                    bidder_name=r.get('bidder_name', name),
                    winner_name=r.get('winner_name', ''),
                    bid_amount=r.get('bid_amount', 0),
                    publish_date=r.get('publish_date', ''),
                    product_detail=r.get('summary', '') or r.get('project_name', ''),
                    source='天眼查API',
                    source_url=r.get('bid_url', '') or r.get('source_url', ''),
                )
                db.session.add(record)
                imported += 1

            if imported > 0:
                db.session.commit()
                total_imported += imported
                print(f'✅ +{imported}条')
            else:
                print(f'📭 已存在，无新增')

            # 避免请求太快
            time.sleep(0.5)

    print(f'\n{"="*50}')
    print(f'🎯 批量更新完成！')
    print(f'   总客户数: {total}')
    print(f'   新增记录: {total_imported} 条')
    print(f'   无记录:   {total_skipped} 个')
    print(f'   出错:     {total_errors} 个')
    print(f'{"="*50}')


if __name__ == '__main__':
    main()
