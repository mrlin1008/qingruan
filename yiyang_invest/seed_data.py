"""
益阳高新区智慧招商平台 — 种子数据
"""
import os
import sys
from werkzeug.security import generate_password_hash
from app import app, db
from models import (User, ParkInfo, IndustryChain, Company, Lead, Project, FollowUp,
                    Space, Policy, Article, BiddingRecord, ProcurementDemand,
                    DemandResponse, TechCapability, TechChallenge, ParkImage)

# 四大赛道产业链节点定义
CHAIN_DATA = [
    # 智能感知
    {'name': '智能感知', 'track': '智能感知', 'chain_position': '', 'gap_level': '完善', 'sort_order': 1,
     'description': '光电感知、激光雷达、量子检测等传感器研发制造', 'children': [
        {'name': '光电传感器', 'track': '智能感知', 'chain_position': '上游', 'gap_level': '薄弱',
         'description': '压电陶瓷、MLCC配套芯片、光学镜头等核心元器件'},
        {'name': '激光雷达模组', 'track': '智能感知', 'chain_position': '中游', 'gap_level': '薄弱',
         'description': '车载/工业激光雷达感知模组研发与中试'},
        {'name': '量子检测设备', 'track': '智能感知', 'chain_position': '中游', 'gap_level': '空白',
         'description': '量子精密测量与检测传感设备'},
        {'name': '传感器封测', 'track': '智能感知', 'chain_position': '下游', 'gap_level': '完善',
         'description': '传感器封装测试与量产制造'},
    ]},
    # 工业视觉
    {'name': '工业视觉', 'track': '工业视觉', 'chain_position': '', 'gap_level': '薄弱', 'sort_order': 2,
     'description': '面向制造业的AI视觉检测、识别与测量系统', 'children': [
        {'name': '工业相机与镜头', 'track': '工业视觉', 'chain_position': '上游', 'gap_level': '空白',
         'description': '高精度工业相机、远心镜头、光源系统'},
        {'name': '视觉算法平台', 'track': '工业视觉', 'chain_position': '中游', 'gap_level': '空白',
         'description': 'AI视觉检测算法、深度学习训练平台'},
        {'name': '视觉检测装备', 'track': '工业视觉', 'chain_position': '下游', 'gap_level': '薄弱',
         'description': 'PCB检测、零部件外观检测、装配引导等专用设备'},
    ]},
    # 装备智能
    {'name': '装备智能', 'track': '装备智能', 'chain_position': '', 'gap_level': '完善', 'sort_order': 3,
     'description': '工程机械、橡塑机械等高端装备的智能化升级', 'children': [
        {'name': '智能控制器', 'track': '装备智能', 'chain_position': '上游', 'gap_level': '薄弱',
         'description': '嵌入式控制器、PLC、工业总线模块'},
        {'name': '工业软件', 'track': '装备智能', 'chain_position': '中游', 'gap_level': '空白',
         'description': 'MES、数字孪生、预测性维护等工业软件'},
        {'name': '智能装备集成', 'track': '装备智能', 'chain_position': '下游', 'gap_level': '完善',
         'description': '路面机械AI工厂、碳基材料智能调控等装备集成'},
        {'name': '机器人系统', 'track': '装备智能', 'chain_position': '下游', 'gap_level': '空白',
         'description': '工业机器人、协作机器人、AGV系统集成'},
    ]},
    # 算力配套
    {'name': '算力配套', 'track': '算力配套', 'chain_position': '', 'gap_level': '完善', 'sort_order': 4,
     'description': '智算中心、数据中心、储能系统等算力基础设施', 'children': [
        {'name': '算力芯片与模组', 'track': '算力配套', 'chain_position': '上游', 'gap_level': '空白',
         'description': 'AI加速卡、算力模组、边缘计算芯片'},
        {'name': '数据中心配套', 'track': '算力配套', 'chain_position': '中游', 'gap_level': '薄弱',
         'description': '服务器、存储、网络设备及运维'},
        {'name': '储能系统', 'track': '算力配套', 'chain_position': '配套', 'gap_level': '完善',
         'description': '虚拟电厂、储能电池、绿色能源'},
    ]},
]

