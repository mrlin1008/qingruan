"""
向长亭作战指挥平台导入湖南省轨道交通行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_rail_transit():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '中车株洲车辆有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '株洲', 'district': '荷塘区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车长江集团核心企业，国内铁路货车研发制造龙头。产品覆盖敞车、平车、罐车、漏斗车等全系列铁路货车，年新造能力超6000辆，出口30+国家。MES/PLM/ERP高度集成，智能产线工控安全与产品设计数据保护并重。',
            },
            {
                'name': '株洲联诚集团控股股份有限公司',
                'industry': '轨道交通', 'org_type': '民企', 'city': '株洲', 'district': '石峰区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '国内轨道交通装备关键零部件龙头，中车核心供应商。产品覆盖牵引电机冷却系统、油压减振器、结构件等300+品类。拥有株洲三个生产基地，ERP/PLM管理复杂产品BOM，供应链协同平台涉及大量客户交互，需信息安全整体方案。',
            },
            {
                'name': '湖南中车智行科技有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车株洲所旗下，智能轨道快运系统（ART）原创企业。全球首创虚拟轨道列车，已在株洲、宜宾、哈尔滨等城市商业运营。列车运行控制系统（TSCS）为核心IP，车地通信和调度平台均有高等级网络安全要求，是智慧城轨安全标杆。',
            },
            {
                'name': '湖南轨道交通控股集团有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省属大型国企，负责全省铁路、城际铁路、磁浮交通投融资建设运营。拥有铁路、磁浮、城际三大业务板块，管辖里程超3000公里。拥有调度指挥、票务清分、资产管理等核心信息系统，关系民生基础设施，关基保护和等保合规为刚需。',
            },
            {
                'name': '长沙市轨道交通集团有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '长沙地铁投资建设运营主体，已运营线路7条，在建线路5条，日均客流超200万人次。拥有综合监控（ISCS）、自动售检票（AFC）、信号（CBTC）、通信等核心系统。城市轨道交通作为关键信息基础设施，网络安全法要求三级等保和关基保护同步推进。',
            },
            {
                'name': '湖南中车通号技术有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车株洲所与中国通号合资，轨道交通信号系统专业企业。产品覆盖CBTC（地铁信号）、CTCS（高铁信号）、有轨电车信号等。信号系统安全完整性等级SIL4为最高安全标准，研发环境安全、代码保护和工控系统网络安全为生命线。',
            },
            {
                'name': '株洲九方装备股份有限公司',
                'industry': '轨道交通', 'org_type': '民企', 'city': '株洲', 'district': '石峰区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '中车株机主要配套商，轨道交通车辆零部件骨干企业。产品覆盖车体部件、转向架部件、电器屏柜等。拥有数控加工、焊接、装配等智能化产线。PLM/ERP系统管理复杂零部件数据，与中车等客户有大量设计协同，数据安全隔离和知识产权保护是关键。',
            },
            {
                'name': '长沙轨道交通运营有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '长沙轨道集团子公司，负责长沙地铁全部线路的运营管理。运营控制中心（OCC）7x24运行，管辖综合监控、票务、乘客信息、安防视频等20+运营系统。日均处理千万级交易数据，运营系统高可用和信息安全直接关系公共安全。',
            },
            {
                'name': '湖南城际铁路有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省城际铁路投建运营主体，运营长株潭城际铁路、长益常城际等线路。拥有城际铁路调度集中（CTC）、票务系统、旅客服务系统等。城际铁路既有国铁属性又有城市轨道特征，需兼顾铁路系统安全和城市轨道交通关基保护双重合规要求。',
            },
            {
                'name': '湖南中车弘辉科技有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '株洲', 'district': '天元区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '中车株洲所旗下，高铁/地铁减振降噪产品专业企业。产品覆盖轨道减振扣件、车轮降噪环、声屏障等。为中车和国内多条地铁线路供货。研发数据（声学仿真参数和材料配方）为核心IP，信息化系统建设中，安全管理从零起步窗口期。',
            },
            {
                'name': '株洲中车奇宏散热技术有限公司',
                'industry': '轨道交通', 'org_type': '合资', 'city': '株洲', 'district': '天元区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '中车株洲所与奇宏电子合资，轨道交通电力电子散热器专业企业。产品覆盖IGBT散热器、变流器散热系统等，是高铁和地铁牵引系统核心部件供应链关键环节。散热器翅片设计和热仿真数据为技术机密，知识产权保护需求突出。',
            },
            {
                'name': '湖南中车时代通信信号有限公司',
                'industry': '轨道交通', 'org_type': '国企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车时代电气（港股+A股）旗下，轨道交通信号系统集成商。业务覆盖城市轨道交通信号系统（CBTC）、干线铁路信号系统等。信号安全完整性（SIL4）认证要求极高的软件开发和测试环境安全，嵌入式系统安全和代码保护是核心竞争力保障。',
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

            # 轨道交通场景：工控安全 + 等保/关基 + 数据安全
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='CBTC/ISCS/SCADA等工控系统终端防护'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='城轨关基保护/信号系统SIL4安全合规'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='工程设计数据/信号代码/研发数据防泄漏'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 轨道交通客户导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_rail_transit()
