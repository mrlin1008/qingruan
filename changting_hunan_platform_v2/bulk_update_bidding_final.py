"""
最终版：按424个客户逐一查询天眼查 —> 网络安全关键词过滤 —> 近一年 —> 湖南本地
关键词来源：网络安全相关.docx（99个）
"""
import sys, os, time, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, BiddingRecord

# 从 网络安全相关.docx 提取的99个网络安全关键词
CYBER_KEYWORDS = [
    '商用密码应用安全性评估', '网络安全等级保护测评', '网络安全攻防技术专项服务',
    '终端数据防泄漏系统', '特征库升级续保服务', '网络安全专项检查服务',
    '网络安全合规性检测', '安全设备续保与维护', '网络安全咨询服务',
    '关键信息基础设施', '数据安全风险评估', '网络安全技术服务',
    '网络安全攻防演练', '网络安全竞赛系统', '网络安全能力验证',
    '网络安全保障服务', '网络安全运维服务', '网络安全设备续保',
    '工业互联网安全', '光网络管理系统', '安全监测与防护',
    '产品兼容性证书', '工控网络防火墙', '等级保护测评',
    '漏洞扫描服务', '数据安全运营', '备份系统建设',
    '安全运营服务', '网络安全培训', '国产操作系统',
    '安全管理平台', '工控安全审计', '信创防火墙',
    '云平台建设', '数据库脱敏', '云平台扩容',
    '数据防泄漏', '云服务租赁', '云平台升级',
    '数据防泄密', '云基础设施', '备份一体机',
    '工控防火墙', '云资源租赁', '数据库审计',
    '国产化产品', '服务器采购', '云资源采购',
    '数据备份', '数据存储', '漏洞扫描',
    '风险评估', '云资源池', '工业网闸',
    '国产芯片', '入侵防御', '渗透测试',
    '主机安全', '数据安全', '容灾备份',
    '工控安全', '日志审计', '存储扩容',
    '存储备份', '入侵检测', '攻击团队',
    '运维审计', '等保测评', '数据容灾',
    '安全探针', '云服务', '云平台',
    '政务云', '路由器', '堡垒机',
    '混合云', '云底座', '云资源',
    '行业云', '私有云', '公有云',
    '交换机', '云计算', '服务器',
    '信创', 'WEB防火墙', 'WAF', 'waf',
    'NGFW', 'SD-WAN', 'IDS', 'IPS', 'DLP',
    '蜜罐', '密评', '灾备', 'BRAS设备',
    '防火墙',
]

# 日期：近一年
CUTOFF = '2025-07-26'

# 湖南标识
HUNAN_MARKERS = [
    '湖南', '湘', '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德',
    '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '吉首', '浏阳',
    '宁乡', '望城', '醴陵', '湘乡', '耒阳', '武冈', '汨罗', '津市',
    '沅江', '资兴', '洪江', '冷水江', '涟源', '凤凰', '韶山', '星沙',
    '麓谷', '岳麓', '铁道',
]


def matched_keywords(title):
    """返回项目名称中命中的所有关键词"""
    if not title:
        return ''
    matched = [kw for kw in CYBER_KEYWORDS if kw.lower() in title.lower()]
    return ','.join(matched[:5])


def is_cyber(title):
    if not title:
        return False
    return any(kw.lower() in title.lower() for kw in CYBER_KEYWORDS)


def is_hunan(bidder, customers):
    if bidder in customers:
        return True
    for cn in customers:
        if cn in bidder and len(cn) > 6:
            return True
    return any(m in bidder for m in HUNAN_MARKERS)


def main():
    with app.app_context():
        customers = Customer.query.order_by(Customer.id).all()
        customer_names = {c.name for c in customers}
        total = len(customers)
        imported = 0
        no_bidding = 0
        no_match = 0
        errors = 0

        print(f'🔍 对 {total} 个客户逐一查询天眼查')
        print(f'   过滤: {len(CYBER_KEYWORDS)}个网络安全关键词 | 近一年(≥{CUTOFF}) | 仅湖南招标方\n')

        from tianyancha_api import fetch_bidding

        for i, customer in enumerate(customers):
            name = customer.name
            print(f'[{i+1}/{total}] {name[:30]}...', end=' ', flush=True)

            try:
                data = fetch_bidding(name)
            except Exception as e:
                print(f'❌ {str(e)[:30]}')
                errors += 1
                continue

            if isinstance(data, dict) and 'error' in data:
                print(f'⚠️ {str(data.get("message",""))[:40]}')
                errors += 1
                continue

            if not data:
                print('📭 无招标数据')
                no_bidding += 1
                continue

            # 过滤：近一年 + 含网络安全关键词 + 湖南招标方
            matched = []
            for r in data:
                title = r.get('project_name', '')
                date = r.get('publish_date', '')
                bidder = r.get('bidder_name', '')
                if date >= CUTOFF and is_cyber(title) and is_hunan(bidder, customer_names):
                    matched.append(r)

            if not matched:
                cyber_count = sum(1 for r in data if is_cyber(r.get('project_name', '')))
                year_count = sum(1 for r in data if r.get('publish_date', '') >= CUTOFF)
                hunan_count = sum(1 for r in data if is_hunan(r.get('bidder_name', ''), customer_names))
                print(f'📭 共{len(data)}条(近一年{year_count}/关键词{cyber_count}/湖南{hunan_count}=0交集)')
                no_match += 1
                continue

            added = 0
            for r in matched:
                pn = r.get('project_name', '')
                bn = r.get('bidder_name', name)
                if BiddingRecord.query.filter_by(project_name=pn, bidder_name=bn).first():
                    continue
                db.session.add(BiddingRecord(
                    customer_id=customer.id,
                    project_name=pn,
                    bidder_name=bn,
                    winner_name=r.get('winner_name', ''),
                    bid_amount=r.get('bid_amount', 0),
                    publish_date=r.get('publish_date', ''),
                    product_detail=matched_keywords(pn),
                    source='天眼查',
                    source_url=r.get('bid_url', '') or r.get('source_url', ''),
                ))
                added += 1

            if added:
                db.session.commit()
                imported += added
                print(f'✅ +{added}条 | 命中:{matched_keywords(matched[0]["project_name"])[:50]}')
            else:
                print('📭 已存在')
                no_match += 1

            time.sleep(0.4)

        print(f'\n{"="*60}')
        print(f'🎯 招投标更新完成！')
        print(f'   总客户: {total} | 新增记录: {imported} | 无招标: {no_bidding}')
        print(f'   无关/已存在: {no_match} | 出错: {errors}')
        print(f'   当前招投标总数: {BiddingRecord.query.count()}')
        print(f'{"="*60}')


if __name__ == '__main__':
    main()