# 空间资源
SPACE_DATA = [
    # 孵化区
    {'name': '数字经济研发服务中心A座', 'zone': '孵化区', 'building': 'A座', 'floor': '1-5F',
     'total_area': 29000, 'available_area': 12000, 'floor_height': '3.6m',
     'load_capacity': '300kg/㎡', 'power_supply': '双回路供电',
     'supporting': '中央空调、光纤入户、共享会议室、路演大厅',
     'rent_desc': '面议（根据项目质量给予租金减免）',
     'status': 'available'},
    {'name': '湖南未来光电技术研究院', 'zone': '孵化区', 'building': 'B座', 'floor': '2F',
     'total_area': 1960, 'available_area': 0, 'floor_height': '3.9m',
     'load_capacity': '500kg/㎡', 'power_supply': '专用配电',
     'supporting': '实验室、洁净间、光电器件测试平台',
     'rent_desc': '已入驻（麓宇光电等）',
     'status': 'occupied'},
    # 制造区
    {'name': '标准厂房1栋', 'zone': '制造区', 'building': '1栋', 'floor': '1-3F',
     'total_area': 8000, 'available_area': 5000, 'floor_height': '5.5m（首层）/4.5m',
     'load_capacity': '800kg/㎡', 'power_supply': '500KVA/栋，可扩容',
     'supporting': '变电站、污水处理站、气站、行车、货梯',
     'rent_desc': '15-25元/㎡/月（前两年享受租金补贴）',
     'status': 'available'},
    {'name': '标准厂房2栋', 'zone': '制造区', 'building': '2栋', 'floor': '1-3F',
     'total_area': 8000, 'available_area': 8000, 'floor_height': '5.5m（首层）/4.5m',
     'load_capacity': '800kg/㎡', 'power_supply': '500KVA/栋，可扩容',
     'supporting': '变电站、污水处理站、气站、行车、货梯',
     'rent_desc': '15-25元/㎡/月（前两年享受租金补贴）',
     'status': 'available'},
    {'name': '标准厂房5栋', 'zone': '制造区', 'building': '5栋', 'floor': '1-2F',
     'total_area': 5500, 'available_area': 2000, 'floor_height': '5.5m（首层）/4.5m',
     'load_capacity': '800kg/㎡', 'power_supply': '500KVA/栋，可扩容',
     'supporting': '变电站、污水处理站、气站、行车、货梯',
     'rent_desc': '15-25元/㎡/月（前两年享受租金补贴）',
     'status': 'available'},
]

# 示例政策
POLICY_DATA = [
    {'title': '益阳高新区促进人工智能产业发展若干政策（征求意见稿）', 'policy_type': '科技创新',
     'issuing_dept': '益阳高新区管委会', 'summary': '从场地、研发、人才、金融、上市等方面对AI企业给予专项支持。',
     'publish_date': '2026-07-01'},
    {'title': '益阳高新区招商项目租金补贴实施办法', 'policy_type': '租金减免',
     'issuing_dept': '益阳高新区产业发展局', 'summary': '新入驻数字经济产业园的项目，前两年享受租金50%-100%补贴。',
     'publish_date': '2026-06-15'},
    {'title': '益阳市高层次人才引进实施办法', 'policy_type': '人才补贴',
     'issuing_dept': '益阳市委人才办', 'summary': '对引进的高层次人才给予安家补贴、科研启动经费、租房补贴等。',
     'publish_date': '2026-05-20'},
    {'title': '益阳高新区科技创新专项资金管理办法', 'policy_type': '科技创新',
     'issuing_dept': '益阳高新区财政局', 'summary': '对研发投入、平台建设、成果转化等给予专项资金支持。',
     'publish_date': '2026-04-10'},
    {'title': '湖南省"人工智能+"行动实施方案', 'policy_type': '科技创新',
     'issuing_dept': '湖南省工信厅', 'summary': '落实"人工智能+"行动部署，推进AI与制造业深度融合。',
     'publish_date': '2026-03-01'},
]

# 示例新闻
ARTICLE_DATA = [
    {'title': '益阳高新区与中南大学达成科技成果转化合作备忘', 'category': '园区动态',
     'summary': '6月23日，向书记与中南大学校长李建成院士一行达成合作备忘，将加快推进益阳与中南大学科技成果转化。',
     'source_url': 'https://www.rmlt.com.cn/2026/0713/753156.shtml',
     'publish_date': '2026-06-25', 'is_published': True},
    {'title': '湖南未来光电技术研究院落地运营', 'category': '产业资讯',
     'summary': '已与湖南师范大学共建湖南未来光电技术研究院，落地麓宇光电电致变色、激光雷达AI感知项目。',
     'source_url': 'http://mp.weixin.qq.com/s?__biz=MzU3NzEzNjU2NQ==&mid=2247587141&idx=2&sn=b7e80fd8c84f5c53d7222caeb025c820',
     'publish_date': '2026-06-10', 'is_published': True},
    {'title': '益阳高新区195家规上工业，近30家布局AI业务', 'category': '园区动态',
     'summary': '全区现有规上工业195家，三一、益阳橡机、信维电科、金博股份等龙头企业具备智能化改造基础。',
     'source_url': 'http://yygxq.yiyang.gov.cn/27355/27359/content_2077691.html',
     'publish_date': '2026-05-15', 'is_published': True},
    {'title': '益阳智算中心正式投入使用', 'category': '产业资讯',
     'summary': '智算中心可提供AI训练、推理算力服务，为区域AI产业发展提供算力底座。',
     'source_url': 'http://yygxq.yiyang.gov.cn/27355/27359/content_2077691.html',
     'publish_date': '2026-04-20', 'is_published': True},
]


