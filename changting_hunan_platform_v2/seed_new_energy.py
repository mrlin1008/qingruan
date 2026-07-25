"""
向长亭作战指挥平台导入湖南省新能源行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_new_energy():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '巴斯夫杉杉电池材料有限公司',
                'industry': '新能源', 'org_type': '合资', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '德国巴斯夫与杉杉股份合资企业，全球领先的锂电正极材料供应商。长沙基地产能超10万吨/年，服务宁德时代、比亚迪等头部客户。拥有MOM/MES等智能制造系统，OT与IT融合度高，工控安全需求突出。',
            },
            {
                'name': '湖南长远锂科股份有限公司',
                'industry': '新能源', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市（五矿集团控股），锂电池正极材料龙头。产品覆盖三元正极、磷酸铁锂、钴酸锂等，年产超10万吨。MES/ERP/IoT系统深度集成，工艺配方数据为核心IP，工控安全和数据防泄漏为关键需求。',
            },
            {
                'name': '湖南科力远新能源股份有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，中国镍氢动力电池龙头，混合动力汽车电池系统头部供应商。业务覆盖电池、混动总成、储能系统。拥有自动化产线控制系统、电池管理平台（BMS）等核心系统，需保障产线连续性和数据安全。',
            },
            {
                'name': '华自科技股份有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，智慧能源与环保自动化龙头。业务覆盖储能系统、充电桩、智能配电网、光伏电站。拥有自主SCADA系统、储能EMS平台和充电运营管理平台。能源IoT设备量大面广，网络安全和平台安全为刚需。',
            },
            {
                'name': '湖南红太阳光电科技有限公司',
                'industry': '新能源', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国电子科技集团（CETC）旗下，国内光伏装备龙头。产品覆盖太阳能电池生产线整线设备、光伏组件、储能系统等。拥有自动化设备控制、产线MES等系统，半导体级洁净厂房智能制造，产权保护和工控安全为核心关注点。',
            },
            {
                'name': '湖南德赛电池有限公司',
                'industry': '新能源', 'org_type': '国企', 'city': '长沙', 'district': '望城区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '德赛集团旗下储能电池基地，总投资100亿元建设20GWh储能电芯项目。聚焦电力储能、工商业储能、户用储能产品。产线高度自动化，MES/WMS/ERP系统全覆盖，是新兴智造标杆，信息安全体系正加速建设中。',
            },
            {
                'name': '湖南立方新能源科技有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '株洲', 'district': '天元区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '专注于聚合物锂离子电池和固态电池研发制造，拥有株洲高新区智能工厂。产品覆盖3C数码、智能穿戴、电动工具等领域。固态电池为前瞻技术方向，研发数据保护和智能制造系统安全是重点需求。',
            },
            {
                'name': '桑顿新能源科技有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '湘潭', 'district': '雨湖区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '锂电池全产业链企业，覆盖正极材料、电芯、电池包及回收。拥有湘潭和长沙两大生产基地，储能产品出货量行业前列。产线数字化程度高，MES系统与设备控制深度融合，需统筹考虑IT与OT安全体系建设。',
            },
            {
                'name': '威胜集团有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '威胜控股（港股上市）核心子公司，中国智能电表领军企业。产品覆盖智能电表、水表、气表、能源管理平台、充电桩等。自建AMI（智能计量）云平台管理千万级终端设备，IoT安全和云平台安全是核心关基需求。',
            },
            {
                'name': '湖南三一智慧新能源有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '三一集团旗下新能源业务平台，覆盖风电装备、光伏、储能、制氢等领域。依托三一智能制造能力快速扩张，风电吊装量全国前列。新能源电站远程监控、设备预测维护等工业互联网应用需高水平安全防护。',
            },
            {
                'name': '湖南海利锂电科技有限公司',
                'industry': '新能源', 'org_type': '国企', 'city': '长沙', 'district': '望城区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南海利集团旗下锂电材料企业，主产磷酸铁锂正极材料，年产能3万吨。已建成智能化生产线，部署DCS/MES系统实现自动化生产。化工+新能源双重属性，需满足危化行业工控安全合规要求。',
            },
            {
                'name': '湖南时代联合新能源有限公司',
                'industry': '新能源', 'org_type': '民企', 'city': '邵阳', 'district': '双清区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '专注于大圆柱锂电池研发制造，产品覆盖两轮车、低速车、储能等领域。邵阳生产基地投产多条自动化产线，信息化系统处于建设期。新能源制造业在快速扩张阶段，IT基础架构和网络安全正从零规划，介入时机好。',
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

            # 新能源制造场景：工控安全 + 数据安全 + WAF
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='产线工控终端/MES服务器安全防护'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='工艺配方/研发数据防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='WAF',
                                gap_analysis='机会', notes='能源管理平台/充电运营平台Web防护'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 新能源客户导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_new_energy()
