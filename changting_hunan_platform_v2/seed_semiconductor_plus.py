"""
完善湖南省半导体行业客户（去重+补充）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_semiconductor_plus():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        # 先处理疑似重复：274 湖南杰楚微 vs 281 湖南楚微
        # 杰楚微可能是录入时的错误，保留楚微，删除杰楚微
        dup = Customer.query.filter_by(name='湖南杰楚微半导体科技有限公司').first()
        if dup:
            print(f'  🗑️  删除疑似重复: {dup.name} (与湖南楚微半导体重复)')
            # 删除关联数据
            from models import SecurityProfile, Opportunity, KeyPerson, InsightSignal
            SecurityProfile.query.filter_by(customer_id=dup.id).delete()
            Opportunity.query.filter_by(customer_id=dup.id).delete()
            KeyPerson.query.filter_by(customer_id=dup.id).delete()
            InsightSignal.query.filter_by(related_customer_id=dup.id).delete()
            db.session.delete(dup)
            db.session.flush()
            print(f'  已清理，ID={dup.id}')

        # 补充半导体客户
        customers = [
            {
                'name': '湖南启泰传感科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '浏阳市',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '国内少数掌握金属基MEMS压力芯片全技术链的企业，产品覆盖工业、汽车、医疗等领域压力传感器芯片。拥有6英寸MEMS产线，自主研发的传感器芯片已进入比亚迪、三一等供应链。产线MES和芯片设计EDA系统为安全核心，研发数据保护为关键需求。',
            },
            {
                'name': '湖南格兰博智能科技有限责任公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '专注于AIOT智能芯片设计，产品覆盖智能语音芯片、物联网MCU、智能家居SoC等。拥有自主研发的芯片IP和嵌入式AI算法。芯片RTL设计和固件源码为核心IP资产，代码安全和IP保护为生命线，需防反向工程和代码泄露。',
            },
            {
                'name': '湖南欧智通科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '专注于WiFi/BT通信芯片设计，产品覆盖WiFi6/6E芯片、蓝牙SoC、物联网连接芯片等。为智能家居和物联网终端提供连接方案。无线通信基带算法和协议栈代码为核心技术资产，芯片设计数据安全为关键。',
            },
            {
                'name': '湖南长城银河科技有限公司',
                'industry': '半导体', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国长城科技旗下，国产自主可控计算机核心部件研制企业。产品覆盖国产CPU主板、军用加固计算机、自主可控服务器等。国防军工业务涉密等级高，产品设计和BOM数据为国家秘密级保护对象，研发环境隔离和数据安全为刚性要求。',
            },
            {
                'name': '湖南国芯半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '功率半导体器件研发制造企业，产品覆盖MOSFET、IGBT、碳化硅器件等。拥有器件仿真设计平台和功率模块封测产线。功率半导体器件工艺参数和仿真模型为技术秘密，工控系统和研发数据需安全隔离防护。',
            },
            {
                'name': '湖南越摩先进半导体有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '望城区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '高端芯片先进封装企业，系统级封装（SiP）和晶圆级封装（WLP）在省内领先。服务5G通信、AI、汽车电子等领域客户的封装需求。先进封装工艺为高精度自动化产线，MES/ERP系统安全与工艺参数保护为运营基础。',
            },
            {
                'name': '中国电子科技集团公司第四十八研究所',
                'industry': '半导体', 'org_type': '国企', 'city': '长沙', 'district': '天心区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': 'CETC在湘核心研究所，国内半导体工艺设备和光伏装备的骨干研发单位。承担离子注入机、扩散炉、PECVD等半导体核心装备研制任务，产品用于国内多条晶圆产线。军品+国家重大专项，半导体装备研发数据和工艺参数为国家战略级科技秘密，需最高安全防护等级。',
            },
            {
                'name': '湖南时变通讯科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '射频微波芯片与组件设计企业，产品覆盖相控阵射频芯片、5G毫米波芯片、卫星通信芯片等。服务国防电子和通信基础设施领域。射频芯片设计和电磁仿真数据为核心技术资产，涉军业务需满足保密要求。',
            },
            {
                'name': '湖南晶湛半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '第三代半导体GaN氮化镓材料和器件研发企业。产品聚焦电力电子GaN功率器件和射频GaN器件。外延生长工艺和器件工艺为核心技术秘密，MOCVD设备工艺参数和研发数据需严防泄密。',
            },
            {
                'name': '湖南天羿微电子科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中小型', 'it_budget_level': '中等',
                'description': 'MEMS微镜芯片和光学传感器设计企业，产品覆盖激光雷达扫描镜、微型投影显示芯片、3D传感芯片等。MEMS设计仿真和微加工工艺为核心技术壁垒。fabless模式，芯片设计IP和版图数据安全为生存保障。',
            },
            {
                'name': '长沙瑶华半导体科技有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '长沙', 'district': '望城区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '半导体封装测试服务企业，提供QFN/BGA/SiP等中高端封装和测试服务，服务省内集成电路设计企业。封测产线MES系统和测试程序数据为客户委托加工的核心资产。客户IP保护和产线数据隔离为封测代工行业的合规基础。',
            },
            {
                'name': '株洲晶鑫半导体设备有限公司',
                'industry': '半导体', 'org_type': '民企', 'city': '株洲', 'district': '天元区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '半导体专用设备制造企业，产品覆盖晶圆清洗设备、刻蚀设备、薄膜沉积设备等。为株洲功率半导体产业集群提供设备配套。设备控制软件和工艺配方为核心竞争力，PLC/工控系统安全直接关系客户产线良率和安全。',
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

            # 半导体场景：工控安全 + 数据安全 + 等保测评
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='晶圆产线MES/EAP/设备工控终端安全防护'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='芯片设计IP/工艺参数/版图数据防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='军工/国家重大专项涉密系统安全合规'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 半导体行业完善完成')
        print(f'   删除重复: 1 个（杰楚微）')
        print(f'   新增补充: {added} 个')
        semi_count = Customer.query.filter_by(industry='半导体').count()
        print(f'   当前半导体行业客户总数: {semi_count}')


if __name__ == '__main__':
    seed_semiconductor_plus()