def seed_all():
    with app.app_context():
        db.create_all()
        print('✓ 数据库表创建完成')

        # 1. 管理员用户
        if not User.query.first():
            admin = User(
                username='admin',
                display_name='管理员',
                role='admin',
                phone='13800000001',
            )
            admin.password_hash = generate_password_hash('admin123')
            db.session.add_all([
                admin,
                User(username='zhangwei', display_name='张伟', role='manager', phone='13800000002',
                     password_hash=generate_password_hash('123456')),
                User(username='liming', display_name='李明', role='staff', phone='13800000003',
                     password_hash=generate_password_hash('123456')),
                User(username='wangfang', display_name='王芳', role='staff', phone='13800000004',
                     password_hash=generate_password_hash('123456')),
            ])
            db.session.commit()
            print('✓ 用户数据（4人招商团队）创建完成')
            print('  管理员: admin / admin123')
            print('  张伟(经理): zhangwei / 123456')
            print('  李明(专员): liming / 123456')
            print('  王芳(专员): wangfang / 123456')
        else:
            print('  用户数据已存在，跳过')

        # 2. 园区信息
        if not ParkInfo.query.first():
            park = ParkInfo(
                park_name='益阳高新区数字经济产业园',
                overview='益阳高新区是长株潭协同型"光电+工业人工智能"特色产业集聚区，聚焦智能感知、工业视觉、装备智能、算力配套四大细分赛道。园区依托数字经济产业园双载体——14.5万㎡研发孵化区和10栋标准厂房制造区，联动湖南未来光电技术研究院、中南大学成果转化基地、益阳智算中心等核心资源，构建"算力底座+创新平台+产业制造+全域场景"发展模式。',
                location_desc='位于湖南省益阳市，距长沙市区约70公里，长张高速、益娄高速交汇，高铁益阳南站直达。处于长株潭城市群1小时经济圈内，可共享长沙高校、科研院所、产业链配套资源。',
                total_area='规划总面积约50万㎡',
                incubator_area='孵化区14.5万㎡（研发办公楼宇）',
                factory_area='制造区10栋标准厂房（含变电站、污水处理站）',
                settled_count=195,
                investment_total=0,
                key_resources='智算中心、湖南未来光电技术研究院、中南大学成果转化基地、虚拟电厂（全省第二家）、中南科创园',
            )
            db.session.add(park)
            db.session.commit()
            print('✓ 园区信息创建完成')
        else:
            print('  园区信息已存在，跳过')

        # 3. 产业链节点
        if not IndustryChain.query.first():
            for track_data in CHAIN_DATA:
                children = track_data.pop('children', [])
                parent = IndustryChain(**track_data)
                db.session.add(parent)
                db.session.flush()
                for child_data in children:
                    child_data['parent_id'] = parent.id
                    db.session.add(IndustryChain(**child_data))
            db.session.commit()
            print(f'✓ 产业链节点创建完成（{IndustryChain.query.count()}个节点）')
        else:
            print('  产业链节点已存在，跳过')

        # 3.5 链主企业
        if not Company.query.filter_by(is_chain_leader=True).first():
            chain_leaders = [
                {'name': '三一重工（益阳）', 'company_type': 'settled', 'industry_track': '装备智能',
                 'scale': '大型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区东部产业园三一大道1号',
                 'lat': 28.585, 'lng': 112.368,
                 'description': '三一重工益阳路面机械智能制造基地，AI数字孪生工厂，年产值超50亿。是益阳高新区装备智能赛道的核心链主企业。',
                 'is_chain_leader': True, 'status': 'active'},
                {'name': '信维电科', 'company_type': 'settled', 'industry_track': '工业视觉',
                 'scale': '大型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区数字经济产业园A区',
                 'lat': 28.572, 'lng': 112.355,
                 'description': 'MLCC智能质检大模型应用基地，电子元器件智能制造标杆工厂，AI质检技术行业领先。',
                 'is_chain_leader': True, 'status': 'active'},
                {'name': '金博股份', 'company_type': 'settled', 'industry_track': '工业视觉',
                 'scale': '大型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区碳谷产业园',
                 'lat': 28.590, 'lng': 112.362,
                 'description': '碳基材料智能制造龙头企业，上市公司。生产过程中的智能调控和质量检测需求量大，对视觉检测设备有持续采购需求。',
                 'is_chain_leader': True, 'status': 'active'},
                {'name': '麓宇光电', 'company_type': 'settled', 'industry_track': '智能感知',
                 'scale': '中型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区未来光电技术研究院',
                 'lat': 28.575, 'lng': 112.345,
                 'description': '电致变色器件和激光雷达模组研发制造企业，依托湖南未来光电技术研究院，是智能感知赛道的链主企业。',
                 'is_chain_leader': True, 'status': 'active'},
                {'name': '益阳智算中心', 'company_type': 'settled', 'industry_track': '算力配套',
                 'scale': '大型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区中南科创园智算中心',
                 'lat': 28.568, 'lng': 112.370,
                 'description': '益阳高新区智算中心，已建成大规模AI训练推理算力集群，服务中南地区AI企业。',
                 'is_chain_leader': True, 'status': 'active'},
                {'name': '益阳橡机', 'company_type': 'settled', 'industry_track': '装备智能',
                 'scale': '大型', 'city': '益阳', 'district': '高新区',
                 'address': '益阳市高新区橡塑机械产业园',
                 'lat': 28.592, 'lng': 112.358,
                 'description': '橡塑机械智能化升级龙头企业，正推进产线数字化和智能装备集成。',
                 'is_chain_leader': True, 'status': 'active'},
            ]
            for c in chain_leaders:
                db.session.add(Company(**c))
            db.session.flush()  # 获取链主企业实际ID
            print(f'✓ 链主企业创建完成（{Company.query.filter_by(is_chain_leader=True).count()}家）')

            # 按名称定位链主企业
            sany = Company.query.filter(Company.name.contains('三一')).first()
            xinwei = Company.query.filter(Company.name.contains('信维')).first()
            jinbo = Company.query.filter(Company.name.contains('金博')).first()
            luyao = Company.query.filter(Company.name.contains('麓宇')).first()
            zhisuan = Company.query.filter(Company.name.contains('智算')).first()
            xiangji = Company.query.filter(Company.name.contains('橡机')).first()
        else:
            print('  链主企业已存在，跳过')

        # 3.6 采购需求
        if not ProcurementDemand.query.first():
            demands = [
                {'chain_company_id': sany.id if sany else None, 'title': '2026年度工业控制器供应商招募',
                 'category': '零部件', 'demand_type': '年度采购',
                 'amount_estimate': '2000万元/年', 'quantity_desc': '约500套/年',
                 'deadline': '2026-09-30',
                 'requirements': '1. 通过ISO9001质量管理体系认证\n2. 有工程机械行业供货经验优先\n3. 注册资本500万元以上\n4. 具备PLC/运动控制器自主生产能力',
                 'description': '三一重工益阳基地2026年度工业控制器采购计划，主要用于路面机械智能化产线。采购品类包括PLC控制器、运动控制器、工业PC等。要求供应商具备持续供货能力和售后技术支持能力。',
                 'contact_info': '三一益阳采购部 张经理 0737-XXXXXXX',
                 'industry_track': '装备智能', 'status': 'open', 'published_at': '2026-07-15'},
                {'chain_company_id': sany.id if sany else None, 'title': '数字孪生软件平台采购需求',
                 'category': '软件', 'demand_type': '供应商招募',
                 'amount_estimate': '500万元', 'quantity_desc': '1套（含3年运维）',
                 'deadline': '2026-10-15',
                 'requirements': '1. 具备工业数字孪生项目实施经验\n2. 支持主流PLC/CNC数据采集\n3. 平台支持二次开发\n4. 团队有制造业案例',
                 'description': '三一益阳工厂正在建设AI数字孪生工厂，需采购数字孪生软件平台，实现产线仿真、工艺优化和预测性维护功能。',
                 'contact_info': '三一数字化部 李工 0737-XXXXXXX',
                 'industry_track': '装备智能', 'status': 'open', 'published_at': '2026-07-20'},
                {'chain_company_id': xinwei.id if xinwei else None, 'title': 'AI视觉检测传感器紧急采购',
                 'category': '设备', 'demand_type': '紧急采购',
                 'amount_estimate': '800万元', 'quantity_desc': '200台工业相机+配套光源',
                 'deadline': '2026-09-01',
                 'requirements': '1. 工业相机分辨率≥2000万像素\n2. 支持GigE Vision/USB3 Vision协议\n3. 含配套LED光源及控制器\n4. 最快30天内交货',
                 'description': '信维电科MLCC产线质检工位升级，紧急采购工业相机和机器视觉光源，需配合现有AI视觉检测算法平台完成集成调试。',
                 'contact_info': '信维电科设备部 刘工 0737-XXXXXXX',
                 'industry_track': '工业视觉', 'status': 'open', 'published_at': '2026-08-01'},
                {'chain_company_id': jinbo.id if jinbo else None, 'title': '碳基材料烧结过程智能监测系统',
                 'category': '设备', 'demand_type': '供应商招募',
                 'amount_estimate': '1200万元', 'quantity_desc': '5条产线',
                 'deadline': '2026-11-30',
                 'requirements': '1. 有高温环境（>2000℃）工业检测经验\n2. 支持多光谱/热成像分析\n3. 系统MTBF>8000小时\n4. 提供2年以上质保',
                 'description': '金博股份碳基材料生产过程中需要对烧结过程进行实时智能监测和异常预警。需要部署多光谱传感器和热成像系统，结合AI算法实现工艺参数实时调控。',
                 'contact_info': '金博股份技术中心 陈主任 0737-XXXXXXX',
                 'industry_track': '工业视觉', 'status': 'open', 'published_at': '2026-07-25'},
                {'chain_company_id': luyao.id if luyao else None, 'title': '激光雷达光学元件年度采购',
                 'category': '原材料', 'demand_type': '年度采购',
                 'amount_estimate': '1500万元/年', 'quantity_desc': '约10万片光学镜片/年',
                 'deadline': '2026-10-01',
                 'requirements': '1. 光学镜片面型精度≤λ/4\n2. 镀膜损伤阈值≥5J/cm²\n3. 通过IATF16949认证优先\n4. 具备车规级批量供货能力',
                 'description': '麓宇光电激光雷达模组量产需要稳定的光学元件供应，包括非球面镜片、分光镜、反射镜等。需建立长期供应关系，年需求量随产能爬坡逐步增长。',
                 'contact_info': '麓宇光电采购部 周总监 0737-XXXXXXX',
                 'industry_track': '智能感知', 'status': 'open', 'published_at': '2026-08-05'},
                {'chain_company_id': zhisuan.id if zhisuan else None, 'title': '数据中心液冷散热系统采购',
                 'category': '设备', 'demand_type': '供应商招募',
                 'amount_estimate': '3000万元', 'quantity_desc': '覆盖500个机柜',
                 'deadline': '2026-12-31',
                 'requirements': '1. 液冷方案PUE≤1.15\n2. 支持单机柜30kW以上散热\n3. 有数据中心液冷项目成功案例\n4. 提供3年运维服务',
                 'description': '益阳智算中心二期扩容，新增500个高密度GPU机柜，需配套液冷散热系统。要求方案PUE（电能使用效率）低于1.15，支持弹性扩容。',
                 'contact_info': '智算中心运维 赵工 0737-XXXXXXX',
                 'industry_track': '算力配套', 'status': 'open', 'published_at': '2026-08-10'},
                {'chain_company_id': xiangji.id if xiangji else None, 'title': '橡塑机械产线智能化改造集成服务',
                 'category': '服务', 'demand_type': '供应商招募',
                 'amount_estimate': '600万元', 'quantity_desc': '3条产线',
                 'deadline': '2026-11-15',
                 'requirements': '1. 有大型装备产线改造经验\n2. 熟悉西门子/三菱PLC体系\n3. 具备MES系统对接能力\n4. 方案含数据采集与看板',
                 'description': '益阳橡机3条橡塑机械装配产线需进行智能化改造，包括设备联网、数据采集、MES接入和产线可视化看板。需交钥匙工程。',
                 'contact_info': '益阳橡机技改办 黄主任 0737-XXXXXXX',
                 'industry_track': '装备智能', 'status': 'open', 'published_at': '2026-08-12'},
                {'chain_company_id': xinwei.id if xinwei else None, 'title': 'SMT产线AOI检测设备采购',
                 'category': '设备', 'demand_type': '供应商招募',
                 'amount_estimate': '900万元', 'quantity_desc': '10台',
                 'deadline': '2026-10-30',
                 'requirements': '1. AOI检测精度≥10μm\n2. 支持01005元器件检测\n3. 误报率≤5%\n4. 含SPC统计过程控制软件',
                 'description': '信维电科新SMT产线需配置10台在线AOI（自动光学检测）设备，用于PCB焊接质量检测。要求支持01005微型元件检测和实时SPC分析。',
                 'contact_info': '信维电科SMT车间 王主任 0737-XXXXXXX',
                 'industry_track': '工业视觉', 'status': 'open', 'published_at': '2026-08-15'},
            ]
            for d in demands:
                db.session.add(ProcurementDemand(**d))
            db.session.commit()
            print(f'✓ 采购需求创建完成（{ProcurementDemand.query.count()}条）')
        else:
            print('  采购需求已存在，跳过')

        # 4. 空间资源
        if not Space.query.first():
            for s in SPACE_DATA:
                db.session.add(Space(**s))
            db.session.commit()
            print(f'✓ 空间资源创建完成（{Space.query.count()}个空间）')
        else:
            print('  空间资源已存在，跳过')

        # 5. 政策
        if not Policy.query.first():
            for p in POLICY_DATA:
                db.session.add(Policy(**p))
            db.session.commit()
            print(f'✓ 政策数据创建完成（{Policy.query.count()}条）')
        else:
            print('  政策数据已存在，跳过')

        # 6. 新闻
        if not Article.query.first():
            for a in ARTICLE_DATA:
                db.session.add(Article(**a))
            db.session.commit()
            print(f'✓ 新闻数据创建完成（{Article.query.count()}条）')
        else:
            print('  新闻数据已存在，跳过')

        # 7. 园区实景图
        if not ParkImage.query.first():
            park_images = [
                {'filename': '20260730002931_1212ab27.jpeg', 'original_name': '园区孵化楼外景.jpeg',
                 'file_size': 1369253, 'category': '园区风光', 'sort_order': 1},
                {'filename': '20260730002951_de7a1dd2.jpg', 'original_name': '标准厂房内景.jpg',
                 'file_size': 1003548, 'category': '制造厂房', 'sort_order': 2},
                {'filename': '20260730003011_8608b13d.png', 'original_name': '研发中心办公区.png',
                 'file_size': 1017311, 'category': '孵化空间', 'sort_order': 3},
            ]
            for img in park_images:
                db.session.add(ParkImage(**img))
            db.session.commit()
            print(f'✓ 园区实景图创建完成（{ParkImage.query.count()}张）')
        else:
            print('  园区实景图已存在，跳过')

        # 8. 招商线索
        if not Lead.query.first():
            for l in [
                {'company_name':'深圳华科创智','contact_person':'陈总','contact_phone':'138xxxx2001','source':'以商招商','industry_track':'智能感知','intent_level':'高','status':'对接中','assigned_to':2,'notes':'通过麓宇光电推荐，正在寻找中部地区生产基地。'},
                {'company_name':'武汉锐科激光','contact_person':'刘经理','contact_phone':'139xxxx2002','source':'展会','industry_track':'智能感知','intent_level':'中','status':'待处理','assigned_to':3,'notes':'光博会接触，光纤激光器国内前三，有扩产计划。'},
                {'company_name':'苏州天准科技','contact_person':'赵副总','contact_phone':'136xxxx2003','source':'网络线索','industry_track':'工业视觉','intent_level':'高','status':'对接中','assigned_to':2,'notes':'科创板上市，AI视觉检测装备龙头，已提交选址需求。'},
                {'company_name':'汇川技术','contact_person':'王总监','contact_phone':'137xxxx2004','source':'推介会','industry_track':'装备智能','intent_level':'中','status':'对接中','assigned_to':4,'notes':'6月长沙推介会接触，对配套三一益阳工厂有明确兴趣。'},
                {'company_name':'杭州海康机器人','contact_person':'李总','contact_phone':'135xxxx2005','source':'在线表单','industry_track':'工业视觉','intent_level':'中','status':'待处理','assigned_to':3,'notes':'关注信维电科MLCC质检设备采购机会。'},
                {'company_name':'长沙景嘉微电子','contact_person':'周副总','contact_phone':'133xxxx2006','source':'以商招商','industry_track':'算力配套','intent_level':'低','status':'待处理','assigned_to':4,'notes':'GPU芯片设计企业，对智算中心算力有兴趣。'},
                {'company_name':'北京格灵深瞳','contact_person':'杨总','contact_phone':'131xxxx2007','source':'网络线索','industry_track':'工业视觉','intent_level':'高','status':'已转化','assigned_to':2,'notes':'AI视觉算法头部企业，已确认意向，正在准备投资方案。'},
                {'company_name':'广州数控','contact_person':'黄经理','contact_phone':'132xxxx2008','source':'展会','industry_track':'装备智能','intent_level':'中','status':'已关闭','assigned_to':3,'notes':'更倾向广州本地扩产，暂时搁置。'},
            ]:
                db.session.add(Lead(**l))
            db.session.commit()
            print(f'✓ 招商线索创建完成（{Lead.query.count()}条）')
        else:
            print('  招商线索已存在，跳过')

        # 9. 招商项目
        if not Project.query.first():
            for p in [
                {'title':'华科创智激光雷达光学模组项目','company_id':4,'stage':'洽谈','amount':5000,'industry_track':'智能感知','owner_id':2,'expected_date':'2026-12','notes':'拟租赁孵化区2000㎡，配套麓宇光电。'},
                {'title':'天准科技AI视觉检测装备华中基地','stage':'签约','amount':3000,'industry_track':'工业视觉','owner_id':2,'expected_date':'2026-10','notes':'已签署意向协议，计划使用标准厂房3000㎡。'},
                {'title':'汇川技术智能控制器生产线','company_id':1,'stage':'落地','amount':8000,'industry_track':'装备智能','owner_id':4,'expected_date':'2026-08','settled_date':'2026-08-15','notes':'已正式落地！为三一提供PLC控制器和伺服驱动。'},
                {'title':'海康机器人湖南区域服务中心','stage':'线索','amount':2000,'industry_track':'工业视觉','owner_id':3,'expected_date':'2027-03','notes':'考虑在益阳设立区域服务中心。'},
                {'title':'景嘉微益阳GPU研发中心','company_id':5,'stage':'洽谈','amount':1500,'industry_track':'算力配套','owner_id':4,'expected_date':'2027-06','notes':'与智算中心联合研发GPU集群管理平台。'},
            ]:
                db.session.add(Project(**p))
            db.session.commit()
            # 线索→项目关联
            gl = Lead.query.filter_by(status='已转化').first()
            fp = Project.query.first()
            if gl and fp:
                gl.converted_project_id = fp.id
                db.session.commit()
            print(f'✓ 招商项目创建完成（{Project.query.count()}个）')
        else:
            print('  招商项目已存在，跳过')

        # 10. 跟进记录
        if not FollowUp.query.first():
            for f in [
                {'project_id':1,'content':'与华科创智陈总视频会议，对方对益阳区位和配套很感兴趣。','next_step':'发送政策包，安排实地考察','contact_person':'陈总','follow_date':'2026-08-10','created_by':2},
                {'project_id':1,'content':'对方CEO计划8月下旬来益阳实地考察。','next_step':'准备接待方案','contact_person':'陈总','follow_date':'2026-08-15','created_by':2},
                {'project_id':2,'content':'完成意向协议签署！天准科技确认在益阳设立华中基地。','next_step':'对接信维电科和金博股份','contact_person':'赵副总','follow_date':'2026-08-20','created_by':2},
                {'project_id':2,'content':'已安排天准技术团队与信维电科对接，下周产线实测。','next_step':'跟进实测结果','contact_person':'赵副总','follow_date':'2026-08-25','created_by':2},
                {'project_id':3,'content':'汇川技术智能控制器产线正式投产！','next_step':'协助与三一签年度合同','contact_person':'王总监','follow_date':'2026-08-15','created_by':4},
                {'project_id':3,'content':'汇川与三一首批供应合同签署，年采购额约2000万元。','next_step':'推动二期扩产','contact_person':'王总监','follow_date':'2026-08-28','created_by':4},
                {'project_id':4,'content':'收到海康机器人在线表单，已回电初步沟通。','next_step':'发送采购需求详情','contact_person':'李总','follow_date':'2026-08-18','created_by':3},
                {'project_id':5,'content':'与景嘉微周副总电话沟通，对GPU集群管理有兴趣。','next_step':'安排技术对接','contact_person':'周副总','follow_date':'2026-08-22','created_by':4},
            ]:
                db.session.add(FollowUp(**f))
            db.session.commit()
            print(f'✓ 跟进记录创建完成（{FollowUp.query.count()}条）')
        else:
            print('  跟进记录已存在，跳过')

        # 11. 招投标记录
        if not BiddingRecord.query.first():
            for b in [
                {'project_name':'三一重工益阳工厂2026年度工业控制器采购招标','bidder_name':'三一重工股份有限公司','winner_name':'汇川技术股份有限公司','bid_amount':2180,'publish_date':'2026-06-15','product_detail':'PLC控制器500套、运动控制器300套','source':'中国招标投标公共服务平台','industry_track':'装备智能'},
                {'project_name':'信维电科MLCC产线AI视觉检测系统采购','bidder_name':'信维电科股份有限公司','winner_name':'苏州天准科技股份有限公司','bid_amount':860,'publish_date':'2026-07-20','product_detail':'AI视觉检测系统10套','source':'湖南招标投标监管网','industry_track':'工业视觉'},
                {'project_name':'金博股份碳基材料智能监测系统招标','bidder_name':'金博碳素股份有限公司','winner_name':None,'bid_amount':0,'publish_date':'2026-08-10','product_detail':'5条产线智能监测系统','source':'湖南招标投标监管网','industry_track':'工业视觉'},
                {'project_name':'益阳智算中心二期液冷散热系统采购','bidder_name':'益阳智算中心运营有限公司','winner_name':'华为数字能源技术有限公司','bid_amount':2950,'publish_date':'2026-08-15','product_detail':'液冷散热系统覆盖500机柜','source':'中央政府采购网','industry_track':'算力配套'},
                {'project_name':'湖南省教育厅等保测评及WAF设备采购','bidder_name':'湖南省教育厅','winner_name':'长亭科技股份有限公司','bid_amount':320,'publish_date':'2026-05-20','product_detail':'等保测评服务、WAF设备采购部署','source':'湖南政府采购网','industry_track':'算力配套'},
            ]:
                db.session.add(BiddingRecord(**b))
            db.session.commit()
            print(f'✓ 招投标记录创建完成（{BiddingRecord.query.count()}条）')
        else:
            print('  招投标记录已存在，跳过')

        # 12. 技术能力（下游专区）
        if not TechCapability.query.first():
            for t in [
                {'chain_company_id':5,'title':'GPU算力集群对外服务','capability_type':'算力服务','description':'大规模GPU集群提供AI训练和推理算力，支持按需租用。相比自建GPU集群可节省70%以上成本。','applicable_scenarios':'大模型训练/微调、AI推理服务、科学计算、渲染农场','contact_info':'智算中心 赵工 0737-XXXXXXX','industry_track':'算力配套','status':'open','published_at':'2026-08-01'},
                {'chain_company_id':5,'title':'虚拟电厂储能系统接入服务','capability_type':'产品供应','description':'全省第二家虚拟电厂已投入运营，为数据中心和制造企业提供储能系统接入和调峰服务，降低用电成本20%-30%。','applicable_scenarios':'数据中心节能、制造企业峰谷套利、新能源消纳','contact_info':'智算中心能源部 0737-XXXXXXX','industry_track':'算力配套','status':'open','published_at':'2026-08-05'},
                {'chain_company_id':1,'title':'路面机械产线AI应用测试环境','capability_type':'产线测试','description':'三一益阳AI数字孪生工厂对外开放产线测试环境，AI方案商可在此验证视觉检测、预测性维护等方案。','applicable_scenarios':'AI视觉检测方案验证、工业软件实测、预测性维护POC','contact_info':'三一数字化部 李工 0737-XXXXXXX','industry_track':'装备智能','status':'open','published_at':'2026-08-10'},
                {'chain_company_id':2,'title':'MLCC产线AI质检方案联合研发','capability_type':'联合研发','description':'信维电科MLCC智能质检大模型项目开放联合研发合作，提供真实产线数据和测试环境。','applicable_scenarios':'AI缺陷检测算法研发、工业大模型训练、质检标准制定','contact_info':'信维电科AI实验室 刘工 0737-XXXXXXX','industry_track':'工业视觉','status':'open','published_at':'2026-08-12'},
                {'chain_company_id':4,'title':'光电传感器微型化封装技术合作','capability_type':'技术合作','description':'麓宇光电依托湖南未来光电技术研究院，对外开放光电传感器微型化封装技术合作。','applicable_scenarios':'可穿戴设备传感器、消费电子微型摄像头、车载激光雷达','contact_info':'麓宇光电研发部 周总监 0737-XXXXXXX','industry_track':'智能感知','status':'open','published_at':'2026-08-15'},
            ]:
                db.session.add(TechCapability(**t))
            db.session.commit()
            print(f'✓ 技术能力创建完成（{TechCapability.query.count()}条）')
        else:
            print('  技术能力已存在，跳过')

        # 13. 供应商企业池
        if not Company.query.filter(Company.company_type == 'supplier').first():
            for s in [
                {'name':'深圳华科创智','company_type':'supplier','industry_track':'智能感知','scale':'中型','city':'深圳','district':'南山区','employee_count':280,'annual_revenue':'3.5亿元','products_services':'光学镀膜材料、非球面镜片、激光雷达光学模组','certifications':'ISO9001, IATF16949, 国家级高新技术企业','advantage_tags':'车规级,光学镀膜,10年经验,华为供应商','lat':22.53,'lng':113.95,'description':'专注于精密光学元器件研发制造。','is_chain_leader':False,'status':'active'},
                {'name':'武汉锐科激光','company_type':'target','industry_track':'智能感知','scale':'大型','city':'武汉','district':'东湖高新区','employee_count':1200,'annual_revenue':'15亿元','products_services':'光纤激光器、半导体激光器、激光加工系统','certifications':'ISO9001, ISO14001, 上市公司','advantage_tags':'上市公司,激光器龙头,国产替代','lat':30.51,'lng':114.42,'description':'国内光纤激光器龙头企业，创业板上市。','is_chain_leader':False,'status':'active'},
                {'name':'苏州天准科技','company_type':'supplier','industry_track':'工业视觉','scale':'中型','city':'苏州','district':'工业园区','employee_count':450,'annual_revenue':'6亿元','products_services':'AI视觉检测装备、精密测量仪器','certifications':'ISO9001, 科创板上市, 国家专精特新小巨人','advantage_tags':'科创板,AI视觉,精密测量','lat':31.32,'lng':120.73,'description':'科创板上市，专注于AI视觉检测和精密测量技术。','is_chain_leader':False,'status':'active'},
                {'name':'深圳朗视光电','company_type':'supplier','industry_track':'工业视觉','scale':'小型','city':'深圳','district':'宝安区','employee_count':120,'annual_revenue':'8000万元','products_services':'工业相机、机器视觉光源、视觉定位系统','certifications':'ISO9001, 国家级高新技术企业','advantage_tags':'工业相机,批量供货,快速交期','lat':22.57,'lng':113.87,'description':'专注于工业相机和视觉光源研发生产，年出货量超10万台。','is_chain_leader':False,'status':'active'},
                {'name':'长沙都正生物','company_type':'target','industry_track':'算力配套','scale':'中型','city':'长沙','district':'高新区','employee_count':300,'annual_revenue':'2亿元','products_services':'AI药物研发平台、生物大数据分析','certifications':'ISO9001, GCP认证, 国家级高新技术企业','advantage_tags':'AI制药,大数据,临床试验','lat':28.22,'lng':112.89,'description':'AI驱动的新药研发企业。','is_chain_leader':False,'status':'active'},
            ]:
                db.session.add(Company(**s))
            db.session.commit()
            print(f'✓ 供应商企业创建完成（{Company.query.filter(Company.company_type.in_(["supplier","target"]), Company.is_chain_leader==False).count()}家）')
        else:
            print('  供应商企业已存在，跳过')

        # 14. 示例响应
        if not DemandResponse.query.first():
            for r in [
                {'demand_id':3,'company_name':'深圳朗视光电','contact_person':'林经理','contact_phone':'133xxxx3001','qualification_desc':'ISO9001认证，国家级高新技术企业，工业相机年出货量超10万台','advantage_desc':'2000万像素工业相机已批量供货给富士康/比亚迪，交期快、价格有竞争力','status':'pending'},
                {'demand_id':3,'company_name':'武汉华工激光','contact_person':'谢总','contact_phone':'139xxxx3002','qualification_desc':'上市公司，激光设备行业龙头','advantage_desc':'自主研发的智能视觉定位系统可用于MLCC产线精确定位','status':'reviewing'},
                {'demand_id':1,'company_name':'深圳汇川技术','contact_person':'王总监','contact_phone':'137xxxx2004','qualification_desc':'上市公司，伺服驱动市占率第一','advantage_desc':'已在益阳投产，可提供本地化服务和快速响应','status':'approved'},
            ]:
                db.session.add(DemandResponse(**r))
            db.session.commit()
            print(f'✓ 示例响应创建完成（{DemandResponse.query.count()}条）')
        else:
            print('  示例响应已存在，跳过')

        # 15. 技术攻关悬赏
        if not TechChallenge.query.first():
            for c in [
                {'chain_company_id':1,'title':'路面机械焊接工艺AI参数优化','challenge_type':'算法攻关','description':'三一益阳工厂焊接工序需优化工艺参数，寻求基于强化学习的参数自适应系统，将焊接合格率从92%提升至98%以上。','reward':'30万元','deadline':'2027-03-31','requirements':'需具备工业AI算法经验','contact_info':'三一数字化部 李工 0737-XXXXXXX','industry_track':'装备智能','status':'open','published_at':'2026-08-20'},
                {'chain_company_id':2,'title':'MLCC缺陷检测小样本学习算法','challenge_type':'算法攻关','description':'MLCC器件缺陷种类多但样本量少，需小样本学习算法实现新缺陷类型快速适配。','reward':'20万元','deadline':'2027-06-30','requirements':'高校/企业均可揭榜','contact_info':'信维电科AI实验室 刘工 0737-XXXXXXX','industry_track':'工业视觉','status':'open','published_at':'2026-08-18'},
                {'chain_company_id':5,'title':'GPU集群智能调度系统研发','challenge_type':'技术难题','description':'2000+GPU节点集群的任务调度效率优化，GPU利用率从65%提升至85%以上。','reward':'50万元','deadline':'2027-09-30','requirements':'有大规模集群调度经验','contact_info':'智算中心 赵工 0737-XXXXXXX','industry_track':'算力配套','status':'open','published_at':'2026-08-22'},
            ]:
                db.session.add(TechChallenge(**c))
            db.session.commit()
            print(f'✓ 技术悬赏创建完成（{TechChallenge.query.count()}条）')
        else:
            print('  技术悬赏已存在，跳过')

        print('\n🎉 种子数据初始化完成！')
        print('运行 python3 app.py 启动平台，访问 http://localhost:5096')


if __name__ == '__main__':
    seed_all()
