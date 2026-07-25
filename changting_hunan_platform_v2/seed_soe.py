"""
向长亭作战指挥平台导入湖南省属国资重点企业（跳过已存在的79家国企）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_soe():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '湖南兴湘投资控股集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属国有资本运营平台，是省委省政府深化国资国企改革的核心抓手。管理资产规模超千亿，控股参股博云新材、华升股份等上市公司。承担省属企业股权管理、国有资本运营等职能，财务投资系统和股权管理系统为关键信息资产，需满足国资监管安全合规。',
            },
            {
                'name': '湖南高新创业投资集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属国有创投平台，管理基金规模超500亿元。聚焦先进制造、新材料、新一代信息技术等领域投资，已投超300家企业，推动50+企业上市。投资管理系统、项目尽调数据库、LP信息披露平台等承载大量敏感商业数据，信息安全关乎基金声誉和合规底线。',
            },
            {
                'name': '湖南省港航水利集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属大型国企，整合全省港口、航道、水利资产。运营岳阳港、长沙港、常德港等主要港口，管理湘江、沅水等千吨级航道。港口TOS系统和船闸调度系统为关键基础设施，工控系统与调度平台面临APT和勒索攻击风险，关基保护为刚需。',
            },
            {
                'name': '湖南省机场管理集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属国企，运营管理长沙黄花国际机场及张家界、常德、永州、怀化等支线机场。长沙机场年旅客吞吐量超3000万。拥有航班信息系统（FIDS）、离港系统、行李系统、安防系统等民航核心IT系统，为民航局网络安全重点监管对象，需等保三级+民航合规。',
            },
            {
                'name': '湖南旅游集团有限责任公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '省属文旅产业投资运营平台，整合全省酒店、景区、旅行社等文旅资源。运营华天酒店集团、韶山旅游区等核心资产。拥有酒店管理PMS系统、景区票务系统、线上旅游平台等。支付卡数据PCI合规和客户个人信息保护为安全核心。',
            },
            {
                'name': '湖南湘投控股集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属大型投资控股集团，业务覆盖电力能源、新材料、生物医药、基金投资等板块。控股湘投金天钛金等多家企业。集团管控系统（财务、投资、HR、OA）承载全省国资重要数据，需满足等保合规和集团级网络安全管理。',
            },
            {
                'name': '湖南省煤业集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省属大型煤炭企业集团，下辖湘永、周源山、金竹山等多个煤矿。拥有煤矿安全监控系统、人员定位系统、瓦斯监测系统等工业安全信息系统。矿山六大系统为安全生产关键信息化设施，工控安全和持续运行保障直接关系矿工生命安全。',
            },
            {
                'name': '湖南粮食集团有限责任公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '开福区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省属粮油产业集团，保障全省粮食安全。运营长沙、岳阳、常德等大型粮库和粮油加工基地。粮食仓储智能化系统（粮情测控、智能通风、仓储管理）为粮食安全监管核心平台，工控系统和储备数据安全为国家战略级需求。',
            },
            {
                'name': '湖南省建筑设计院集团股份有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省建筑设计行业龙头，拥有建筑、规划、市政、勘察等甲级资质。年设计项目超2000个，BIM/CAD/PLM等设计系统管理海量工程数据。设计图纸和工程数据为知识产权核心资产，需协同设计环境下的数据安全和版权保护。',
            },
            {
                'name': '湖南湘科控股集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属军工集团，整合兵器、军需、民爆等国防工业资产。下属多个军品科研生产单位，产品覆盖轻武器、弹药、火工品等。涉密信息系统按国家秘密标准管理，军品研发数据和生产线工控安全为国家秘密级防护要求。',
            },
            {
                'name': '湘电集团有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '湘潭', 'district': '岳塘区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南装备制造骨干国企，产品覆盖大中型交直流电机、风力发电机、军工舰船电力推进系统等。军品+民品双线业务，军工舰船动力系统和装备研发数据涉密等级高。工控产线安全与涉密信息系统防护并重，需同时满足军工保密和网络安全合规。',
            },
            {
                'name': '长沙房产（集团）有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '长沙市属大型国有房地产集团（长房集团），开发项目超百个，物业管理面积超3000万㎡。拥有智慧社区管理平台、物业IoT系统、房产销售ERP等系统。管理超百万业主个人信息和房产交易数据，个人信息保护法合规和数据安全为监管重点。',
            },
            {
                'name': '湖南路桥建设集团有限责任公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南建投集团旗下，国内路桥施工领军企业。承建矮寨大桥、洞庭湖大桥等超级工程，业务遍布海内外。BIM/智慧工地/项目管理系统管理海量工程数据。海外项目多的特性使数据跨境传输安全和反商业间谍成为独特安全需求。',
            },
            {
                'name': '湖南省产权交易所有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省属国有产权交易平台，负责全省企业国有产权、行政事业单位资产、金融企业国有资产等交易。电子竞价和在线交易系统处理大宗国有产权交易，年交易额超百亿。交易系统安全直接影响国有资产保值增值，需最严格的交易安全和防操纵保护。',
            },
            {
                'name': '湖南国有资产经营管理有限公司',
                'industry': '国资', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '省属国资管理平台，负责省属"僵尸企业"出清、低效无效资产处置、国有企业退休人员社会化管理等。管理大量国企人员档案、资产台账、财务清算数据。清退企业数据迁移和档案电子化带来数据安全挑战，多企业数据汇聚后安全管控复杂度高。',
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

            # 国资场景：等保合规+数据安全+主机安全
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='集团管控/交易/调度等核心系统等级保护'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='国资数据/产权交易/投资决策数据防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='工控/涉密/交易系统终端安全防护'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 国资企业导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')
        print(f'   国企总数: {Customer.query.filter_by(org_type="国企").count()}')


if __name__ == '__main__':
    seed_soe()
