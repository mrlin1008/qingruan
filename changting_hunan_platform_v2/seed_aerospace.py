"""
向长亭作战指挥平台导入湖南省航空航天企业（跳过已存在的11家）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import Customer, SecurityProfile


def seed_aerospace():
    with app.app_context():
        existing_names = {c.name for c in Customer.query.with_entities(Customer.name).all()}

        customers = [
            {
                'name': '湖南航天有限责任公司',
                'industry': '航空航天', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '中国航天科工集团（CASIC）在湘二级单位，管理多个研究所和子公司。业务覆盖航天装备、新材料、浮空器、惯性导航、环保装备等领域。军品+民品双线，承担国防重大专项，涉密信息系统按国军标管理。航天装备研发数据和产线工控安全为国家秘密级保护对象。',
            },
            {
                'name': '湖南航天机电设备与特种材料研究所',
                'industry': '航空航天', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '湖南航天（CASIC）下属核心研究所。聚焦航天特种机电设备、惯性导航系统、磁性材料、隐身材料等研制。产品直接应用于导弹、卫星、无人飞行器等国防装备。军品涉密等级为机密级以上，涉密信息系统与研发数据需国家保密标准下的最高安全防护。',
            },
            {
                'name': '长沙天仪空间科技研究院有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '充足',
                'description': '国内商业SAR遥感卫星领军企业，中国首家发射商业SAR卫星。截至2025年已发射超40颗卫星，建成国内最大商业SAR卫星星座。运营卫星测控中心、地面接收站和遥感数据云平台。卫星测控链路安全直接关乎太空资产安全，遥感数据涉及国家安全，需最高等级网络安全防护。',
            },
            {
                'name': '湖南华航航空科技有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '长沙县',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '航空零部件制造与维修企业，为ARJ21/C919等国产飞机提供结构件和内饰件。拥有精密数控加工和复合材料成型产线，通过AS9100航空航天质量认证。航空制造MES系统管理与主机厂的设计数据协同，OEM设计数据保密要求严格。',
            },
            {
                'name': '湖南山河航空动力机械有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '株洲', 'district': '芦淞区',
                'scale': '中型', 'it_budget_level': '充足',
                'description': '山河智能旗下，国内轻型航空活塞发动机领军企业。产品覆盖无人机动力、轻型运动飞机动力、直升机辅助动力等。拥有发动机试车台数据采集系统和研发PLM系统。航空发动机性能数据和设计图纸为核心IP，发动机FADEC控制软件安全为飞行安全关键。',
            },
            {
                'name': '湖南宏大日晟航天动力技术有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '充足',
                'description': '专注于卫星推进系统和火箭动力技术，产品覆盖电推进、化学推进、冷气推进等航天动力系统。为商业卫星和运载火箭提供姿轨控动力方案。推进系统设计仿真和试车数据为核心技术秘密，航天动力研发环境安全等级高。',
            },
            {
                'name': '长沙北斗产业安全技术研究院有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '大型', 'it_budget_level': '充足',
                'description': '国内北斗导航安全领域领军机构，国防科大技术转化平台。承担国家北斗三号安全专项测试、北斗安全终端研制、导航对抗技术研究等任务。拥有北斗信号仿真系统、导航安全测试实验室等核心平台。导航安全测试数据和对抗技术为国家机密级保护对象，信息安全是存在的基础。',
            },
            {
                'name': '湖南中森通信科技有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '北斗导航与卫星通信产品研发企业，产品覆盖北斗高精度接收机、卫星通信终端、抗干扰天线等。服务国防和行业应用客户。通信协议栈代码和导航信号处理算法为核心IP，涉军产品需满足军品信息安全要求。',
            },
            {
                'name': '湖南斯北图科技有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '商业卫星测控与数据应用企业，提供卫星TT&C测控站设备、卫星数据处理平台和卫星物联网解决方案。服务国内多家商业卫星公司。卫星测控链路安全直接关系在轨卫星资产，卫星数据接收和分发系统为关键信息基础设施。',
            },
            {
                'name': '湖南航升卫星科技有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中小型', 'it_budget_level': '中等',
                'description': '微小卫星整星研制和空间技术应用企业。已发射多颗技术验证和业务卫星，聚焦遥感、通信、科学实验等微纳卫星平台。整星AIT和卫星综合测试系统为核心技术设施，卫星研制环境安全和测试数据保护为商业航天竞争力保障。',
            },
            {
                'name': '长沙微纳坤宸新材料有限公司',
                'industry': '航空航天', 'org_type': '民企', 'city': '长沙', 'district': '宁乡市',
                'scale': '中型', 'it_budget_level': '中等',
                'description': '中南大学技术转化企业，国内超高温陶瓷基复合材料领军者。产品应用于高超声速飞行器热防护、火箭发动机喷管、导弹天线罩等极端环境。承担多项国家重大专项和军工配套任务。材料配方和制备工艺为国家级核心技术秘密，涉军研发数据需最高安全防护等级。',
            },
            {
                'name': '湖南航天远望科技有限公司',
                'industry': '航空航天', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区',
                'scale': '中型', 'it_budget_level': '充足',
                'description': '湖南航天（CASIC）下属，国内浮空器（飞艇/系留气球）领域主力企业。产品覆盖预警监视飞艇、通信中继浮空器、环境监测系留气球等。承担军用浮空器平台研制，涉密等级高。飞艇飞行控制和任务载荷系统涉及国防应用，需军工信息安全保护。',
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

            # 航空航天场景：等保+数据安全+主机安全/工控
            profiles = [
                SecurityProfile(customer_id=customer.id, product_category='等保测评',
                                gap_analysis='机会', notes='涉密信息系统/国军标安全保密合规'),
                SecurityProfile(customer_id=customer.id, product_category='数据安全',
                                gap_analysis='机会', notes='航天装备设计/卫星测控/导航安全数据防泄漏'),
                SecurityProfile(customer_id=customer.id, product_category='主机安全',
                                gap_analysis='机会', notes='研发工作站/卫星测控终端/工控系统终端防护'),
            ]
            for p in profiles:
                db.session.add(p)

            added += 1
            print(f'  ✅ 新增: {c["name"]} ({c["industry"]} | {c["city"]})')

        db.session.commit()
        print(f'\n🎯 航空航天企业导入完成，新增 {added} 个')
        print(f'   当前航空航天行业客户: {Customer.query.filter_by(industry="航空航天").count()}')
        print(f'   当前客户总数: {Customer.query.count()}')


if __name__ == '__main__':
    seed_aerospace()
