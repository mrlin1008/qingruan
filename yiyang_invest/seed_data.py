"""
益阳高新区智慧招商平台 — 种子数据
"""
import os
import sys
from werkzeug.security import generate_password_hash
from app import app, db
from models import (User, ParkInfo, IndustryChain, Company, Space, Policy, Article, ProcurementDemand, ParkImage)

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

        print('\n🎉 种子数据初始化完成！')
        print('运行 python3 app.py 启动平台，访问 http://localhost:5096')


if __name__ == '__main__':
    seed_all()
