"""
向长亭作战指挥平台导入湖南省生物制药行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_biopharma():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '圣湘生物科技股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股科创板上市，国内分子诊断龙头。新冠期间核酸检测产品出口160+国家，营收破百亿。拥有全自动核酸提取、PCR检测、NGS测序等核心平台。LIMS/MES系统贯穿研发生产全流程，基因数据和患者隐私保护为合规刚需。',
            },
            {
                'name': '三诺生物传感股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，中国血糖监测第一品牌，全球第四。产品覆盖血糖仪、CGM持续葡萄糖监测系统、尿酸检测等，用户超2000万。健康大数据平台管理海量患者血糖数据，隐私保护和数据安全是FDA/CE/NMPA合规核心要求。',
            },
            {
                'name': '湖南方盛制药股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，覆盖中成药、化药、生物药的综合性药企。拥有10个GMP生产基地，产品线覆盖心脑血管、骨伤科、儿科等领域。ERP/LIMS/QMS系统全面部署，药品生产数据完整性（DI）是GMP/FDA审计重点，工控安全为合规必备。',
            },
            {
                'name': '湖南九典制药股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，化药制剂与原料药一体化企业。核心产品洛索洛芬钠凝胶贴膏年销超20亿，是国内经皮给药领域标杆。拥有原料药+制剂全产业链，DCS/MES/ERP系统覆盖从合成到包装全流程，药品追溯和CSV计算机化系统验证是合规重点。',
            },
            {
                'name': '湖南尔康制药股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'A股上市，国内药用辅料行业龙头。产品覆盖药用辅料、原料药、成品药三大板块，辅料品种超200个。拥有多个GMP智能化生产基地，供应链管理系统管理上千种物料。药品供应链安全和生产数据完整性为核心监管合规需求。',
            },
            {
                'name': '湖南华纳大药厂股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '大型', 'it_budget_level': '中等',
                'description': 'A股上市，专注于消化、呼吸、抗感染等治疗领域的化药企业。拥有浏阳和望城两大生产基地，多条通过GMP认证的智能化生产线。MES系统与ERP集成，药品生产批次记录电子化，需满足数据完整性和计算机化系统验证（CSV）要求。',
            },
            {
                'name': '湖南汉森制药股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '益阳', 'district': '赫山区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': 'A股上市，中成药企业。核心产品四磨汤口服液为中药保护品种，年销售额稳定在10亿级。拥有益阳GMP生产基地，自动化提取和灌装产线。ERP/SCADA系统管理生产全流程，工艺配方为核心IP，数据防泄漏为关键安全需求。',
            },
            {
                'name': '湖南南岳生物制药有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '衡阳', 'district': '雁峰区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省唯一血液制品企业，国内少数拥有单采血浆站网络和血液制品生产资质的企业。产品覆盖人血白蛋白、静注人免疫球蛋白、凝血因子等。浆站信息系统（BMIS）与生产MES/LIMS高度集成，血液制品全链条追溯和生物安全数据保护级别极高。',
            },
            {
                'name': '湖南斯奇生物制药有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '九芝堂集团旗下生物药企业，专注于基因工程药物研发生产。核心产品斯奇康（卡介菌多糖核酸注射液）为免疫调节剂。拥有通过GMP认证的生物发酵和纯化产线，生物反应器控制系统（DCS）为核心工控资产，生物制药工艺参数和数据安全保护为合规底线。',
            },
            {
                'name': '湖南天劲制药有限责任公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '中成药企业，主打筋骨康系列产品。拥有GMP标准化生产基地，自动化提取、浓缩、制剂产线。生产信息化系统正在升级建设中，IT基础架构和网络安全正处于规划窗口期，介入时机好，可从零建立安全体系。',
            },
            {
                'name': '湖南春光九汇现代中药有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '国内中药配方颗粒行业前列企业，拥有超微粉碎、动态逆流提取等核心技术。中药配方颗粒纳入医保后市场快速放量。自动化和信息化产线扩建中。配方颗粒生产工艺为商业机密，研发数据和MES系统需要建立全面安全防护体系。',
            },
            {
                'name': '湖南明康中锦医疗科技股份有限公司',
                'industry': '生物制药', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '国内呼吸医疗器械领军企业，产品覆盖高流量无创呼吸湿化治疗仪、医用压缩式雾化器等。产品获NMPA、CE、FDA认证，出口多国。医疗器械注册文档和研发数据为核心IP，需满足医疗器械行业数据完整性合规要求。',
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

            # 生物制药场景：数据完整性合规 + 工控安全 + 等保
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='GMP产线工控终端/DCS/MES服务器防护'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='药品研发数据/临床数据/工艺配方防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='药企核心信息系统等级保护合规'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 生物制药客户导入完成，新增 {added} 个')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_biopharma()
