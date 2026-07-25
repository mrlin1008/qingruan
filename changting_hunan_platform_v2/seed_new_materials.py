"""
向长亭作战指挥平台导入湖南省新材料行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_new_materials():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '湖南金博碳素股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '益阳', 'district': '赫山区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，科创板碳基复合材料第一股。光伏热场碳/碳复合材料全球龙头，市占率超40%。产品延伸至半导体热场、刹车盘等领域。拥有自研CVD沉积工艺产线，工艺参数为核心IP，工控安全和研发数据保护至关重要。',
            },
            {
                'name': '湖南博云新材料股份有限公司',
                'industry': '新材料', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，中南大学背景。国内粉末冶金复合材料龙头，产品覆盖航空刹车副、航天用碳/碳复合材料、高性能硬质合金等。军品+民品双线业务，涉密信息系统与产线工控安全并重，需满足军工保密和等保合规要求。',
            },
            {
                'name': '湖南湘投金天钛金属股份有限公司',
                'industry': '新材料', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南湘投控股集团旗下，国内高端钛合金材料领军企业。产品广泛应用于航空发动机、舰船、核电、化工等领域。拥有钛带卷、钛焊管、钛棒材等核心产线，军工配套资质齐全，涉密产线工控安全和研发数据安全等级高。',
            },
            {
                'name': '湖南中科星城石墨有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '宁乡市',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中科电气（A股）全资子公司，国内锂电池负极材料头部企业。年产负极材料超10万吨，服务宁德时代、比亚迪、SK等全球头部电池厂。MES/IoT系统贯穿全产线，石墨化工艺参数高度机密，需工控安全和数据防泄漏综合治理。',
            },
            {
                'name': '湖南松井新材料股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '宁乡市',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市（科创板），新型功能涂层材料龙头。产品覆盖消费电子涂料、汽车涂料、特种油墨等。客户涵盖华为、苹果、小米、比亚迪等，配方和工艺数据是核心IP。MES与ERP深度集成，配方数据防泄漏为第一优先级。',
            },
            {
                'name': '长沙岱勒新材料科技股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': 'A股上市，国内金刚石线龙头。产品用于光伏硅片切割、蓝宝石切割、磁材切割等领域。年产金刚石线超3000万公里。智能制造程度高，产线数字化管理系统与设备控制层融合度高，工控安全需求日益突出。',
            },
            {
                'name': '湖南航天环宇通信科技股份有限公司',
                'industry': '新材料', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市（科创板），航天科工集团旗下。主营航空航天复合材料及精密零部件，覆盖卫星、导弹、大飞机等高端装备。军品业务涉密等级高，研发设计数据（CAD/CAE/PLM）为核心资产，军工合规和信息安全要求极为严格。',
            },
            {
                'name': '湖南华曙高科技股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市（科创板），工业级3D打印龙头。全球少数掌握SLS（选择性激光烧结）全技术链的企业，设备出口欧美。产品覆盖高分子粉末材料、金属粉末材料和3D打印设备。核心技术参数和材料配方为全球竞争力基础，信息安全关乎企业命脉。',
            },
            {
                'name': '湖南宇新能源科技股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，轻烃综合利用与化工新材料企业。产品覆盖异辛烷、甲基叔丁基醚、顺酐、BDO及下游可降解材料等。拥有大型化工装置DCS/SIS控制系统，需满足危化行业工控安全等级保护和应急管理部安全合规要求。',
            },
            {
                'name': '湖南湘江涂料集团有限公司',
                'industry': '新材料', 'org_type': '国企', 'city': '长沙', 'district': '望城区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '中国涂料工业十强，湖南最大涂料企业。产品覆盖汽车涂料、工业涂料、建筑涂料、树脂等。拥有自动化调色和灌装产线，ERP/WMS系统管理。涂料配方为核心无形资产，配方管理系统和产线控制系统的安全隔离是关键。',
            },
            {
                'name': '湖南方恒新材料技术股份有限公司',
                'industry': '新材料', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '专注于金属动态复合材料研发制造，产品应用于核电、LNG、航空航天、新能源汽车等高端领域。拥有多项国际PCT专利，技术壁垒高。研发管理系统和专利数据库为核心资产，需数据安全和知识产权保护整体方案。',
            },
            {
                'name': '时代华鑫新材料技术有限公司',
                'industry': '新材料', 'org_type': '国企', 'city': '株洲', 'district': '天元区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车株洲所旗下，国内最大的高性能聚酰亚胺薄膜（PI膜）供应商。产品应用于5G通信、柔性显示、高铁牵引电机绝缘、航空航天等领域。打破杜邦全球垄断，属战略性新材料。工艺参数为国家级核心技术秘密，安全防护等级最高。',
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

            # 新材料场景：研发数据保护 + 工控安全 + 等保合规
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='配方/工艺参数/研发数据防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='MES/DCS/SCADA等工控系统终端防护'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='军工/危化合规要求的等级保护测评'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 新材料客户导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_new_materials()
