"""
正确方案：按424个客户逐个查询天眼查招投标
仅保留含网络安全关键词 + 近一年的项目
"""
import sys, os, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, BiddingRecord

# 网络安全相关关键词（来自 网络安全相关.docx）
CYBER_KEYWORDS = [
    # 安全产品
    '防火墙', 'NGFW', 'WEB防火墙', 'WAF', '入侵防御', 'IPS', '入侵检测', 'IDS',
    '堡垒机', '运维审计', '日志审计', '数据库审计', '漏洞扫描',
    '主机安全', '蜜罐', 'SD-WAN', '安全管理平台', '安全探针',
    # 国产化
    '国产芯片', '国产操作系统', '国产化产品', '信创',
    # 安全服务
    '网络安全运维', '安全运营服务', '安全监测与防护', '网络安全技术服务',
    '渗透测试', '漏洞扫描服务', '风险评估', '网络安全能力验证',
    # 合规
    '等级保护测评', '等保测评', '商用密码应用安全性评估', '密评',
    '网络安全合规', '关键信息基础设施',
    # 攻防
    '网络安全攻防演练', '攻防演练', '网络安全竞赛', '网络安全培训',
    # 数据安全
    '数据防泄漏', 'DLP', '数据库脱敏', '数据安全运营', '数据安全风险评估',
    '数据安全', '数据防泄密',
    # 工控安全
    '工控防火墙', '工业网闸', '工控安全审计', '工控安全', '工业互联网安全',
    # 灾备
    '容灾备份', '灾备', '备份一体机', '数据备份', '数据容灾',
    # 云
    '政务云', '行业云', '云平台', '云基础设施', '云底座',
    # 服务器
    '服务器采购', '服务器设备',
    # 安全设备/服务
    '安全设备续保', '网络安全保障', '安全监测', '安全运营',
    '网络安全服务', '信息安全', '信息网络安全',
]

CUTOFF_DATE = '2025-07-26'


def is_cyber_project(title):
    """判断项目标题是否属于网络安全相关"""
    if not title:
        return False
    for kw in CYBER_KEYWORDS:
        if kw.lower() in title.lower():
            return True
    return False


def main():
    with app.app_context():
        customers = Customer.query.order_by(Customer.id).all()
        total_customers = len(customers)
        total_imported = 0
        total_errors = 0

        print(f'🔍 对 {total_customers} 个客户逐一查询天眼查招投标')
        print(f'   过滤条件: 网络安全关键词({len(CYBER_KEYWORDS)}个) + 近一年(≥{CUTOFF_DATE})\n')

        for i, customer in enumerate(customers):
            name = customer.name
            print(f'[{i+1}/{total_customers}] {name[:25]}...', end=' ', flush=True)

            try:
                from tianyancha_api import fetch_bidding
                data = fetch_bidding(name)
            except Exception as e:
                print(f'❌ {str(e)[:40]}')
                total_errors += 1
                continue

            if isinstance(data, dict) and 'error' in data:
                msg = str(data.get('message', ''))[:50]
                print(f'⚠️ {msg}')
                total_errors += 1
                continue

            if not data:
                print('📭')
                continue

            # 过滤：仅网络安全关键词 + 近一年
            filtered = []
            for r in data:
                title = r.get('project_name', '')
                date = r.get('publish_date', '')
                if is_cyber_project(title) and date >= CUTOFF_DATE:
                    filtered.append(r)

            if not filtered:
                print(f'📭 ({len(data)}条但无关)')
                continue

            imported = 0
            for r in filtered:
                project_name = r.get('project_name', '')
                bidder_name = r.get('bidder_name', name)

                # 去重
                existing = BiddingRecord.query.filter_by(
                    project_name=project_name, bidder_name=bidder_name
                ).first()
                if existing:
                    continue

                record = BiddingRecord(
                    customer_id=customer.id,
                    project_name=project_name,
                    bidder_name=bidder_name,
                    winner_name=r.get('winner_name', ''),
                    bid_amount=r.get('bid_amount', 0),
                    publish_date=r.get('publish_date', ''),
                    product_detail=r.get('summary', '') or project_name,
                    source=f'天眼查(网络安全)',
                    source_url=r.get('bid_url', '') or r.get('source_url', ''),
                )
                db.session.add(record)
                imported += 1

            if imported > 0:
                db.session.commit()
                total_imported += imported
                print(f'✅ +{imported}条')
            else:
                print(f'📭 (已存在)')

            time.sleep(0.4)

        print(f'\n{"="*50}')
        print(f'🎯 网络安全招投标更新完成！')
        print(f'   查询客户: {total_customers} 个')
        print(f'   新增记录: {total_imported} 条')
        print(f'   出错: {total_errors} 个')
        print(f'   招投标总数: {BiddingRecord.query.count()}')
        print(f'{"="*50}')


if __name__ == '__main__':
    main()
