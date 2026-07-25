"""
向长亭作战指挥平台导入湖南省半导体行业重点客户
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile, Opportunity, KeyPerson


def seed_semiconductor():
    with app.app_context():
        # ---- 半导体行业客户 ----
        customers = [
            {
                'name': '湖南三安半导体有限责任公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '三安光电全资子公司，总投资160亿元。国内首条8英寸碳化硅全产业链生产线，聚焦SiC/GaN第三代半导体功率芯片。与意法半导体合资建厂，与理想汽车合作。2024年出货超3亿颗，服务全球超800家客户。',
            },
            {
                'name': '长沙景嘉微电子股份有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '国内GPU芯片研发龙头企业，总部位于长沙高新区。产品覆盖GPU、嵌入式计算机、AI智算等。2024年发布景宏系列AI智算产品，2025年入选湖南"人工智能+"十大重点企业。',
            },
            {
                'name': '中车时代半导体有限公司（株洲）',
                'industry': '半导体', 'org_type': '国企', 'city': '株洲', 'district': '石峰区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中车集团旗下功率半导体IDM，建成国内首条6英寸IGBT芯片生产线。第五代IGBT技术成功应用于高铁牵引系统，中低压功率器件产业化项目持续推进。株洲功率半导体产业园2024年产值突破400亿。',
            },
            {
                'name': '飞腾信息技术有限公司（长沙）',
                'industry': '半导体', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '国产自主核心CPU芯片提供商，长沙设有子公司。基于ARM架构研发高性能服务器CPU和桌面CPU，产品广泛应用于信创领域。是中国电子（CEC）旗下核心芯片企业。',
            },
            {
                'name': '国科微电子股份有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'SoC芯片设计上市企业，产品覆盖4K/8K智能机顶盒解码芯片、固态存储主控芯片、视频监控ISP芯片等。是国内领先的集成电路设计企业，多项技术国内首创。',
            },
            {
                'name': '长沙比亚迪半导体有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '长沙县',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国最大的车规级IGBT供应商之一，长沙8英寸晶圆产线月产4万片，覆盖芯片设计、晶圆制造、模块封装完整能力。产品覆盖IGBT、SiC、MCU、传感器等。',
            },
            {
                'name': '湖南进芯电子科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '一般',
                'description': 'DSP芯片设计企业，打破国外DSP芯片垄断。产品覆盖工业控制、电机驱动、数字电源等领域，是国内DSP芯片国产替代的先行者。',
            },
            {
                'name': '芯盛智能科技（湖南）有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '长沙县',
                'scale': '中型', 'it_budget_level': '充足',
                'description': '固态存储主控芯片研发企业，2025年迁址长沙经开区。产品覆盖SATA/PCIe SSD主控芯片、eMMC/UFS存储控制器等，致力于存储芯片国产化。',
            },
            {
                'name': '湖南杰楚微半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '一般',
                'description': '8英寸硅基及6英寸碳化硅晶圆代工企业，提供功率器件、模拟芯片代工服务，是湖南省内稀缺的晶圆代工产能。',
            },
            {
                'name': '长沙驰芯半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中小型', 'it_budget_level': '有限',
                'description': '超宽带（UWB）芯片研发企业，产品应用于室内精确定位、数字钥匙、IoT等场景。是国内UWB芯片领域的新锐力量。',
            },
            {
                'name': '长沙韶光半导体有限公司',
                'industry': '半导体', 'org_type': '国企', 'city': '长沙', 'district': '开福区',
                'scale': '中型', 'it_budget_level': '一般',
                'description': '军用电子元器件研发制造企业，产品覆盖军用集成电路、混合集成电路、微波器件等。是军工半导体领域的重要供应商。',
            },
            {
                'name': '湖南融创微电子科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中小型', 'it_budget_level': '有限',
                'description': '高可靠存储器、微控制器芯片设计企业。产品应用于航天、军工等高可靠领域，是国内高可靠存储芯片的重要供应商。',
            },
            {
                'name': '长沙安牧泉智能科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '一般',
                'description': '高端芯片封装测试企业，年产2000万颗高算力大芯片。聚焦FC-BGA、2.5D/3D先进封装技术，服务于AI芯片、GPU/CPU等高端芯片封装需求。',
            },
            {
                'name': '蓝思科技股份有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '全球消费电子防护玻璃龙头，近年向半导体领域延伸。建设智能装备研发及生产基地，涉及半导体设备零部件制造、精密加工等。2025年列入湖南电子信息制造业重点项目。',
            },
            {
                'name': '韶光芯材科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '长沙县',
                'scale': '中型', 'it_budget_level': '一般',
                'description': '半导体光掩模材料国产化企业，2025年列入湖南重点项目。光掩模是芯片制造的关键材料之一，国产替代需求迫切。',
            },
            {
                'name': '湖南顺为功率半导体有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '株洲', 'district': '天元区',
                'scale': '中小型', 'it_budget_level': '有限',
                'description': '第三代功率半导体SiC/IGBT封测企业，2025年列入湖南重点项目。服务于新能源汽车、光伏储能等功率半导体封装测试需求。',
            },
            {
                'name': '湖南楚微半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '一般',
                'description': '集成电路装备国产化企业，8英寸集成电路成套装备国产化项目入选2025年湖南重点项目。致力于半导体制造设备的自主研发和产业化。',
            },
            {
                'name': '湖南艾迪奥电子科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '益阳', 'district': '赫山区',
                'scale': '中小型', 'it_budget_level': '有限',
                'description': '关键电子元器件研发生产基地，2025年列入湖南重点项目。产品覆盖磁性元件、射频器件等半导体配套元器件。',
            },
        ]

        added = 0
        for c in customers:
            existing = Customer.query.filter_by(name=c['name']).first()
            if existing:
                print(f'  ⏭ 跳过（已存在）: {c["name"]}')
                continue
            db.session.add(Customer(**c))
            added += 1

        db.session.commit()
        print(f'\n✅ 新增 {added} 个半导体行业客户')

        # ---- 为半导体客户创建安全画像 ----
        semi_customers = Customer.query.filter_by(industry='半导体').all()
        profile_count = 0
        for cust in semi_customers:
            existing = SecurityProfile.query.filter_by(customer_id=cust.id).first()
            if existing:
                continue
            # 半导体行业重点关注：数据安全/工业互联网安全/WAF/渗透测试/等保
            profiles = [
                {'customer_id': cust.id, 'product_category': '数据安全', 'current_solution': '暂无', 'satisfaction': '低', 'gap_analysis': '半导体企业涉及大量IP核/设计版图等核心数据，数据防泄漏和分类分级是刚需'},
                {'customer_id': cust.id, 'product_category': '主机安全', 'current_solution': '部分部署杀毒软件', 'satisfaction': '低', 'gap_analysis': '半导体产线涉及工控系统和MES/EDA服务器，主机安全防护薄弱'},
                {'customer_id': cust.id, 'product_category': '安全服务', 'current_solution': '无', 'satisfaction': '低', 'gap_analysis': '等保合规是半导体企业的政策红线，渗透测试和安全评估需求明确'},
            ]
            for p in profiles:
                db.session.add(SecurityProfile(**p))
                profile_count += 1

        db.session.commit()
        print(f'✅ 新增 {profile_count} 条安全画像')

        # ---- 为头部半导体客户创建商机 ----
        head_customers = Customer.query.filter(
            Customer.industry == '半导体',
            Customer.scale.in_(['大型'])
        ).all()

        opp_count = 0
        for cust in head_customers:
            existing_opp = Opportunity.query.filter_by(customer_id=cust.id).first()
            if existing_opp:
                continue

            if '三安' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — SiC产线数据安全治理项目',
                    customer_id=cust.id, product_category='数据安全',
                    product_detail='长亭数据安全治理方案（分类分级+流转监控+API安全）',
                    stage='contacted', amount=80, probability=25,
                    expected_close_date='2026-10-01',
                    pain_point='SiC芯片IP核、设计版图、工艺参数等核心数据保护，客户包括意法半导体、理想汽车等，数据安全合规要求高',
                    our_solution='数据分类分级+流转可视化+动态脱敏+API安全整体方案',
                    competitor_involved='安恒信息',
                    notes='已通过渠道初步接触，CTO对数据安全方案表示兴趣。需安排技术交流演示。'
                )
            elif '景嘉微' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — GPU研发环境等保及安全加固',
                    customer_id=cust.id, product_category='安全服务',
                    product_detail='等保三级测评+渗透测试+主机安全',
                    stage='lead', amount=50, probability=15,
                    expected_close_date='2026-12-01',
                    pain_point='GPU芯片设计EDA环境复杂，AI算力平台数据量大，等保合规+核心IP防泄漏',
                    our_solution='等保一站式服务+牧云主机安全+洞见SOC安全运营',
                    competitor_involved='奇安信',
                    notes='2025年入选湖南AI十大企业，安全投入有望在2026年增加。关注HW参演机会。'
                )
            elif '中车' in cust.name and '半导体' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — IGBT产线工控安全及关基保护',
                    customer_id=cust.id, product_category='主机安全',
                    product_detail='牧云主机安全+工业协议识别+关基合规',
                    stage='contacted', amount=120, probability=30,
                    expected_close_date='2026-09-15',
                    pain_point='IGBT产线属于关键信息基础设施，工控系统安全防护急需升级。高铁/风电等下游应用对供应链安全要求越来越高。',
                    our_solution='牧云主机安全+工控协议深度检测+关基安全评估+洞见SOC',
                    competitor_involved='绿盟科技',
                    notes='株洲功率半导体产业园产值破400亿，安全投入有保障。已与IT总监初步沟通。'
                )
            elif '飞腾' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — CPU研发数据安全与信创合规',
                    customer_id=cust.id, product_category='数据安全',
                    product_detail='数据安全治理+渗透测试+WAF',
                    stage='lead', amount=60, probability=20,
                    expected_close_date='2026-11-01',
                    pain_point='ARM架构CPU研发涉及大量核心IP，信创领域客户对安全资质要求严格',
                    our_solution='数据分类分级+雷池WAF+渗透测试+等保咨询',
                    competitor_involved='深信服',
                )
            elif '国科微' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — SoC芯片设计数据安全及API安全',
                    customer_id=cust.id, product_category='WAF',
                    product_detail='雷池WAF+API安全模块+渗透测试',
                    stage='lead', amount=45, probability=15,
                    expected_close_date='2026-12-15',
                    pain_point='机顶盒/存储/监控三大产品线SoC设计，外协合作多，API安全和数据流转管控需求急迫',
                    our_solution='雷池WAF+API安全+数据安全方案',
                    competitor_involved='启明星辰',
                )
            elif '比亚迪' in cust.name and '半导体' in cust.name:
                opp = Opportunity(
                    title=f'{cust.name} — 车规芯片产线安全及供应链安全',
                    customer_id=cust.id, product_category='主机安全',
                    product_detail='牧云主机安全+工控安全+供应链安全评估',
                    stage='contacted', amount=90, probability=25,
                    expected_close_date='2026-10-15',
                    pain_point='车规级芯片对可靠性和安全性要求极高，8英寸产线月产4万片，供应链安全审查严格',
                    our_solution='牧云主机安全+谛听威胁情报+安全服务组合',
                    competitor_involved='奇安信',
                )
            else:
                continue
            db.session.add(opp)
            opp_count += 1

        db.session.commit()
        print(f'✅ 新增 {opp_count} 条商机')

        # ---- 汇总 ----
        print('\n📊 半导体行业数据导入完成：')
        print(f'   - 客户: {Customer.query.filter_by(industry="半导体").count()} 家')
        print(f'   - 安全画像: {SecurityProfile.query.join(Customer).filter(Customer.industry=="半导体").count()} 条')
        print(f'   - 商机: {Opportunity.query.join(Customer).filter(Customer.industry=="半导体").count()} 条')


if __name__ == '__main__':
    seed_semiconductor()
