"""
按网络安全关键词在天眼查搜索招投标，匹配现有客户并导入
关键词来源于：网络安全相关.docx
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, BiddingRecord
from tianyancha_api import search_bids_cross, _run_tyc


# 从docx中提取的网络安全核心搜索关键词（去重、去逗号变体）
KEYWORDS = [
    # 安全产品类
    '防火墙', 'WEB防火墙', 'WAF', '入侵防御', 'IPS', '入侵检测', 'IDS',
    '堡垒机', '运维审计', '日志审计', '数据库审计', '漏洞扫描',
    '主机安全', '蜜罐', 'SD-WAN', '安全管理平台', '安全探针',
    # 国产化类
    '国产芯片', '国产操作系统', '国产化产品',
    # 安全服务类
    '网络安全运维', '安全运营服务', '安全监测与防护', '网络安全技术服务',
    '渗透测试', '风险评估', '网络安全能力验证',
    # 合规类
    '等级保护测评', '等保测评', '商用密码应用安全性评估', '密评',
    '网络安全合规性检测', '关键信息基础设施',
    # 攻防类
    '网络安全攻防演练', '网络安全竞赛', '网络安全培训',
    # 数据安全类
    '数据防泄漏', 'DLP', '数据库脱敏', '数据安全运营', '数据安全风险评估',
    # 工控安全类
    '工控防火墙', '工业网闸', '工控安全审计', '工控安全', '工业互联网安全',
    # 灾备类
    '容灾备份', '灾备', '备份一体机', '数据备份',
    # 云服务类
    '政务云', '云服务', '云平台建设', '云基础设施',
    # 服务器类
    '服务器采购', '服务器设备',
]


def main():
    with app.app_context():
        customers = {c.name: c.id for c in Customer.query.all()}
        total_imported = 0
        total_errors = 0

        print(f'🔍 用 {len(KEYWORDS)} 个网络安全关键词搜索天眼查招投标...')
        print(f'   目标匹配客户: {len(customers)} 个\n')

        for i, kw in enumerate(KEYWORDS):
            print(f'[{i+1}/{len(KEYWORDS)}] 搜索: "{kw}" ...', end=' ', flush=True)

            try:
                results = search_bids_cross(kw)
            except Exception as e:
                print(f'❌ 异常: {e}')
                total_errors += 1
                continue

            if isinstance(results, dict) and 'error' in results:
                msg = results.get('message', str(results))
                print(f'⚠️ {msg[:60]}')
                total_errors += 1
                if '频率' in msg or '限流' in msg or 'too many' in msg.lower():
                    time.sleep(10)
                continue

            if not results:
                print('📭 无结果')
                continue

            imported = 0
            for r in results:
                bidder = r.get('bidder_name', '')
                if not bidder:
                    continue

                # 匹配客户（招标方名称匹配）
                matched_cid = None
                for cname, cid in customers.items():
                    if cname in bidder or bidder in cname:
                        matched_cid = cid
                        break

                project_name = r.get('project_name', '')
                if not project_name:
                    continue

                # 去重检查
                existing = BiddingRecord.query.filter_by(
                    project_name=project_name,
                    bidder_name=bidder,
                ).first()
                if existing:
                    continue

                record = BiddingRecord(
                    customer_id=matched_cid,
                    project_name=project_name,
                    bidder_name=bidder,
                    winner_name=r.get('winner_name', ''),
                    bid_amount=r.get('bid_amount', 0),
                    publish_date=r.get('publish_date', ''),
                    product_detail=r.get('summary', '') or project_name,
                    source=f'天眼查(按关键词:{kw})',
                    source_url=r.get('source_url', '') or r.get('bid_url', ''),
                )
                db.session.add(record)
                imported += 1

            if imported > 0:
                db.session.commit()
                total_imported += imported
                print(f'✅ +{imported}条')
            else:
                print('📭 无新记录')

            time.sleep(0.8)  # 控制频率

        print(f'\n{"="*50}')
        print(f'🎯 网络安全招投标更新完成！')
        print(f'   搜索关键词: {len(KEYWORDS)} 个')
        print(f'   新增记录: {total_imported} 条')
        print(f'   出错: {total_errors} 个')
        print(f'   当前招投标总数: {BiddingRecord.query.count()}')
        print(f'{"="*50}')


if __name__ == '__main__':
    main()
