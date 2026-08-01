"""
益阳高新区智慧招商平台 — 种子数据
"""
import os
import sys
from werkzeug.security import generate_password_hash
from app import app, db
from models import (User, ParkInfo, IndustryChain, Space, Policy, Article)

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
     'publish_date': '2026-06-25', 'is_published': True},
    {'title': '湖南未来光电技术研究院落地运营', 'category': '产业资讯',
     'summary': '已与湖南师范大学共建湖南未来光电技术研究院，落地麓宇光电电致变色、激光雷达AI感知项目。',
     'publish_date': '2026-06-10', 'is_published': True},
    {'title': '益阳高新区195家规上工业，近30家布局AI业务', 'category': '园区动态',
     'summary': '全区现有规上工业195家，三一、益阳橡机、信维电科、金博股份等龙头企业具备智能化改造基础。',
     'publish_date': '2026-05-15', 'is_published': True},
    {'title': '益阳智算中心正式投入使用', 'category': '产业资讯',
     'summary': '智算中心可提供AI训练、推理算力服务，为区域AI产业发展提供算力底座。',
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

        print('\n🎉 种子数据初始化完成！')
        print('运行 python3 app.py 启动平台，访问 http://localhost:5096')


if __name__ == '__main__':
    seed_all()
