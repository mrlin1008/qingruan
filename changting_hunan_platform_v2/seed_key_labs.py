"""
向长亭作战指挥平台导入湖南省重点实验室
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_key_labs():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            # ===== 四大省实验室（岳麓山/湘江/芙蓉/岳麓山工业创新中心）=====
            {
                'name': '岳麓山实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省"四大实验室"之首，由湖南省政府联合中国农科院、湖南农大等共建。聚焦种业创新，建设生物育种、分子育种、智能育种等研究平台。拥有基因组测序、生物信息学等高性能计算集群和种质资源数据库，基因数据和育种算法为核心国家级战略资产，需顶级科研数据安全防护。',
            },
            {
                'name': '湘江实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省"四大实验室"之一，湖南工商大学牵头，联合国防科大、中南大学等共建。聚焦先进计算与人工智能，建设AI算力平台、大数据中心、先进计算集群。拥有大规模GPU计算集群和AI模型训练平台，算力安全和AI模型保护为实验室核心安全需求，需防APT攻击窃取AI研究成果。',
            },
            {
                'name': '芙蓉实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省"四大实验室"之一，由中南大学牵头，联合湘雅系医院等共建。聚焦精准医学和生命健康，建设生物样本库、医学大数据平台、精准诊疗研发平台。千万级生物样本数据和患者临床数据为极度敏感信息，需满足人类遗传资源管理条例和数据安全法严格合规要求。',
            },
            {
                'name': '岳麓山工业创新中心',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省"四大实验室"之一，聚焦先进制造与工业技术创新。建设智能制造、高端装备、新能源装备等研发平台。联合三一、中联、中车等龙头企业，产学研协同研发数据汇聚。多方协同创新环境下数据分级分类、访问控制和知识产权保护为安全管理核心难题。',
            },

            # ===== 国家重点实验室（依托高校在湘部分）=====
            {
                'name': '粉末冶金国家重点实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '依托中南大学建设，国内粉末冶金领域唯一的国家重点实验室。聚焦高性能粉末冶金材料、碳/碳复合材料等前沿研究，多项成果应用于航空航天和国防装备。承担大量国防军工项目，科研成果和工艺数据涉密等级高，实验数据和超算资源需严格安全管控。',
            },
            {
                'name': '高性能计算国家重点实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '依托国防科技大学建设，国家超级计算长沙中心（天河系列）核心支撑。聚焦高性能计算机体系结构、大规模并行计算、量子计算等前沿领域。拥有天河超级计算机集群，承担国防和国家重大项目计算任务，超算系统安全为国家战略级关基保护重点。',
            },
            {
                'name': '化学生物传感与计量学国家重点实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '依托湖南大学建设，化学与生物交叉学科前沿研究基地。聚焦化学传感器、生物纳米技术、化学生物学等领域。拥有大型精密仪器共享平台和科研数据管理系统，仪器联网和数据自动采集，实验室信息系统安全和科研成果保护为管理重点。',
            },
            {
                'name': '杂交水稻全国重点实验室',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '芙蓉区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '依托湖南杂交水稻研究中心（国家杂交水稻工程技术研究中心）建设，袁隆平院士创立。聚焦超级杂交稻、耐盐碱水稻、智能育种等研究，保障国家粮食安全。种质资源基因组数据库和育种算法为国家核心农业机密，数据安全等级对标国家秘密。',
            },

            # ===== 省重点实验室级别的其它重要科研平台 =====
            {
                'name': '国家超级计算长沙中心',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '科技部批复的国家级超算中心，由湖南大学运营管理。拥有"天河"系列超级计算机，总算力达千万亿次级别。服务湖南及周边省份气象预报、生物医药、智能制造等领域计算需求。超算中心为关键信息基础设施，算力调度安全和用户数据隔离为核心安全要求。',
            },
            {
                'name': '国家先进轨道交通装备创新中心',
                'industry': '科研', 'org_type': '国企', 'city': '株洲', 'district': '石峰区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '工信部批复的国家级制造业创新中心，由中车株机牵头12家单位共建。聚焦轨道交通装备关键共性技术研发，包括智能运维、新能源动力、智能制造等领域。联合研发平台汇聚多家央企核心技术数据，多方协同下IP保护和数据安全隔离为管理痛点。',
            },
            {
                'name': '湖南光电集成创新研究院',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '依托湖南大学建设，聚焦硅基光电子、光子集成芯片、量子光学等前沿研究。光学芯片设计仿真和制造工艺测试平台为核心科研设施，光子芯片设计和测试数据为前沿科技制高点，研究成果具有高商业价值且易于数字化窃取，安全保护尤为关键。',
            },
            {
                'name': '湖南省北斗导航产业技术创新战略联盟',
                'industry': '科研', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南省北斗卫星导航应用产业协同创新平台，联合国防科大、长沙北斗产业安全技术研究院、中森通信等产学研单位。聚焦北斗芯片、终端、应用系统研发和测试评估。卫星导航测试数据和信号仿真软件为核心资产，卫星导航安全测试环境需物理隔离和最高安全防护。',
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

            # 科研实验室场景：数据安全 + 等保 + 主机安全
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='科研数据/基因数据/超算数据分级分类与防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='国家级平台/超算中心等级保护与关基合规'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='超算集群/精密仪器工作站终端安全防护'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 重点实验室导入完成，新增 {added} 个')
        print(f'   当前科研行业客户: {Customer.query.filter_by(industry="科研").count()}')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_key_labs()
