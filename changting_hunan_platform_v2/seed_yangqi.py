"""
向长亭作战指挥平台导入在湖南省的央企重点客户（跳过已存在的31家）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_yangqi():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '中国南方航空股份有限公司湖南分公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '南航在湘运力基地，长沙黄花机场最大基地航司。执管A320/B737机队，航线覆盖全国及东南亚。拥有航班运行控制（AOC）、飞行管理、机务维修信息系统等航司核心系统。民航关键信息基础设施，需等保三级+民航网络安全监管双重合规。',
            },
            {
                'name': '中国兵器装备集团长沙机电产品研究开发中心',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国兵器装备集团在湘军品研发机构，承担特种装备和光电产品研发任务。涉密信息系统按国军标安全保密要求建设，军品研发数据和产品设计图纸按国家秘密管理。涉密网络与工业控制网络的物理隔离和防泄密为核心安全要求。',
            },
            {
                'name': '中冶长天国际工程有限责任公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国五矿/中冶集团旗下，中国冶金铁前工程领域龙头。承担国内外数百项大型烧结、球团、选矿工程项目，市场占有率全国第一。拥有工程设计PLM/BIM系统和项目管理系统，工程设计和工艺数据为国际竞争力核心，知识产权保护与数据防泄漏需求突出。',
            },
            {
                'name': '中国航发中传机械有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '望城区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国航发集团旗下精密齿轮和传动系统专业企业，是国内航空发动机齿轮箱和直升机传动系统的核心研制单位。为C919、涡扇-XX等国家重点型号配套。军品+民品双线业务，涉密等级高，研发设计和生产线工控系统为国家秘密级保护对象。',
            },
            {
                'name': '中国航发湖南动力机械研究所',
                'industry': '央企', 'org_type': '国企', 'city': '株洲', 'district': '芦淞区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国航发集团直属发动机科研院所，中小型航空发动机的"国家队"。承担涡轴、涡桨、涡扇等发动机的预先研究和型号研制任务。拥有超算仿真、试车数据管理、协同设计等核心科研IT系统。发动机仿真数据和飞行试车数据为国家核心军事机密，需最高等级安全防护。',
            },
            {
                'name': '中国华能集团有限公司湖南分公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '华能集团（五大发电之一）在湘区域公司，运营岳阳、华容等火电厂及多个风电场、光伏电站。拥有DCS/SCADA发电控制系统和电力监控系统（EMS）。电力监控系统为关键信息基础设施，需满足发改委14号令电力监控系统安全防护和等保三级要求。',
            },
            {
                'name': '中国华电集团有限公司湖南分公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '华电集团（五大发电之一）在湘区域公司，运营常德、湘潭、永州等火电及新能源资产。发电厂SIS/DCS/SCADA系统为电力工控核心，新能源智慧运维平台管理分布式场站。电力工控安全和远程运维安全需满足发改委14号令和能源局工控安全合规。',
            },
            {
                'name': '国家能源集团湖南电力有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '国家能源集团（全球最大发电企业）在湘区域公司。运营宝庆、益阳等火电厂及大量风电光伏新能源资产，火电装机超400万kW。智慧电厂和新能源区域集控中心为数字化转型核心，电力工控系统安全和远程集控通信安全直接关系电网安全。',
            },
            {
                'name': '中国长江三峡集团有限公司湖南分公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '三峡集团在湘区域公司，负责湖南省长江大保护、清洁能源开发等业务。运营多个污水处理、水环境治理项目及新能源电站。SCADA远程监控系统管理遍布全省的环保设施和新能源资产，工控系统与集团总部网络互联，边界安全和远程运维安全为管控重点。',
            },
            {
                'name': '中国核工业集团湖南新华水电有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中核集团在湘水电及新能源投资运营平台，运营多个水电站和新能源场站。水电厂计算机监控系统和大坝安全监测系统为电站运行核心。水电工控系统与电网调度数据网互联，电力工控安全和调度数据安全为合规红线。',
            },
            {
                'name': '中国建筑材料集团有限公司湖南西南水泥',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '中国建材集团旗下，在湖南运营多条新型干法水泥生产线。拥DCS生产过程控制系统和ERP企业管理系统。水泥产线自动化和工业控制系统全面管控生产，工控安全和环保监测数据安全为企业运营管理基础保障。',
            },
            {
                'name': '中国广核集团湖南分公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中广核集团在湘区域公司，开发和运营多个风电、光伏、储能项目。新能源智慧运维平台为集团"一总部多基地"运维模式的重要节点。风电和光伏场站地域分散、无人值守，远程集控网络安全和场站边缘安全是新能源网络安全核心挑战。',
            },
            {
                'name': '中国黄金集团湖南矿业有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '中国黄金集团在湘矿山企业，运营大万、平江等多个黄金矿山。矿山六大安全系统（监测监控、人员定位、紧急避险、压风自救、供水施救、通信联络）为安全生产信息化基础。矿山工控与安全监控系统直接关系矿工生命安全，需高可用和安全防护一体化保障。',
            },
            {
                'name': '中粮集团湖南有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '长沙', 'district': '开福区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中粮集团在湘业务平台，涵盖粮油加工、仓储物流、品牌食品等。运营长沙、岳阳等大型粮油加工和仓储基地。仓储智能化系统（粮情测控、智能出入库）和供应链管理平台为运营核心。储备粮数据安全和食品追溯系统安全为国家粮食安全战略组成部分。',
            },
            {
                'name': '中国航发湖南南方宇航工业有限公司',
                'industry': '央企', 'org_type': '国企', 'city': '株洲', 'district': '芦淞区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国航发集团旗下航空发动机零部件和微型燃机研制企业。产品覆盖航空传动系统、减速器等关键部件，为国产军民用发动机配套。军品科研生产涉密等级高，精密加工工艺参数和产品设计数据为国家秘密级保护对象，需军工资质下的高安全保障。',
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

            # 央企场景：关基+等保+工控安全
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='核心生产/调度/科研系统等级保护与关基合规'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='军工涉密/电力工控/民航系统终端安全防护'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='军品研发数据/发电调度数据/民航运营数据防泄漏'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 央企导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')
        print(f'   国企总数: {Customer.query.filter_by(org_type="国企").count()}')


if __name__ == '__main__':
    seed_yangqi()
