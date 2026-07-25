"""
向长亭作战指挥平台导入湖南省科研机构
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_research():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '湖南省科学技术信息研究所',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省科技厅直属，全省科技信息资源中心和科技战略研究智库。建设运营湖南省科技报告系统、科技专家库、科技奖励评审平台等核心信息系统。管理全省科研项目数据和专家信息，科技数据安全和专家隐私保护为信息安全核心任务。',
            },
            {
                'name': '湖南省农业科学院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省最大农业科研机构，下设杂交水稻研究中心、蔬菜研究所、茶叶研究所等15个专业所。拥有国家水稻改良中心、国家茶树改良中心等国家级平台。农业种质资源数据库和育种信息为国家级战略资产，承担多项国家重大科研项目，科研数据安全保护级别高。',
            },
            {
                'name': '湖南省林业科学院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '天心区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省林业局直属，林业科研公益一类事业单位。聚焦林木遗传育种、森林生态、油茶等经济林、林产品加工等研究。拥有国家油茶工程技术研究中心和林木种质资源数据库。林木良种数据和林业生态监测数据为科研核心资产，需数据安全保护。',
            },
            {
                'name': '湖南省水利水电科学研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '雨花区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省水利厅直属，水利科研与技术服务公益性单位。聚焦水资源管理、水旱灾害防御、水工程安全监测、智慧水利等研究。运营全省水库大坝安全监测系统和水利信息化平台。水利工程安全监测数据直接关系公共安全，系统安全和数据完整性为监管底线。',
            },
            {
                'name': '湖南省环境保护科学研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '雨花区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省生态环境厅直属，环境科研与技术服务核心机构。承担全省环境监测、环境规划、污染治理技术等研究。运营全省环境监测数据管理平台和重点污染源在线监控系统。环境监测数据为政府决策基础，环境数据安全与防篡改至关重要。',
            },
            {
                'name': '湖南省中医药研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省中医药管理局直属，湖南中医药大学附属研究院。聚焦中药资源、中药新药创制、中医临床研究等。拥有中药资源数据库、中药成分数据库和临床研究数据管理系统。中药资源数据和中药配方为国家战略性资源，中医药数据安全关乎文化安全和经济安全。',
            },
            {
                'name': '湖南省地质调查院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省自然资源厅直属，全省基础性公益性地质调查研究机构。拥有全省地质矿产数据库、地质灾害监测预警系统和地质信息服务平台。地质矿产数据为国家基础性战略矿产资源数据，地质灾害监测系统为民生安全保障，需数据安全和高可用双保障。',
            },
            {
                'name': '湖南省计量检测研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '雨花区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省市场监督管理局直属，全省最高法定计量检定机构和质量检验机构。拥有全省计量检定管理系统、产品质量检验信息系统和LIMS实验室信息管理系统。计量检定证书和检验报告具有法律效力，数据完整性和系统安全为核心合规要求。',
            },
            {
                'name': '长沙矿山研究院有限责任公司',
                'industry': '科研', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国五矿集团旗下，国内采矿技术研发核心机构。承担国家深部矿产资源勘探开发、矿山安全技术、海洋采矿等重大科研任务。拥有矿井三维仿真、矿山安全监测和智能采矿技术平台。承担国家重大科技专项，矿山开采技术数据和安全监测系统需高等级安全防护。',
            },
            {
                'name': '长沙矿冶研究院有限责任公司',
                'industry': '科研', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国五矿集团旗下，国内矿产资源综合利用技术研发领军机构。聚焦选矿工艺、冶金新工艺、新能源电池材料等研发。拥有中试生产线LIMS/MES和研发数据管理平台。冶金工艺参数和电池材料配方为核心技术秘密，研发数据防泄漏为安全重中之重。',
            },
            {
                'name': '湖南省交通科学研究院有限公司',
                'industry': '科研', 'org_type': '国企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '中等',
                'description': '湖南省交通运输厅下属，省内交通科研与技术服务龙头。承担高速公路、桥梁、隧道等工程设计、检测、监测和科研工作。运营全省桥梁健康监测系统和公路资产信息化管理平台。桥梁隧道结构安全监测数据直接关系交通安全，系统安全高可用为生命线。',
            },
            {
                'name': '湖南省疾病预防控制中心',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省卫健委直属，全省公共卫生与疾病防控技术核心机构。运营全省传染病网络直报系统、突发公共卫生事件应急指挥信息系统和实验室检测LIMS系统。疫情数据为国家生物安全核心信息，传染病上报系统安全直接影响公共卫生安全，需最高等级信息安全和灾备保障。',
            },
            {
                'name': '湖南省药品检验检测研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省药品监督管理局直属，全省药品化妆品检验检测核心机构。运营药品检验LIMS系统、药品不良反应监测系统和药品标准数据库。药品检验数据和不良反应报告为药品安全监管基础，系统安全直接关系公众用药安全。',
            },
            {
                'name': '湖南省气象科学研究所',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '天心区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '湖南省气象局直属，气象科研与应用技术开发机构。聚焦灾害性天气预报技术、农业气象、人工影响天气等研究。运营区域数值天气预报模式和气象大数据分析平台。气象观测数据和预报模型为气象服务核心资产，数据安全直接关系防灾减灾。',
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

            # 科研机构场景：数据安全 + 等保 + 主机安全
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='科研数据/检测数据/监测数据的分类分级与防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='核心业务信息系统等级保护与行业合规'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='LIMS/监测系统/科研工作站终端安全防护'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 科研机构导入完成，新增 {added} 个')
        print(f'   当前科研行业客户: {Customer.query.filter_by(industry="科研").count()}')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_research()
