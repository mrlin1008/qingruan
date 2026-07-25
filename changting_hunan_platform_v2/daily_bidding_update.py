"""
每日招投标更新脚本 — 仅新增当天项目，不重复导入历史数据
用法: python3 daily_bidding_update.py
建议: 每天上午8:00通过cron自动执行
"""
import sys, os, time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, BiddingRecord

# 网络安全关键词（来自 网络安全相关.docx）
CYBER_KEYWORDS = [
    '商用密码应用安全性评估', '网络安全等级保护测评', '终端数据防泄漏系统',
    '特征库升级续保服务', '网络安全专项检查服务', '网络安全合规性检测',
    '安全设备续保与维护', '关键信息基础设施', '数据安全风险评估',
    '网络安全技术服务', '网络安全攻防演练', '网络安全能力验证',
    '网络安全保障服务', '网络安全运维服务', '网络安全设备续保',
    '工业互联网安全', '安全监测与防护', '工控网络防火墙',
    '等级保护测评', '漏洞扫描服务', '数据安全运营', '备份系统建设',
    '安全运营服务', '网络安全培训', '国产操作系统', '安全管理平台',
    '工控安全审计', '信创防火墙', '云平台建设', '数据库脱敏',
    '云平台扩容', '数据防泄漏', '云服务租赁', '云平台升级',
    '数据防泄密', '云基础设施', '备份一体机', '工控防火墙',
    '云资源租赁', '数据库审计', '国产化产品', '服务器采购',
    '云资源采购', '数据备份', '漏洞扫描', '风险评估',
    '工业网闸', '国产芯片', '入侵防御', '渗透测试',
    '主机安全', '数据安全', '容灾备份', '工控安全',
    '日志审计', '入侵检测', '运维审计', '等保测评',
    '安全探针', '云平台', '政务云', '堡垒机',
    '云底座', '云资源', '行业云', '云计算', '服务器',
    'WEB防火墙', '信创', '密评', '灾备', '蜜罐',
    '防火墙', 'WAF', 'waf', 'NGFW', 'SD-WAN', 'IDS', 'IPS', 'DLP',
    '路由器', '交换机',
]

# 湖南标识
HUNAN_MARKERS = [
    '湖南', '湘', '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德',
    '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '吉首', '浏阳',
    '宁乡', '望城', '醴陵', '湘乡', '耒阳', '武冈', '汨罗', '津市',
    '沅江', '资兴', '洪江', '冷水江', '涟源', '凤凰', '韶山', '星沙',
    '麓谷', '岳麓', '铁道',
]


def is_cyber(title):
    if not title:
        return False
    return any(kw.lower() in title.lower() for kw in CYBER_KEYWORDS)


def is_hunan(bidder, customers):
    if bidder in customers:
        return True
    for cn in customers:
        if len(cn) > 6 and cn in bidder:
            return True
    return any(m in bidder for m in HUNAN_MARKERS)


def matched_keywords(title):
    if not title:
        return ''
    return ','.join([kw for kw in CYBER_KEYWORDS if kw.lower() in title.lower()][:5])


def main():
    start_time = datetime.now()
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_update.log')

    def log(msg):
        print(msg)
        with open(log_file, 'a') as f:
            f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}\n')

    log(f'========== 每日招投标更新开始 ==========')
    log(f'日期: {start_time.strftime("%Y-%m-%d")}')

    with app.app_context():
        customers = Customer.query.order_by(Customer.id).all()
        customer_names = {c.name for c in customers}
        total = len(customers)

        # 已有项目哈希（用于快速去重）
        existing = set()
        for r in BiddingRecord.query.with_entities(
            BiddingRecord.project_name, BiddingRecord.bidder_name
        ).all():
            existing.add((r.project_name, r.bidder_name))

        imported = 0
        checked = 0
        errors = 0

        from tianyancha_api import fetch_bidding

        for customer in customers:
            name = customer.name
            try:
                data = fetch_bidding(name)
            except Exception as e:
                errors += 1
                continue

            if isinstance(data, dict) and 'error' in data:
                errors += 1
                continue
            if not data:
                continue

            checked += len(data)

            for r in data:
                title = r.get('project_name', '')
                bidder = r.get('bidder_name', '')
                date = r.get('publish_date', '')

                # 跳过已存在的
                if (title, bidder) in existing:
                    continue
                # 必须含网络安全关键词
                if not is_cyber(title):
                    continue
                # 必须湖南本地招标方
                if not is_hunan(bidder, customer_names):
                    continue

                db.session.add(BiddingRecord(
                    customer_id=customer.id,
                    project_name=title,
                    bidder_name=bidder,
                    winner_name=r.get('winner_name', ''),
                    bid_amount=r.get('bid_amount', 0),
                    publish_date=date,
                    product_detail=matched_keywords(title),
                    source='天眼查(每日更新)',
                    source_url=r.get('bid_url', '') or r.get('source_url', ''),
                ))
                existing.add((title, bidder))
                imported += 1

            time.sleep(0.3)  # API频率控制

        if imported > 0:
            db.session.commit()

        final_count = BiddingRecord.query.count()
        elapsed = (datetime.now() - start_time).total_seconds()
        log(f'查询客户: {total} | 检查项目: {checked} | 新增: {imported} | 出错: {errors}')
        log(f'耗时: {elapsed:.0f}秒 | 当前总数: {final_count}')
        log(f'========== 每日招投标更新结束 ==========\n')
        return imported


if __name__ == '__main__':
    main()
