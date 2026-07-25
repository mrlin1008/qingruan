"""
向长亭作战指挥平台导入湖南省新零售行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile, Opportunity, KeyPerson


def seed_retail():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '步步高商业连锁股份有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '湘潭', 'district': '雨湖区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南零售龙头，A股上市。拥有超市、百货、家电等多业态，门店超400家。2025年引入胖东来模式调改门店，数字化改造加速。信息系统涵盖ERP、POS、会员系统、线上商城、供应链管理等，安全合规需求突出。',
            },
            {
                'name': '湖南友谊阿波罗商业股份有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市百货集团（友阿股份），旗下友谊商店、阿波罗商业广场等10余家大型百货购物中心。近年转型跨境电商、奥莱、社区生活中心等新业态，线上有友阿微商城，年营收超百亿。',
            },
            {
                'name': '湖南兴盛优选电子商务有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '全国社区电商头部平台，注册用户超1亿，覆盖17个省份。日订单超1200万，年GMV超400亿。拥有自建物流仓配体系，核心系统包括交易平台、物流调度、支付结算、大数据分析等，数据安全和系统稳定性至关重要。',
            },
            {
                'name': '水羊集团股份有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市美妆电商集团（原御泥坊），旗下拥有御泥坊、小迷糊、大水滴等品牌。自主开发电商中台系统、智能仓储、数据中台，日处理订单超10万，深度依赖线上交易系统和用户数据安全。',
            },
            {
                'name': '湖南零食很忙商业连锁有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '全国最大零食连锁品牌之一，与赵一鸣零食合并后门店超13000家，年营收超200亿。拥有自主研发的智能补货系统、会员系统、供应链管理平台、加盟商管理系统。线下门店数字化和线上会员运营要求高可用IT基础设施。',
            },
            {
                'name': '湖南茶悦文化产业发展集团有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '茶颜悦色母公司，全国知名新式茶饮品牌。门店超800家，拥有自主开发的小程序点单系统、会员系统、供应链平台。线上交易占比超70%，日均交易量巨大，系统安全与数据保护是核心关注点。',
            },
            {
                'name': '湖南文和友文化产业发展集团有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '超级网红文化餐饮综合体，长沙海信广场店年客流量超千万，年营收超10亿。深圳、广州等城市布局。拥有自主研发的排队叫号、智能收银、会员营销系统。品牌IP价值高，数字化运营要求强，需防黑客攻击和恶意抢号等安全威胁。',
            },
            {
                'name': '湖南梦洁家纺股份有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市家纺龙头，全国门店超3000家。线上天猫、京东、抖音等全渠道布局，自建电商运营中台。拥有ERP、WMS、CRM等核心系统，线上线下融合的全渠道零售模式要求高水平信息安全保障。',
            },
            {
                'name': '湖南颐而康保健连锁股份有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '全国知名健康养生连锁品牌，门店超100家，年服务超500万人次。拥有自主研发的预约管理系统、会员管理平台、智能排班系统。数字化运营和会员隐私保护是核心安全需求。',
            },
            {
                'name': '费大厨餐饮管理有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湘菜连锁头部品牌，"辣椒炒肉"品类开创者，全国门店超200家。拥有自研点餐系统、供应链管理、会员系统、外卖聚合平台。门店快速扩张期IT系统建设需求旺盛，需满足餐饮行业数据合规要求。',
            },
            {
                'name': '湖南墨茉点心局食品有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '天心区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '新中式烘焙连锁品牌，全国门店超100家。线上小程序交易占比高，会员体系完善。拥有数字化门店管理系统、中央厨房ERP、线上商城。快速扩张中急需规范IT安全体系。',
            },
            {
                'name': '湖南黑色经典食品有限公司',
                'industry': '新零售', 'org_type': '民企', 'city': '长沙', 'district': '天心区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南特产零食连锁头部品牌，全国门店超500家。拥有加盟管理系统、供应链平台、线上商城。线下门店POS系统和线上交易系统的安全稳定是核心IT需求。',
            },
        ]

        added = 0
        for c in customers:
            if c['name'] in existing_names:
                print(f'  跳过（已存在）: {c["name"]}')
                continue
            customer = Customer(**c)
            db.session.add(customer)
            db.session.flush()

            # 添加默认安全画像 — 电商/零售场景优先关注WAF、数据安全、安全运营
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='WAF',
                                gap_analysis='机会', notes='线上商城/小程序Web防护需求'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='会员数据与交易数据保护'),
                SecurityProfile(customer_id=customer.id, product_category='安全运营',
                                gap_analysis='机会', notes='多门店/多渠道IT安全运维需求'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 新零售客户导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_retail()
