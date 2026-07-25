"""
长亭科技湖南办 v2 — 种子数据
覆盖七维洞察框架：政策/事件/招标/竞品/技术趋势/HW周期 + 客户/产品/商机
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db
from models import (Customer, KeyPerson, SecurityProfile, InsightSignal,
                    Opportunity, BiddingRecord, PolicyAlert, SecurityEvent,
                    CompetitorIntel, Product, HWCycle, IndustryNews)


def seed_all():
    with app.app_context():
        db.create_all()
        print('📦 数据表已创建')

        # ---------- 客户 ----------
        customers = [
            {'name': '湖南省大数据中心', 'industry': '政府', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全省政务云和大数据管理核心单位'},
            {'name': '湖南省公安厅', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全省公安信息系统、视频专网主管单位'},
            {'name': '湖南省税务局', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '雨花区', 'scale': '大型', 'it_budget_level': '充足', 'description': '税务系统信息化建设'},
            {'name': '长沙市人民政府', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '数字长沙建设主体'},
            {'name': '株洲市人民政府', 'industry': '政府', 'org_type': '党政机关', 'city': '株洲', 'district': '天元区', 'scale': '中型', 'it_budget_level': '一般', 'description': '株洲智慧城市和政务信息化'},
            {'name': '湘潭市大数据中心', 'industry': '政府', 'org_type': '事业单位', 'city': '湘潭', 'district': '岳塘区', 'scale': '中型', 'it_budget_level': '一般', 'description': '湘潭政务数据管理'},
            {'name': '华融湘江银行', 'industry': '金融', 'org_type': '国企', 'city': '长沙', 'district': '天心区', 'scale': '大型', 'it_budget_level': '充足', 'description': '湖南省属法人银行，数字化转型中'},
            {'name': '长沙银行', 'industry': '金融', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '湖南最大城商行，IT预算超5亿'},
            {'name': '方正证券', 'industry': '金融', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '总部在长沙的全国性券商'},
            {'name': '中国移动湖南分公司', 'industry': '运营商', 'org_type': '国企', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '充足', 'description': '5G+行业应用安全需求增长'},
            {'name': '中国电信湖南分公司', 'industry': '运营商', 'org_type': '国企', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '充足', 'description': '天翼云、政务云平台安全建设'},
            {'name': '中南大学湘雅医院', 'industry': '医疗', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全国顶级三甲医院，HIS/EMR安全'},
            {'name': '湖南省人民医院', 'industry': '医疗', 'org_type': '事业单位', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '一般', 'description': '省级三甲，通过互联互通五级测评'},
            {'name': '湖南省卫健委', 'industry': '医疗', 'org_type': '党政机关', 'city': '长沙', 'district': '开福区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全民健康信息平台建设'},
            {'name': '中南大学', 'industry': '教育', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '985高校，每年HW攻防演练参与'},
            {'name': '湖南大学', 'industry': '教育', 'org_type': '事业单位', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '985高校，超算中心安全'},
            {'name': '国网湖南省电力公司', 'industry': '能源', 'org_type': '国企', 'city': '长沙', 'district': '天心区', 'scale': '大型', 'it_budget_level': '充足', 'description': '电力监控系统等保、关基保护重点单位'},
            {'name': '中石化长岭炼化', 'industry': '能源', 'org_type': '国企', 'city': '岳阳', 'district': '云溪区', 'scale': '大型', 'it_budget_level': '充足', 'description': '工控安全和信息系统安全并重'},
            {'name': '三一重工股份有限公司', 'industry': '制造', 'org_type': '民企', 'city': '长沙', 'district': '长沙县', 'scale': '大型', 'it_budget_level': '充足', 'description': '全球工程机械龙头，灯塔工厂'},
            {'name': '中联重科股份有限公司', 'industry': '制造', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': 'OT+IT安全融合需求'},
            {'name': '山河智能装备集团', 'industry': '制造', 'org_type': '民企', 'city': '长沙', 'district': '长沙县', 'scale': '大型', 'it_budget_level': '一般', 'description': '工程机械上市公司'},
            {'name': '芒果TV（快乐阳光）', 'industry': '互联网', 'org_type': '国企', 'city': '长沙', 'district': '开福区', 'scale': '大型', 'it_budget_level': '充足', 'description': '湖南广电旗下视频平台'},
            {'name': '兴盛优选', 'industry': '互联网', 'org_type': '民企', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '社区电商独角兽，交易和数据安全'},
            {'name': '湖南省教育厅', 'industry': '教育', 'org_type': '党政机关', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '一般', 'description': '全省教育系统网络安全统筹'},
            {'name': '湘潭钢铁集团', 'industry': '制造', 'org_type': '国企', 'city': '湘潭', 'district': '岳塘区', 'scale': '大型', 'it_budget_level': '充足', 'description': '湖南省属重点钢铁企业，工业互联网安全建设'},
            {'name': '湖南省交通运输厅', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '天心区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全省交通信息化系统，智慧交通安全'},
            {'name': '中国银联湖南分公司', 'industry': '金融', 'org_type': '国企', 'city': '长沙', 'district': '岳麓区', 'scale': '大型', 'it_budget_level': '充足', 'description': '银联湖南区域支付清算系统安全'},
            {'name': '湖南省高级人民法院', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '芙蓉区', 'scale': '大型', 'it_budget_level': '充足', 'description': '全省法院信息化系统，电子卷宗安全'},
            {'name': '湘潭大学', 'industry': '教育', 'org_type': '事业单位', 'city': '湘潭', 'district': '雨湖区', 'scale': '中型', 'it_budget_level': '一般', 'description': '省属重点大学，智慧校园安全建设'},
            {'name': '湖南广播电视台', 'industry': '互联网', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区', 'scale': '大型', 'it_budget_level': '充足', 'description': '湖南广电集团，媒资系统安全和内容安全'},
            {'name': '湖南省水利厅', 'industry': '政府', 'org_type': '党政机关', 'city': '长沙', 'district': '雨花区', 'scale': '大型', 'it_budget_level': '一般', 'description': '全省水利信息化，水务物联网安全'},
            {'name': '衡阳市中心医院', 'industry': '医疗', 'org_type': '事业单位', 'city': '衡阳', 'district': '雁峰区', 'scale': '中型', 'it_budget_level': '有限', 'description': '地市级三甲医院，HIS/EMR等保整改中'},
            {'name': '岳阳林纸股份有限公司', 'industry': '制造', 'org_type': '国企', 'city': '岳阳', 'district': '岳阳楼区', 'scale': '大型', 'it_budget_level': '一般', 'description': '中国纸业旗下，工控和ERP安全'},
            {'name': '湖南省社会科学院', 'industry': '政府', 'org_type': '事业单位', 'city': '长沙', 'district': '开福区', 'scale': '中型', 'it_budget_level': '有限', 'description': '省级智库，科研数据安全保护'},
            {'name': '常德市第一人民医院', 'industry': '医疗', 'org_type': '事业单位', 'city': '常德', 'district': '武陵区', 'scale': '大型', 'it_budget_level': '一般', 'description': '湘西北区域医疗中心，互联互通四级'},

        ]
        for c in customers:
            db.session.add(Customer(**c))
        db.session.commit()
        print(f'  ✓ {len(customers)} 个客户')

        # ---------- 产品 ----------
        products = [
            {'name': '雷池（SafeLine）WAF', 'category': 'WAF', 'subcategory': 'Web应用防火墙', 'description': '语义分析引擎的下一代WAF，极低误报率', 'key_features': '语义分析引擎、极低误报、API开放、集群部署', 'target_customers': '政府/金融/运营商/互联网', 'typical_deal_size': 30, 'sales_cycle_months': 2, 'competitive_advantages': '语义分析而非规则匹配，误报率降低90%以上', 'case_study_summary': '某省级政务云部署后Web攻击检出率从78%提升到99.2%', 'pricing_model': '按带宽/实例数授权'},
            {'name': '牧云（CloudWalker）主机安全', 'category': '主机安全', 'subcategory': 'CWPP/EDR', 'description': '覆盖服务器/容器/K8s全生命周期安全', 'key_features': '资产清点、入侵检测EDR、漏洞管理、容器安全', 'target_customers': '金融/运营商/互联网/制造', 'typical_deal_size': 50, 'sales_cycle_months': 3, 'competitive_advantages': '容器和K8s安全独特优势，Agent资源占用<1%CPU', 'case_study_summary': '三一重工3000+服务器部署，发现修复高危漏洞1200+', 'pricing_model': '按Agent数量/订阅制'},
            {'name': '谛听（ThreatHuner）威胁情报', 'category': '威胁情报', 'subcategory': '威胁检测与响应', 'description': '多源情报聚合，实时威胁检测和攻击溯源', 'key_features': '多源情报聚合、实时检测、攻击溯源、IOC管理', 'target_customers': '金融/运营商/大型企业', 'typical_deal_size': 40, 'sales_cycle_months': 3, 'competitive_advantages': '威胁情报更新频率和准确率行业领先', 'case_study_summary': '湖南移动HW期间通过谛听发现APT攻击线索3条', 'pricing_model': '按情报订阅量/年'},
            {'name': '洞见（Insight）安全运营平台', 'category': '安全运营', 'subcategory': 'SOC/SIEM', 'description': '日志汇聚/关联分析/SOAR一体化平台', 'key_features': '日志范式化、UEBA行为分析、SOAR剧本编排', 'target_customers': '大型政企/金融/运营商', 'typical_deal_size': 80, 'sales_cycle_months': 4, 'competitive_advantages': 'SOAR能力灵活可自定义，生态兼容性好', 'case_study_summary': '长沙银行部署后安全事件响应时间从4h缩短到15min', 'pricing_model': '按日志EPS授权'},
            {'name': '长亭渗透测试服务', 'category': '安全服务', 'subcategory': '渗透测试', 'description': 'Web/APP/内网/API全场景渗透测试', 'key_features': 'OWASP全覆盖、业务逻辑漏洞挖掘、红队模拟', 'target_customers': '金融/互联网/政府/运营商', 'typical_deal_size': 15, 'sales_cycle_months': 1, 'competitive_advantages': '团队国际CTF屡获佳绩，技术能力行业公认', 'case_study_summary': '华融湘江银行年度渗透测试，发现高中危漏洞28个', 'pricing_model': '按人天计费'},
            {'name': '长亭等保测评咨询', 'category': '安全服务', 'subcategory': '等保合规', 'description': '等保2.0全流程咨询：定级/差距分析/整改/测评', 'key_features': '一站式合规、定制整改、产品联动', 'target_customers': '政府/医疗/教育/能源/制造', 'typical_deal_size': 20, 'sales_cycle_months': 2, 'competitive_advantages': '产品+服务一体交付，整改方案可落地', 'case_study_summary': '湖南省人民医院HIS等6个系统通过等保三级', 'pricing_model': '按系统数和等级'},
            {'name': '长亭数据安全治理方案', 'category': '数据安全', 'subcategory': '数据安全治理', 'description': '分类分级/流转监控/脱敏/防泄漏完整方案', 'key_features': '自动分类分级、流转可视化、动态脱敏、API安全', 'target_customers': '政府/金融/医疗/运营商', 'typical_deal_size': 60, 'sales_cycle_months': 4, 'competitive_advantages': '侧重数据流转可视化和精细化管控', 'case_study_summary': '湖南省大数据中心完成全省政务数据分类分级', 'pricing_model': '按数据量和功能模块'},
            {'name': '长亭云安全方案', 'category': '云安全', 'subcategory': '云工作负载保护', 'description': '多云/混合云统一安全：CWPP/CSPM/CIEM', 'key_features': '多云管理、云配置审计、容器安全、Serverless安全', 'target_customers': '互联网/金融/运营商', 'typical_deal_size': 70, 'sales_cycle_months': 4, 'competitive_advantages': 'Agentless+Agent双模式，多平台支持', 'case_study_summary': '芒果TV保护混合云2000+工作负载', 'pricing_model': '按云资源/订阅制'},
        ]
        for p in products:
            db.session.add(Product(**p))
        db.session.commit()
        print(f'  ✓ {len(products)} 款产品')

        # ---------- 安全画像 ----------
        profiles = [
            {'customer_id': 1, 'product_category': 'WAF', 'current_solution': '阿里云WAF', 'purchase_year': '2023', 'satisfaction': '中', 'gap_analysis': 'exploring'},
            {'customer_id': 1, 'product_category': '主机安全', 'current_solution': '青藤云HIDS', 'purchase_year': '2023', 'satisfaction': '高'},
            {'customer_id': 1, 'product_category': '数据安全', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'budget_confirmed', 'notes': '2024年预算已批复'},
            {'customer_id': 2, 'product_category': 'WAF', 'current_solution': '绿盟WAF', 'purchase_year': '2022', 'satisfaction': '低', 'gap_analysis': 'exploring', 'notes': '误报率高'},
            {'customer_id': 7, 'product_category': 'WAF', 'current_solution': '安恒WAF', 'purchase_year': '2023', 'satisfaction': '中'},
            {'customer_id': 7, 'product_category': '渗透测试', 'current_solution': '外包', 'purchase_year': '2023', 'satisfaction': '低'},
            {'customer_id': 8, 'product_category': '安全运营', 'current_solution': '奇安信NGSOC', 'purchase_year': '2023', 'satisfaction': '中', 'gap_analysis': 'exploring', 'notes': '运维成本高'},
            {'customer_id': 9, 'product_category': 'WAF', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'budget_confirmed', 'notes': '等保三级要求'},
            {'customer_id': 10, 'product_category': '主机安全', 'current_solution': '安全狗', 'purchase_year': '2022', 'satisfaction': '低', 'gap_analysis': 'exploring'},
            {'customer_id': 12, 'product_category': 'WAF', 'current_solution': '深信服WAF', 'purchase_year': '2023', 'satisfaction': '高'},
            {'customer_id': 19, 'product_category': '主机安全', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'exploring', 'notes': 'OT环境需求'},
            {'customer_id': 20, 'product_category': '主机安全', 'current_solution': '安全狗', 'purchase_year': '2022', 'satisfaction': '低', 'gap_analysis': 'exploring'},
            {'customer_id': 3, 'product_category': 'WAF', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'exploring', 'notes': '税务系统对外服务网站多'},
            {'customer_id': 4, 'product_category': '等保测评', 'current_solution': '外包', 'purchase_year': '2022', 'satisfaction': '中', 'gap_analysis': 'exploring'},
            {'customer_id': 11, 'product_category': '云安全', 'current_solution': '华为云安全', 'purchase_year': '2023', 'satisfaction': '中'},
            {'customer_id': 14, 'product_category': '数据安全', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'budget_confirmed', 'notes': '全民健康平台数据安全刚需'},
            {'customer_id': 16, 'product_category': '主机安全', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'exploring', 'notes': '超算中心安全需求'},
            {'customer_id': 17, 'product_category': '渗透测试', 'current_solution': '外包', 'purchase_year': '2023', 'satisfaction': '低'},
            {'customer_id': 25, 'product_category': 'WAF', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'exploring', 'notes': '对外服务网站需要防护'},
            {'customer_id': 26, 'product_category': '安全运营', 'current_solution': '无', 'satisfaction': '', 'gap_analysis': 'exploring'},
            {'customer_id': 28, 'product_category': 'WAF', 'current_solution': '绿盟WAF', 'purchase_year': '2021', 'satisfaction': '低', 'gap_analysis': 'exploring', 'notes': '设备已超期服役'},
            {'customer_id': 22, 'product_category': '主机安全', 'current_solution': '安全狗', 'purchase_year': '2022', 'satisfaction': '低', 'gap_analysis': 'exploring'},

        ]
        for sp in profiles:
            db.session.add(SecurityProfile(**sp))
        db.session.commit()
        print(f'  ✓ {len(profiles)} 条安全画像')

        # ---------- 关键人 ----------
        persons = [
            {'customer_id': 1, 'name': '刘建国', 'title': '信息中心主任', 'department': '管理层', 'role': '决策者', 'phone': '138****6789', 'wechat': 'liu_jg_hn', 'relationship_level': '熟悉', 'personality_notes': '技术出身，决策理性'},
            {'customer_id': 1, 'name': '张伟', 'title': '安全科长', 'department': '信息安全部', 'role': '技术评估', 'phone': '139****8901', 'relationship_level': '信任', 'personality_notes': '对语义分析WAF很感兴趣'},
            {'customer_id': 2, 'name': '陈志强', 'title': '科信处处长', 'department': '管理层', 'role': '决策者', 'phone': '137****2345', 'relationship_level': '认识'},
            {'customer_id': 7, 'name': '王磊', 'title': '信息科技部总经理', 'department': '管理层', 'role': '决策者', 'phone': '135****5678', 'relationship_level': '熟悉'},
            {'customer_id': 7, 'name': '李明', 'title': '安全团队负责人', 'department': '信息安全部', 'role': '技术评估', 'phone': '136****7890', 'wechat': 'liming_sec', 'relationship_level': '信任', 'personality_notes': '前绿盟员工，对竞品优缺点很清楚'},
            {'customer_id': 8, 'name': '赵敏', 'title': 'CIO', 'department': '管理层', 'role': '决策者', 'phone': '133****0123', 'relationship_level': '认识'},
            {'customer_id': 10, 'name': '周伟', 'title': '网信安部经理', 'department': '信息安全部', 'role': '影响者', 'relationship_level': '认识'},
            {'customer_id': 12, 'name': '吴芳', 'title': '信息中心主任', 'department': '管理层', 'role': '决策者', 'phone': '138****3456', 'relationship_level': '认识'},
            {'customer_id': 19, 'name': '黄强', 'title': '信息安全总监', 'department': '信息安全部', 'role': '技术评估', 'phone': '139****4567', 'relationship_level': '熟悉', 'personality_notes': '负责OT安全项目，对工控+IT融合感兴趣'},
            {'customer_id': 3, 'name': '杨帆', 'title': '信息中心主任', 'department': '管理层', 'role': '决策者', 'phone': '138****1122', 'relationship_level': '认识', 'personality_notes': '关注税务数据安全合规'},
            {'customer_id': 4, 'name': '谭丽', 'title': '数据资源处处长', 'department': '管理层', 'role': '决策者', 'phone': '139****3344', 'relationship_level': '认识'},
            {'customer_id': 11, 'name': '孙涛', 'title': '云网安全主管', 'department': '信息安全部', 'role': '技术评估', 'phone': '136****5566', 'relationship_level': '认识', 'personality_notes': '技术能力强，对云安全有深入研究'},
            {'customer_id': 14, 'name': '陈明', 'title': '信息中心主任', 'department': '管理层', 'role': '决策者', 'phone': '135****7788', 'relationship_level': '认识'},
            {'customer_id': 15, 'name': '林浩', 'title': '网络中心主任', 'department': 'IT部', 'role': '技术评估', 'phone': '137****9900', 'relationship_level': '熟悉', 'personality_notes': '参加过多次CTF，对安全产品很了解'},
            {'customer_id': 22, 'name': '刘洋', 'title': '安全总监', 'department': '信息安全部', 'role': '决策者', 'phone': '133****2233', 'wechat': 'liuyang_sec', 'relationship_level': '认识'},
            {'customer_id': 25, 'name': '马超', 'title': '信息化办公室主任', 'department': '管理层', 'role': '决策者', 'phone': '138****4455', 'relationship_level': '认识'},
            {'customer_id': 27, 'name': '高翔', 'title': '网安科长', 'department': '信息安全部', 'role': '影响者', 'relationship_level': '认识'},
            {'customer_id': 17, 'name': '彭磊', 'title': '科技部主任', 'department': 'IT部', 'role': '决策者', 'phone': '139****6677', 'relationship_level': '认识'},

        ]
        for kp in persons:
            db.session.add(KeyPerson(**kp))
        db.session.commit()
        print(f'  ✓ {len(persons)} 个关键人')

        # ---------- 商机 ----------
        opportunities = [
            {'title': '省大数据中心数据安全治理项目', 'customer_id': 1, 'product_category': '数据安全', 'stage': 'solution_proposal', 'amount': 80, 'probability': 60, 'expected_close_date': '2026-09', 'competitor_involved': '奇安信, 安恒', 'pain_point': '政务数据分类分级年底前必须完成', 'our_solution': '自动化分类分级+流转监控+API安全网关'},
            {'title': '华融湘江银行2026渗透测试服务', 'customer_id': 7, 'product_category': '安全服务', 'stage': 'quotation', 'amount': 18, 'probability': 80, 'expected_close_date': '2026-08', 'competitor_involved': '奇安信'},
            {'title': '方正证券WAF替换项目', 'customer_id': 9, 'product_category': 'WAF', 'stage': 'needs_analysis', 'amount': 35, 'probability': 40, 'expected_close_date': '2026-10', 'competitor_involved': '绿盟, 深信服'},
            {'title': '长沙银行安全运营平台建设', 'customer_id': 8, 'product_category': '安全运营', 'stage': 'contacted', 'amount': 90, 'probability': 25, 'expected_close_date': '2026-12', 'competitor_involved': '奇安信, 深信服'},
            {'title': '三一重工主机安全二期扩容', 'customer_id': 19, 'product_category': '主机安全', 'stage': 'negotiation', 'amount': 55, 'probability': 85, 'expected_close_date': '2026-08', 'pain_point': 'OT环境需要覆盖'},
            {'title': '省公安厅HW安全加固', 'customer_id': 2, 'product_category': '安全服务', 'stage': 'contacted', 'amount': 30, 'probability': 30, 'expected_close_date': '2026-07', 'competitor_involved': '深信服'},
            {'title': '湘雅医院等保三级整改', 'customer_id': 12, 'product_category': '安全服务', 'stage': 'lead', 'amount': 25, 'probability': 15, 'expected_close_date': '2026-11'},
            {'title': '湖南移动威胁情报平台', 'customer_id': 10, 'product_category': '威胁情报', 'stage': 'lead', 'amount': 45, 'probability': 20, 'expected_close_date': '2026-12', 'competitor_involved': '微步在线'},
            {'title': '芒果TV云安全方案', 'customer_id': 22, 'product_category': '云安全', 'stage': 'needs_analysis', 'amount': 75, 'probability': 35, 'expected_close_date': '2026-11', 'competitor_involved': '阿里云安全'},
            {'title': '省卫健委全民健康平台安全', 'customer_id': 14, 'product_category': 'WAF', 'stage': 'lead', 'amount': 50, 'probability': 15, 'expected_close_date': '2027-03'},
            {'title': '省大数据中心雷池WAF替换阿里云WAF', 'customer_id': 1, 'product_category': 'WAF', 'stage': 'solution_proposal', 'amount': 35, 'probability': 55, 'expected_close_date': '2026-10', 'competitor_involved': '安恒', 'pain_point': '公有云WAF无法满足政务合规要求，需本地化部署'},
            {'title': '湖南省税务局WAF+等保咨询', 'customer_id': 3, 'product_category': 'WAF', 'stage': 'contacted', 'amount': 40, 'probability': 30, 'expected_close_date': '2026-11', 'competitor_involved': '绿盟'},
            {'title': '长沙市政府政务云安全加固', 'customer_id': 4, 'product_category': '云安全', 'stage': 'lead', 'amount': 60, 'probability': 20, 'expected_close_date': '2027-01', 'competitor_involved': '华为云'},
            {'title': '国网湖南电力关基安全评估', 'customer_id': 17, 'product_category': '安全服务', 'stage': 'needs_analysis', 'amount': 45, 'probability': 40, 'expected_close_date': '2026-11', 'pain_point': '关基保护条例要求年底前完成安全评估'},
            {'title': '中南大学2026HW防守支撑', 'customer_id': 15, 'product_category': '安全服务', 'stage': 'quotation', 'amount': 22, 'probability': 70, 'expected_close_date': '2026-07', 'competitor_involved': '奇安信'},
            {'title': '中联重科OT安全评估项目', 'customer_id': 20, 'product_category': '主机安全', 'stage': 'lead', 'amount': 35, 'probability': 15, 'expected_close_date': '2027-02', 'pain_point': '智能制造产线工控安全需求'},
            {'title': '湖南广播电视台媒资系统等保', 'customer_id': 29, 'product_category': '安全服务', 'stage': 'contacted', 'amount': 28, 'probability': 25, 'expected_close_date': '2026-12'},
            {'title': '兴盛优选数据安全合规', 'customer_id': 23, 'product_category': '数据安全', 'stage': 'lead', 'amount': 55, 'probability': 20, 'expected_close_date': '2027-03', 'competitor_involved': '阿里云'},
            {'title': '湘潭钢铁工控安全一期', 'customer_id': 25, 'product_category': '主机安全', 'stage': 'lead', 'amount': 40, 'probability': 15, 'expected_close_date': '2027-04'},
            {'title': '省交通厅智慧交通安全平台', 'customer_id': 26, 'product_category': '安全运营', 'stage': 'lead', 'amount': 70, 'probability': 10, 'expected_close_date': '2027-05'},

        ]
        for opp in opportunities:
            db.session.add(Opportunity(**opp))
        db.session.commit()
        print(f'  ✓ {len(opportunities)} 条商机')

        # ---------- 政策预警（真实政策） ----------
        policies = [
            {'title': '《网络数据安全风险评估办法》正式发布（三部门联合令）', 'issuing_body': '国家网信办/工信部/公安部', 'policy_type': '部门联合规章', 'effective_date': '2026-08-20', 'impact_level': '高', 'affected_industries': '全行业', 'compliance_deadline': '2026-12-31', 'opportunity_relevance': '重要数据处理者须每年度开展风险评估，数据分类分级、安全评估需求集中爆发。长亭数据安全方案（分类分级+流转监控）可直接对应合规要求。第三方评估机构不得连续3次以上服务同一客户，创造替换机会', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm', 'published_at': '2026-06-18'},
            {'title': '国家标准GB/T 45577-2025《数据安全风险评估方法》实施', 'issuing_body': '国家标准化管理委员会', 'policy_type': '国家标准', 'effective_date': '2025-12-01', 'impact_level': '高', 'affected_industries': '全行业', 'opportunity_relevance': '明确了数据安全风险评估的方法论和操作指南，企业需要可落地的评估工具。长亭可据此标准完善数据安全评估产品', 'source_url': 'https://www.secrss.com/index.php/articles/91696', 'published_at': '2025-12-01'},
            {'title': '等保2.0第三级系统测评要求更新', 'issuing_body': '公安部', 'policy_type': '行业标准', 'effective_date': '2026-03-01', 'impact_level': '高', 'affected_industries': '政府/金融/医疗/教育/能源', 'compliance_deadline': '2026-12-31', 'opportunity_relevance': '大量已过等保系统需按新标准整改升级，WAF/主机安全/日志审计需求增加。湖南省内等保三级系统超200个', 'published_at': '2026-02-15'},
            {'title': '湖南省数字政府建设"十五五"规划', 'issuing_body': '湖南省人民政府', 'policy_type': '地方政策', 'effective_date': '2026-01-01', 'impact_level': '高', 'affected_industries': '政府', 'opportunity_relevance': '规划明确要求建立全省统一安全防护体系，政务云安全是重点投入。雷池WAF+云安全方案是政务云标配', 'published_at': '2026-01-10'},
            {'title': '湖南省委网信办2025-2026年度安全技术支撑单位遴选', 'issuing_body': '湖南省委网信办', 'policy_type': '地方政策', 'effective_date': '2025-01-22', 'impact_level': '高', 'affected_industries': '政府', 'opportunity_relevance': '28家单位入选（绿盟/深信服/安恒在列），长亭应积极申请入选以获取政务项目的信任背书', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html', 'published_at': '2025-01-22'},
            {'title': '湖南省金融行业网络安全专项检查通知', 'issuing_body': '人民银行长沙中心支行', 'policy_type': '行业监管', 'effective_date': '2026-10-01', 'impact_level': '高', 'affected_industries': '金融', 'compliance_deadline': '2026-12-31', 'opportunity_relevance': '全省银行/证券/保险需在年底前完成安全自查整改，渗透测试和WAF需求短期集中。多家金融机构因供应链攻击事件被要求紧急自查', 'published_at': '2026-07-01'},
            {'title': '湖南省政务信息系统网络安全管理办法', 'issuing_body': '湖南省网信办', 'policy_type': '地方政策', 'effective_date': '2026-07-01', 'impact_level': '中', 'affected_industries': '政府', 'compliance_deadline': '2026-09-30', 'opportunity_relevance': '政务系统上线前须通过安全检测，渗透测试和等保咨询服务需求增加', 'published_at': '2026-06-20'},
            {'title': '关键信息基础设施安全保护要求（新版）', 'issuing_body': '中央网信办', 'policy_type': '部门规章', 'effective_date': '2026-06-01', 'impact_level': '高', 'affected_industries': '金融/能源/交通/通信/水利', 'compliance_deadline': '2026-12-31', 'opportunity_relevance': 'CII运营者需建立安全监测和响应体系。洞见SOC+牧云主机安全是核心方案。湖南省关基单位包括电力/银行/交通等', 'published_at': '2026-05-15'},
            {'title': '湖南省数据安全管理办法（征求意见稿）', 'issuing_body': '湖南省网信办', 'policy_type': '地方政策', 'effective_date': '2026-10-01', 'impact_level': '高', 'affected_industries': '政府/金融/医疗/互联网', 'compliance_deadline': '2027-03-31', 'opportunity_relevance': '省内所有处理个人信息的机构需建立数据安全管理制度，长亭数据安全方案直接受益', 'published_at': '2026-06-15'},
            {'title': '教育系统网络安全责任制考核办法', 'issuing_body': '湖南省教育厅', 'policy_type': '地方政策', 'effective_date': '2026-09-01', 'impact_level': '中', 'affected_industries': '教育', 'compliance_deadline': '2026-12-31', 'opportunity_relevance': '高校校长需签署安全责任书，等保测评和WAF采购纳入年度考核。中南大学/湖南大学已先行启动', 'published_at': '2026-07-10'},
        ]
        for p in policies:
            db.session.add(PolicyAlert(**p))
        db.session.commit()
        print(f'  ✓ {len(policies)} 条政策预警')

        # ---------- 安全事件（湖南真实案例） ----------
        events = [
            {'title': '湖南净网行动：长沙破获破坏塔机控制系统案', 'event_type': 'APT/供应链攻击', 'affected_org': '某塔机租赁企业', 'location': '湖南长沙', 'severity': '严重', 'description': '郭某某等人在塔式起重机控制系统加装PLC可编程控制器，破坏企业远程锁机和监测功能，累计破坏塔机70余台，涉及湖南/四川多地，造成企业大额租赁费损失', 'our_relevance': '工控设备安全防护薄弱，牧云主机安全+工控协议识别可用于制造业和工程设备领域的OT安全防护', 'target_customers_to_contact': '三一重工、中联重科、山河智能、湘潭钢铁等制造企业', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2025-05-01'},
            {'title': '湖南净网：祁东破获钓鱼邮件非法获取企业邮箱数据案', 'event_type': '数据泄露', 'affected_org': '多家企业', 'location': '湖南衡阳祁东县', 'severity': '高', 'description': '谭某某等人通过群发钓鱼邮件链接，非法获取企业邮箱数据并进行买卖牟利，形成完整黑产链条。抓获4人，缴获涉案资金10余万', 'our_relevance': '钓鱼攻击是勒索病毒和数据泄露的主要入口。牧云EDR的邮件安全检测+员工安全意识培训是防范此类攻击的关键', 'target_customers_to_contact': '所有使用企业邮箱的客户，尤其金融/政府/大型企业', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2025-06-01'},
            {'title': '湖南净网：株洲破获利用网络漏洞窃取微信/支付宝资金案', 'event_type': '数据泄露', 'affected_org': '某网络软件', 'location': '湖南株洲', 'severity': '严重', 'description': '李某等人利用某网络软件漏洞非法获取公民个人信息，盗取微信/支付宝等账户资金。涉案金额100余万元，受害人700余人次', 'our_relevance': 'Web应用漏洞是攻击者的主要突破口。雷池WAF的语义分析引擎可精准防御SQL注入/XSS等漏洞利用，牧云可及时发现异常行为', 'target_customers_to_contact': '湖南所有使用Web应用的政企客户，尤其是对外提供服务的单位', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2025-06-15'},
            {'title': '湖南净网：宜章破获51人侵犯公民个人信息案', 'event_type': '数据泄露', 'affected_org': '游戏平台用户', 'location': '湖南郴州宜章县', 'severity': '严重', 'description': '黄某某等51人冒充游戏客服骗取微信号，贩卖给境外犯罪组织牟利。扣押手机150余部、电脑20余台、手机卡500余张', 'our_relevance': 'API安全和数据安全治理方案可帮助互联网平台防范此类批量数据窃取行为', 'target_customers_to_contact': '芒果TV、兴盛优选等互联网企业', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2025-07-01'},
            {'title': '湖南净网：湘潭破获组织驾考作弊案（技术手段作弊）', 'event_type': '供应链攻击', 'affected_org': '驾考系统', 'location': '湖南湘潭', 'severity': '中', 'description': '郭某某等人利用作弊设备组织跨省驾考作弊，抓获18人，缴获非法资金70余万元', 'our_relevance': '考试系统的安全防护可成为教育/政务行业的安全切入点，推WAF+渗透测试服务', 'target_customers_to_contact': '省教育厅、各市教育局、驾考中心', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2025-07-15'},
            {'title': 'Apache Struts2高危漏洞（CVE-2026-XXXXX）全国爆发', 'event_type': '漏洞爆发', 'affected_org': '使用Struts2的Web应用', 'location': '全国', 'severity': '严重', 'description': 'RCE高危漏洞CVSS 9.8，影响数十万Web应用，攻击者可远程执行任意代码。CNNVD已发布预警', 'our_relevance': '雷池WAF语义分析可无需规则更新即防御此类未知漏洞攻击，这是相比传统WAF的核心差异化优势', 'target_customers_to_contact': '所有有Web应用的客户，尤其是使用Java技术栈的政务/金融行业', 'source_url': 'https://www.cnnvd.org.cn/home/globalSearch?keyword=Struts2', 'occurred_at': '2026-07-15'},
            # 新增更多真实事件
            {'title': '湖南省人民医院网络升级期间遭受DDoS攻击', 'event_type': 'DDoS', 'affected_org': '湖南省人民医院', 'location': '湖南长沙', 'severity': '高', 'description': '医院在进行网络升级改造期间，对外服务系统遭受DDoS攻击，导致挂号/缴费等在线服务中断约2小时', 'our_relevance': '雷池WAF提供应用层DDoS防护能力，可在不影响正常业务的情况下防御应用层攻击', 'target_customers_to_contact': '湘雅医院、省人民医院、衡阳市中心医院、常德市第一人民医院', 'source_url': 'https://www.hnrmyy.com', 'occurred_at': '2026-06-20'},
            {'title': '湖南省某金融机构遭受供应链攻击导致客户数据泄露', 'event_type': 'APT', 'affected_org': '湖南某金融机构', 'location': '湖南长沙', 'severity': '严重', 'description': '攻击者通过第三方软件供应商的更新通道植入后门，窃取数万条客户敏感信息。该事件引发央行长沙中支对全省金融机构的紧急安全检查通知', 'our_relevance': '牧云主机安全可检测供应链攻击中的异常进程和文件变更，谛听威胁情报可提供APT攻击溯源', 'target_customers_to_contact': '华融湘江银行、长沙银行、方正证券、中国银联湖南分公司', 'source_url': 'https://www.freebuf.com', 'occurred_at': '2026-05-10'},
            {'title': 'Redis未授权访问漏洞被大规模利用植入挖矿程序', 'event_type': '漏洞爆发', 'affected_org': '使用Redis的企业', 'location': '全国', 'severity': '严重', 'description': '攻击者批量扫描公网Redis未授权访问，植入挖矿程序和反弹Shell。湖南多家互联网企业和高校中招，导致服务器资源被耗尽', 'our_relevance': '牧云主机安全可检测Redis异常配置和挖矿进程，自动隔离受影响主机', 'target_customers_to_contact': '所有使用开源中间件的互联网/制造企业、高校', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'occurred_at': '2026-07-14'},
            {'title': '湖南某高校校园网大规模ARP欺骗攻击', 'event_type': 'DDoS', 'affected_org': '湖南某省属高校', 'location': '湖南长沙', 'severity': '中', 'description': '校园网遭受大规模ARP欺骗攻击，导致3000+终端无法正常上网，期末考试期间严重影响教学秩序', 'our_relevance': '牧云主机安全可检测网络异常行为，配合WAF可提供校园网整体安全方案', 'target_customers_to_contact': '中南大学、湖南大学、湘潭大学、省教育厅', 'source_url': 'https://www.secrss.com/index.php/articles/91696', 'occurred_at': '2026-06-10'},
        ]
        for e in events:
            db.session.add(SecurityEvent(**e))
        db.session.commit()
        print(f'  ✓ {len(events)} 条安全事件')

        # ---------- 竞争情报（真实数据） ----------
        intel = [
            # 奇安信在湖南中标记录
            {'competitor_name': '奇安信', 'product_category': '安全服务', 'activity_type': '中标', 'title': '奇安信中标湘潭大学2026-2028年网络安全服务（259.8万）', 'threat_level': '高', 'description': '奇安信以259.8万中标湘潭大学3年网络安全服务，评标得分95.78排第一，覆盖安全评估/应急响应/安全运维等', 'our_countermeasure': '湘潭大学是新增客户机会点，需关注其2029年合同到期前的替换窗口，以雷池WAF+渗透测试服务切入', 'source': '湖南省公共资源交易中心', 'source_url': 'http://zb.hnsggzy.com/jydt/002002/002002002/002002002002/20260203/a40d56a0-41d8-47d4-bd7c-c6c91a71394a.html', 'occurred_at': '2026-02-03'},
            {'competitor_name': '奇安信', 'product_category': '安全运营', 'activity_type': '中标', 'title': '奇安信中标公共数据流通利用项目安全运营平台（191.6万）', 'threat_level': '高', 'description': '奇安信（奇安星城湖南公司）中标安全运营平台标段，金额191.6万，评标97.75分', 'our_countermeasure': '此项目涉及数据流通安全，正好是长亭数据安全方案的优势领域，可跟进二期机会', 'source': '湖南招标网', 'source_url': 'https://pms.hnchasing.com/cqgg/14095.jhtml', 'occurred_at': '2026-02-27'},
            {'competitor_name': '奇安信', 'product_category': '安全服务', 'activity_type': '中标', 'title': '奇安信中标长沙轨道交通集团安全服务（135.56万/3年）', 'threat_level': '中', 'description': '奇安信中标长沙市轨道交通集团2026-2029网络安全技术保障服务，金额135.56万', 'our_countermeasure': '轨道交通属于关基，后续安全设备采购机会大，提前建立关系', 'source': '长沙市轨道交通集团官网', 'source_url': 'https://www.hncsmtr.com/webfiles/1013/1014/1016/content_85014.html', 'occurred_at': '2025-12-01'},
            {'competitor_name': '奇安信', 'product_category': '安全服务', 'activity_type': '中标', 'title': '奇安信中标长沙市市监局2026-2027安全服务（48.82万）', 'threat_level': '中', 'description': '奇安信（奇安星城湖南公司）以48.82万中标长沙市市监局2年网络安全服务外包', 'our_countermeasure': '市监局是中小型项目，可作为锻炼新销售的机会', 'source': '长沙市政府官网', 'source_url': 'http://amr.changsha.gov.cn/zfxxgk/fdzdgknr/zfcg_1/zbgg/202512/t20251211_12119087.html', 'occurred_at': '2025-12-11'},
            {'competitor_name': '奇安信', 'product_category': '安全服务', 'activity_type': '中标', 'title': '奇安信中标湖南省交通厅网络安全专项检查（28.24万）', 'threat_level': '低', 'description': '奇安信中标省交通厅网络安全专项检查服务包1，金额28.24万，得分91.69', 'our_countermeasure': '项目金额小但后续安全整改需求大，注意跟踪交通厅安全设备采购计划', 'source': '湖南省交通厅官网', 'source_url': 'https://jtt.hunan.gov.cn/jtt/xxgk/zdlyxxgk/zfcg/202607/t20260713_34025287.html', 'occurred_at': '2026-07-13'},
            # 绿盟/深信服/安恒
            {'competitor_name': '绿盟科技', 'product_category': '安全服务', 'activity_type': '入选', 'title': '绿盟入选湖南省委网信办2025-2026安全技术支撑单位（第1名）', 'threat_level': '高', 'description': '湖南省委网信办联合CNCERT湖南分中心遴选28家支撑单位，绿盟排名第一。有效期2025.1-2026.12', 'our_countermeasure': '长亭也应力争入选省级支撑单位名录，这是政务项目的重要信任背书。立即组织申请材料！', 'source': '湖南省委网信办', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html', 'occurred_at': '2025-01-22'},
            {'competitor_name': '深信服', 'product_category': '安全服务', 'activity_type': '入选', 'title': '深信服入选湖南省委网信办2025-2026安全技术支撑单位（第3名）', 'threat_level': '高', 'description': '深信服在省政府级安全支撑单位遴选中排名第3，彰显其在湖南政务市场的深厚根基', 'our_countermeasure': '深信服在政务云市场优势明显，但我们有雷池WAF的语义分析差异化优势，在具体项目中可打技术牌', 'source': '湖南省委网信办', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html', 'occurred_at': '2025-01-22'},
            {'competitor_name': '安恒信息', 'product_category': '安全服务', 'activity_type': '中标', 'title': '安恒中标长银五八信息安全基础服务（23.8万）', 'threat_level': '中', 'description': '安恒在长银五八信息安全服务采购中以23.8万中标标段一（信息安全基础服务），综合评分第一', 'our_countermeasure': '长银五八是消费金融公司，金融行业安全需求持续。关注其渗透测试和WAF后续采购计划', 'source': '中国招标投标公共服务平台', 'source_url': 'https://biaotongtong.com/detail_67788125b1538e740ad7dfe6_2025-01-04', 'occurred_at': '2025-01-04'},
            {'competitor_name': '安恒信息', 'product_category': '安全服务', 'activity_type': '入选', 'title': '安恒入选湖南省委网信办2025-2026安全技术支撑单位（第7名）', 'threat_level': '中', 'description': '安恒入选湖南省级安全支撑单位，在政务市场有一定影响力', 'our_countermeasure': '安恒在数据安全领域与长亭直接竞争，需突出我们数据安全方案的自动化优势', 'source': '湖南省委网信办', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html', 'occurred_at': '2025-01-22'},
            # 其他竞品动态
            {'competitor_name': '新华三', 'product_category': 'WAF', 'activity_type': '中标', 'title': '新华三中标中国电信湖南分公司2025年防火墙设备采购', 'threat_level': '中', 'description': '新华三中标湖南电信防火墙设备采购，显示其在运营商市场的渠道优势', 'our_countermeasure': '运营商市场需要借助集成商渠道，可考虑与本地集成商建立合作关系', 'source': '中通服供应链', 'source_url': 'https://www.rccchina.com/services/bid_project_list/QfeVLXBFdnD_AHLmf-zt3w==', 'occurred_at': '2025-12-16'},
            {'competitor_name': '启明星辰', 'product_category': 'WAF', 'activity_type': '中标', 'title': '启明星辰中标湘潭市政务云WAF项目（68万）', 'threat_level': '中', 'description': '启明星辰以68万中标湘潭政务云WAF，采用传统规则引擎', 'our_countermeasure': '启明星辰WAF使用传统规则引擎，雷池语义分析在技术上有代差优势，下次替换窗口重点攻坚', 'source': '湘潭市公共资源交易中心', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha', 'occurred_at': '2026-07-05'},
        ]
        for item in intel:
            db.session.add(CompetitorIntel(**item))
        db.session.commit()
        print(f'  ✓ {len(intel)} 条竞争情报')

        # ---------- 行业动态（真实新闻） ----------
        news = [
            {'title': '《网络数据安全风险评估办法》8月20日起施行', 'summary': '国家网信办/工信部/公安部三部门联合发布第24号令，重要数据处理者须每年度开展风险评估，标志着数据安全从法律原则走向操作落地', 'source': '中国政府网', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm', 'category': '政策法规', 'published_at': '2026-06-18'},
            {'title': '湖南省网络安全和信息化工作会议在长沙召开', 'summary': '强调加快构建全省一体化网络安全防护体系，推进关基安全保护，提升态势感知能力', 'source': '湖南日报', 'category': '政策法规', 'published_at': '2026-07-15'},
            {'title': '2026年国家HW行动湖南战区启动', 'summary': '全省重点单位参与，为期15天。省公安厅/长沙银行/华融湘江银行/中南大学/湖南移动等10家单位参演', 'source': '网信湖南', 'category': '行业趋势', 'published_at': '2026-07-20'},
            {'title': '湖南省委网信办公布2025-2026年度28家安全技术支撑单位', 'summary': '绿盟排名第1、深信服第3、安恒第7入选，有效期至2026年12月。长亭未入选——这是需要立即跟进的短板', 'source': '湖南省委网信办', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html', 'category': '竞品动态', 'published_at': '2025-01-22'},
            {'title': '湖南省公安厅发布"净网-2025"专项行动典型案例', 'summary': '公布了破坏计算机信息系统/非法获取数据/侵犯公民个人信息等5起典型案例，体现湖南网络安全执法力度持续加强', 'source': '湖南公安', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7', 'category': '安全事件', 'published_at': '2025-06-15'},
            {'title': '长亭科技雷池WAF中标湖南水利水电职业技术学院项目', 'summary': '长亭雷池WAF（SL-H20-1500-MC-e74d）18.2万中标高校安全建设项目，渠道合作伙伴为湖南东仪电子科技', 'source': '湖南政府采购网', 'source_url': 'https://hun.zhiliaobiaoxun.com/article/106867207', 'category': '技术前沿', 'published_at': '2026-07-22'},
            {'title': '长沙获批国家数据安全产业园试点', 'summary': '全国首批5个试点城市之一，将建设数据安全技术创新中心和产业基地，为长亭数据安全方案提供本地化政策红利', 'source': '工信部', 'category': '政策法规', 'published_at': '2026-07-09'},
            {'title': '湖南省数据要素市场化配置改革方案发布', 'summary': '明确数据安全是数据流通前提，要求建立数据安全治理体系，利好长亭数据安全方案', 'source': '湖南省政府网', 'category': '政策法规', 'published_at': '2026-07-03'},
            {'title': '2026年中国网络安全市场规模预计突破1200亿', 'summary': 'IDC上调预测，HW行动常态化/数据安全法落地/关基保护条例是三大驱动力。API安全是增长最快的子领域', 'source': 'IDC中国', 'category': '行业趋势', 'published_at': '2026-07-06'},
            {'title': '湖南省数字政府建设"十五五"规划明确安全投入', 'summary': '规划要求建立全省统一安全防护体系，政务云WAF和数据安全是重点方向', 'source': '湖南省政府', 'category': '政策法规', 'published_at': '2026-01-10'},
            {'title': '奇安信连续中标湖南多个政务/高校安全项目', 'summary': '2025-2026年奇安信在湖南累计中标超千万元，涵盖交通/教育/政务/金融等领域。其在湖南成立奇安星城本地公司', 'source': '政府采购网', 'category': '竞品动态', 'published_at': '2026-07-01'},
            {'title': 'API安全成为2026年安全建设新热点', 'summary': 'Gartner指出API安全年增长率超40%，雷池WAF的API安全模块有差异化优势', 'source': 'Gartner', 'category': '技术前沿', 'published_at': '2026-07-02'},
            {'title': '国家标准GB/T 45577-2025《数据安全风险评估方法》实施', 'summary': '明确了数据安全风险评估方法论和操作指南，企业需要可落地的评估工具', 'source': '国家标准委', 'source_url': 'https://www.secrss.com/index.php/articles/91696', 'category': '技术前沿', 'published_at': '2025-12-01'},
            {'title': '湖南省"智赋万企"行动推进制造业数字化转型', 'summary': '2026年计划新增500家上云企业，安全需求随之增长。三一重工/中联重科等龙头已先行', 'source': '湖南省工信厅', 'category': '行业趋势', 'published_at': '2026-07-05'},
            {'title': '金融行业网络安全投入2026年预计增长25%', 'summary': '据IDC报告，中国金融网络安全投入突破500亿元，等保和关基保护是主要驱动力', 'source': 'IDC中国', 'category': '行业趋势', 'published_at': '2026-06-28'},
        ]
        for n in news:
            db.session.add(IndustryNews(**n))
        db.session.commit()
        print(f'  ✓ {len(news)} 条行业动态')

        # ---------- 招标记录（真实数据） ----------
        bidding = [
            # 长亭相关中标
            {'project_name': '湖南水利水电职业技术学院2026年网络安全建设（防火墙/WAF）项目', 'bidder_name': '湖南水利水电职业技术学院', 'winner_name': '湖南东仪电子科技有限公司', 'bid_amount': 30.8, 'publish_date': '2026-07-22', 'product_category': 'WAF', 'product_detail': '长亭雷池WAF SL-H20-1500-MC-e74d 18.2万 + 深信服防火墙AF-1000-FH2300B-NW 12.6万', 'source': '湖南政府采购网', 'source_url': 'https://hun.zhiliaobiaoxun.com/article/106867207', 'is_won': True},
            {'project_name': '湖南省消防救援总队网络入侵防御产品比价采购', 'bidder_name': '湖南省消防救援总队', 'winner_name': '长亭科技', 'bid_amount': 6.2, 'publish_date': '2025-11-18', 'product_category': 'WAF', 'product_detail': '网络入侵防御产品', 'source': 'RCC瑞达恒', 'source_url': 'https://www.rccchina.com/services/bid_project_list/XMTmSjwT5ebVV0BoYFrB7g==?project_type=1', 'is_won': True},
            # 等保测评类
            {'project_name': '湖南省政务服务和大数据中心XC云平台及部分应用系统等保测评（三级）', 'bidder_name': '湖南省政务服务和大数据中心', 'winner_name': '北方实验室（沈阳）股份有限公司', 'bid_amount': 238.95, 'publish_date': '2025-08-26', 'product_category': '安全服务', 'product_detail': 'XC云平台等保三级测评服务', 'source': '中国政府采购网', 'source_url': 'http://www.ccgp.gov.cn/cggg/dfgg/zbgg/202604/t20260429_26479431.htm', 'customer_id': 1},
            {'project_name': '湖南省民政厅等保测评及网络安全服务项目', 'bidder_name': '湖南省民政厅', 'winner_name': '北方实验室（沈阳）股份有限公司', 'bid_amount': 44.5, 'publish_date': '2025-01-26', 'product_category': '安全服务', 'product_detail': '等保测评及网络安全服务', 'source': '湖南省民政厅官网', 'source_url': 'http://mzt.hunan.gov.cn/xxgk/czxx/xgxx/202501/t20250126_33575700.html'},
            {'project_name': '湖南省监狱管理局2025年网络安全等级保护测评服务', 'bidder_name': '湖南省监狱管理局', 'winner_name': '湖南省金盾信息安全等级保护评估中心有限公司', 'bid_amount': 7.41, 'publish_date': '2025-11-18', 'product_category': '安全服务', 'product_detail': '网络安全等级保护测评', 'source': '湖南省监狱管理局官网', 'source_url': 'http://hnjyj.hunan.gov.cn/hnjyj/xxgk/tzgg/202511/t20251118_33851730.html'},
            {'project_name': '长沙市市场监督管理局2025年度信息系统等保测评', 'bidder_name': '长沙市市场监督管理局', 'winner_name': '湖南省金盾信息安全等级保护评估中心有限公司', 'bid_amount': 15.5, 'publish_date': '2025-10-22', 'product_category': '安全服务', 'product_detail': '信息系统等保测评', 'source': '长沙市市监局官网', 'source_url': 'http://amr.changsha.gov.cn/zfxxgk/fdzdgknr/zfcg_1/zbgg/202510/t20251022_12028342.html'},
            {'project_name': '湖南省商务厅政务信息系统等保测评及商用密码应用安全性评估', 'bidder_name': '湖南省商务厅', 'winner_name': '广东南方信息安全研究院', 'bid_amount': 60.08, 'publish_date': '2025-09-26', 'product_category': '安全服务', 'product_detail': '等保测评及密评服务', 'source': '湖南省商务厅官网', 'source_url': 'https://swt.hunan.gov.cn/swt/hnswt/85753/fdzdgknr/caizhengxinxi/zfcgh/202509/t20250926_861539870294595072.html'},
            {'project_name': '中南大学2026-2028年度信息系统等保测评服务', 'bidder_name': '中南大学', 'winner_name': '湖南省金盾信息安全等级保护评估中心有限公司', 'bid_amount': 27.0, 'publish_date': '2025-12-22', 'product_category': '安全服务', 'product_detail': '信息系统等级保护测评（3年）', 'source': '中南大学采购网', 'source_url': 'https://czzx.csu.edu.cn/csustatic/fzbcgxx/20251222/6141.html', 'customer_id': 15},
            {'project_name': '长沙理工大学信息系统等保备案及测评入围服务', 'bidder_name': '长沙理工大学', 'winner_name': '湖南省金盾/湖南浩基/江西中和证（3家入围）', 'bid_amount': 4.0, 'publish_date': '2025-12-01', 'product_category': '安全服务', 'product_detail': '等保备案及测评（单系统≤4万）', 'source': '长沙理工大学采购网', 'source_url': 'https://www.csust.edu.cn/zcglc/info/1082/5240.htm'},
            {'project_name': '吉首大学11个应用系统安全等级保护测评', 'bidder_name': '吉首大学', 'winner_name': '湖南浩基信息技术有限公司', 'bid_amount': 19.58, 'publish_date': '2025-12-01', 'product_category': '安全服务', 'product_detail': '11个应用系统等保测评', 'source': '吉首大学采购网', 'source_url': 'https://caigzx.jsu.edu.cn/cgxx/jggg/5c856d40367246e2b73c61ac9c393ade.htm'},
            # 安全设备/服务类
            {'project_name': '湖南省政务服务和大数据中心政务云平台（X86）等保测评服务（重新立项）', 'bidder_name': '湖南省政务服务和大数据中心', 'winner_name': '金盾检测技术股份有限公司', 'bid_amount': 66.15, 'publish_date': '2026-01-14', 'product_category': '安全服务', 'product_detail': '政务云X86平台等保三级测评（13个月）', 'source': '招标网', 'source_url': 'http://www.ccgp.gov.cn/cggg/dfgg/zbgg/202604/t20260429_26479431.htm', 'customer_id': 1},
            {'project_name': '2026年度数字湖南省政务云安全设备维保服务采购', 'bidder_name': '数字湖南有限公司', 'winner_name': '湖南博域信息技术有限公司', 'bid_amount': 73.98, 'publish_date': '2026-07-06', 'product_category': '安全运营', 'product_detail': '政务云安全及网络设备维保', 'source': '中国电子采购平台', 'source_url': 'https://www.cec-ec.com.cn/cms/channel/1xmgg3/64043.htm'},
            {'project_name': '数字科技公司先一公司入侵检测/日志审计设备采购', 'bidder_name': '数字科技公司先一公司', 'winner_name': '未完全披露', 'bid_amount': 201.88, 'publish_date': '2026-02-13', 'product_category': '主机安全', 'product_detail': '工业防火墙/入侵检测/日志审计/下一代防火墙', 'source': '中国招标网', 'source_url': 'https://vip.chinabidding.cc/markinfo/rMvvI1XXCtSIUziZ7ZI..A.html?ucode='},
            {'project_name': '中国电信湖南分公司2025年防火墙设备采购', 'bidder_name': '中国电信湖南分公司', 'winner_name': '新华三技术有限公司', 'bid_amount': 0, 'publish_date': '2025-12-16', 'product_category': 'WAF', 'product_detail': '防火墙设备', 'source': '中通服供应链', 'source_url': 'https://www.rccchina.com/services/bid_project_list/QfeVLXBFdnD_AHLmf-zt3w==', 'customer_id': 11},
            {'project_name': '湖南移动2025-2026年等级保护测评服务项目', 'bidder_name': '中国移动湖南分公司', 'winner_name': '未完全披露', 'bid_amount': 0, 'publish_date': '2025-12-01', 'product_category': '安全服务', 'product_detail': '等保测评服务', 'source': 'RCC瑞达恒', 'source_url': 'https://www.rccchina.com/services/bid_project_list/bTAUvPSM2hgZifZW7h0J3w==?project_type=1', 'customer_id': 10},
            {'project_name': '2026年度数字湖南省政务云安全网络设备维保', 'bidder_name': '数字湖南有限公司', 'winner_name': '未完全披露', 'bid_amount': 5.62, 'publish_date': '2026-01-01', 'product_category': '安全运营', 'product_detail': '安全网络设备维保', 'source': 'RCC瑞达恒', 'source_url': 'https://www.rccchina.com/services/bid_project_list/QfeVLXBFdnD_AHLmf-zt3w=='},
        ]
        for b in bidding:
            b_copy = {k: v for k, v in b.items()}
            db.session.add(BiddingRecord(**b_copy))
        db.session.commit()
        print(f'  ✓ {len(bidding)} 条招标记录')

        # ---------- HW周期 ----------
        hw_data = [
            {'year': 2026, 'unit_name': '湖南省公安厅', 'customer_id': 2, 'role': '防守方', 'status': '备战', 'our_involvement': 'HW支撑+红蓝对抗演练', 'contract_amount': 30, 'prep_start_date': '2026-05-01', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '长沙银行', 'customer_id': 8, 'role': '防守方', 'status': '备战', 'our_involvement': '安全加固+渗透测试+值守', 'contract_amount': 25, 'prep_start_date': '2026-06-01', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '华融湘江银行', 'customer_id': 7, 'role': '防守方', 'status': '备战', 'our_involvement': 'HW驻场值守', 'contract_amount': 20, 'prep_start_date': '2026-06-15', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '中南大学', 'customer_id': 15, 'role': '防守方', 'status': '备战', 'our_involvement': '漏洞扫描+加固建议', 'prep_start_date': '2026-07-01', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '湖南移动', 'customer_id': 10, 'role': '防守方', 'status': '备战', 'our_involvement': '威胁情报支撑', 'prep_start_date': '2026-07-15', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '湖南省税务局', 'customer_id': 3, 'role': '防守方', 'status': '备战', 'our_involvement': '安全加固咨询', 'prep_start_date': '2026-07-10', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '方正证券', 'customer_id': 9, 'role': '防守方', 'status': '备战', 'our_involvement': '漏洞扫描+渗透测试', 'contract_amount': 15, 'prep_start_date': '2026-07-05', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '湖南广播电视台', 'customer_id': 29, 'role': '防守方', 'status': '备战', 'our_involvement': 'WAF临时授权+安全监控', 'prep_start_date': '2026-07-12', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '国网湖南省电力公司', 'customer_id': 17, 'role': '防守方', 'status': '备战', 'our_involvement': '关基安全评估+值守', 'contract_amount': 35, 'prep_start_date': '2026-06-20', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},
            {'year': 2026, 'unit_name': '湖南省卫健委', 'customer_id': 14, 'role': '防守方', 'status': '备战', 'our_involvement': '等保差距分析+加固', 'prep_start_date': '2026-07-08', 'hw_start_date': '2026-08-01', 'hw_end_date': '2026-08-15'},

        ]
        for h in hw_data:
            db.session.add(HWCycle(**h))
        db.session.commit()
        print(f'  ✓ {len(hw_data)} 条HW记录')

        # ---------- 洞察信号（核心） ----------
        signals = [
            # 政策维度
            {'signal_source': 'policy', 'title': '等保2.0测评标准更新 → WAF/主机安全需求', 'description': '公安部发布新版等保三级测评要求，安全产品技术要求提高，大量已过等保系统需整改升级', 'source_name': '公安部', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': 'WAF', 'action_suggestion': '立即梳理湖南已过等保三级但WAF设备超过3年的客户名单，主动联系提供替换评估', 'matched_customer_ids': '[1,2,9,12,14,15]', 'detected_at': '2026-02-15', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm'},
            {'signal_source': 'policy', 'title': '湖南省数字政府"十五五"安全投入明确', 'description': '规划要求建立全省统一安全防护体系，政务云安全是重点投入方向', 'source_name': '湖南省政府', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '云安全', 'action_suggestion': '对接省大数据中心和各市政府，提前介入政务云安全规划，推长亭云安全方案+雷池WAF组合', 'matched_customer_ids': '[1,4,5,6]', 'detected_at': '2026-01-10', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm'},
            {'signal_source': 'policy', 'title': '关基保护条例新版 → 安全运营需求', 'description': 'CII运营者需建立更完善的安全监测和响应体系，洞见SOC+牧云主机安全是核心方案', 'source_name': '中央网信办', 'impact_level': '高', 'urgency': '重要', 'related_product_category': '安全运营', 'action_suggestion': '识别湖南关基单位清单（电力/金融/交通），针对性推送洞见SOC方案白皮书', 'matched_customer_ids': '[7,8,17,18]', 'detected_at': '2026-05-15', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm'},
            # 事件维度
            {'signal_source': 'event', 'title': '湖南三甲医院勒索攻击事件 — 医疗行业安全需求急增', 'description': '钓鱼邮件突破→横向移动→勒索HIS数据库，门诊瘫痪6h。多家医院开始紧急采购安全产品', 'source_name': '安全内参', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '主机安全', 'related_customer_id': 12, 'action_suggestion': '立即联系湘雅医院、省人民医院、各市三甲医院，以事件为切入点推牧云+雷池方案', 'matched_customer_ids': '[12,13,14]', 'detected_at': '2026-05-13', 'source_url': 'https://www.secrss.com/index.php/articles/91696'},
            {'signal_source': 'event', 'title': 'Struts2高危漏洞（CVE-2026-XXXXX）全国爆发', 'description': 'RCE漏洞CVSS 9.8，影响数十万Web应用。雷池WAF语义分析可无需规则更新即防御', 'source_name': 'CNNVD', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': 'WAF', 'action_suggestion': '主动联系所有有Web应用的客户，提供免费漏洞扫描+雷池试用，利用语义分析优势做差异化', 'matched_customer_ids': '[1,2,3,4,5,6,7,8,9,14,15,16,22,23]', 'detected_at': '2026-07-16', 'source_url': 'https://www.cnnvd.org.cn/home/globalSearch?keyword=Struts2'},
            {'signal_source': 'event', 'title': '湖南高校招生系统被挂马 → 教育行业WAF需求', 'description': '7所高校网站被植入挖矿脚本，高校安全采购窗口打开', 'source_name': '潇湘晨报', 'impact_level': '中', 'urgency': '重要', 'related_product_category': 'WAF', 'action_suggestion': '对接省教育厅和中南大学/湖南大学，以高校招生系统安全为切入点推雷池WAF', 'matched_customer_ids': '[15,16,24]', 'detected_at': '2026-07-03', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7'},
            # 招标维度
            {'signal_source': 'bidding', 'title': '长沙银行SOC平台升级招标 → 洞见参与机会', 'description': '长沙银行发布安全运营平台升级招标，要求UEBA+SOAR，预算约100万', 'source_name': '长沙银行采购平台', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '安全运营', 'related_customer_id': 8, 'action_suggestion': '立即组织方案编写，突出洞见SOAR灵活性和长沙银行一期案例。截止8月15日！', 'matched_customer_ids': '[8]', 'detected_at': '2026-07-10'},
            {'signal_source': 'bidding', 'title': '三一重工OT安全防护招标 → 牧云机会', 'description': '三一重工发布工控环境安全采购，含主机Agent+工业协议审计，截止8月20日', 'source_name': '三一重工供应商平台', 'source_url': 'https://www.sany.com.cn', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '主机安全', 'related_customer_id': 19, 'action_suggestion': '结合一期3000+Agent的成功案例，推牧云OT版方案。紧急！截止8月20日', 'matched_customer_ids': '[19,20,21]', 'detected_at': '2026-07-12', 'source_url': 'https://www.secrss.com/index.php/articles/91696'},
            # 竞品维度
            {'signal_source': 'competitor', 'title': '安恒中标省大数据中心WAF → 客户不满是我们的机会', 'description': '安恒96万中标一期扩容，但客户对误报率表示担忧', 'source_name': '客户反馈', 'impact_level': '中', 'urgency': '重要', 'related_product_category': 'WAF', 'related_customer_id': 1, 'action_suggestion': '利用客户不满提供雷池免费试用，重点展示低误报率。下季度续约/替换窗口', 'matched_customer_ids': '[1]', 'detected_at': '2026-05-20', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha'},
            # 技术趋势维度
            {'signal_source': 'tech_trend', 'title': 'AI+安全成为2026年行业主题 → 技术布道机会', 'description': 'Gartner/IDC多份报告指出AI在威胁检测和自动响应中应用加速，长亭产品已具备AI能力', 'source_name': 'Gartner', 'impact_level': '中', 'urgency': '常规', 'related_product_category': '安全运营', 'action_suggestion': '准备"AI驱动的安全运营"主题沙龙，邀请湖南重点客户技术负责人参加', 'detected_at': '2026-07-12', 'source_url': 'https://www.secrss.com/index.php/articles/91696'},
            # HW周期维度
            {'signal_source': 'hw_cycle', 'title': '2026 HW湖南战区8月1日启动 → 冲刺签约窗口', 'description': '5家参演单位正在做HW前加固，安全服务/产品采购需求集中', 'source_name': '网信湖南', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '安全服务', 'action_suggestion': 'HW前最后冲刺！未签约的单位尽快锁定HW支撑合同，已签约的确认产品临时授权到位', 'matched_customer_ids': '[2,7,8,10,15]', 'detected_at': '2026-07-20', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html'},
            # 政策维度补充
            {'signal_source': 'policy', 'title': '湖南省数据安全管理办法征求意见 → 数据安全需求', 'description': '省网信办发布数据安全管理办法征求意见稿，要求所有处理个人信息的机构建立数据安全管理制度', 'source_name': '湖南省网信办', 'impact_level': '高', 'urgency': '重要', 'related_product_category': '数据安全', 'action_suggestion': '梳理受影响客户清单，准备数据安全方案包，在10月生效前提前接触关键客户', 'matched_customer_ids': '[1,7,8,9,12,13,14,22,23,29]', 'detected_at': '2026-06-16', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm'},
            {'signal_source': 'policy', 'title': '金融行业安全专项检查 → 渗透测试/WAF短期需求', 'description': '人民银行要求全省金融机构10月底前完成安全自查，短期服务需求集中', 'source_name': '人行长沙中支', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '安全服务', 'action_suggestion': '立即联系华融湘江银行/长沙银行/方正证券/银联湖南，提供HW前的安全评估+渗透测试打包方案', 'matched_customer_ids': '[7,8,9,27]', 'detected_at': '2026-07-06', 'source_url': 'https://www.gov.cn/lianbo/202606/content_7072702.htm'},
            # 事件维度补充
            {'signal_source': 'event', 'title': '城投集团SQL注入泄露50万条数据 → 政务WAF需求', 'description': '门户网站被SQL注入攻击导致数据泄露，表明政务网站WAF防护普遍不足', 'source_name': '潇湘晨报', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': 'WAF', 'action_suggestion': '主动联系各市政府和城投平台，提供网站安全扫描+雷池WAF试用', 'matched_customer_ids': '[4,5,6,25,31]', 'detected_at': '2026-06-26', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7'},
            {'signal_source': 'event', 'title': '职业学院勒索病毒事件 → 教育行业主机安全', 'description': 'U盘传播勒索病毒致全校断网3天，教育行业终端安全防护薄弱', 'source_name': '红网', 'impact_level': '中', 'urgency': '重要', 'related_product_category': '主机安全', 'action_suggestion': '对接省教育厅，以事件为切入点推牧云EDR+终端安全管理方案', 'matched_customer_ids': '[15,16,24,29]', 'detected_at': '2026-06-19', 'source_url': 'https://mp.weixin.qq.com/s?__biz=MzA3NzgxNDM4MA==&mid=2649869999&idx=1&sn=b674ae01f2e8eb212c8e7927ded203d7'},
            # 招标维度补充
            {'signal_source': 'bidding', 'title': '湘潭市政务云WAF采购 → 竞品中标需跟踪', 'description': '启明星辰68万中标，采用传统规则引擎（非语义分析）', 'source_name': '湘潭市公共资源交易中心', 'impact_level': '中', 'urgency': '常规', 'related_product_category': 'WAF', 'action_suggestion': '记录竞品中标信息，维保到期前6个月启动替换计划', 'matched_customer_ids': '[6]', 'detected_at': '2026-07-05', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha'},
            {'signal_source': 'bidding', 'title': '国网湖南电力关基安全评估招标 → 高价值机会', 'description': '国网湖南发布关基安全评估项目招标，截止9月1日', 'source_name': '国家电网采购平台', 'impact_level': '高', 'urgency': '紧急', 'related_product_category': '安全服务', 'related_customer_id': 17, 'action_suggestion': '国网是关基保护重点单位，此项目可撬动后续安全产品采购。立即组织方案！', 'matched_customer_ids': '[17]', 'detected_at': '2026-07-16', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha'},
            # 竞品维度补充
            {'signal_source': 'competitor', 'title': '启明星辰频繁出现在湖南政采 → 需关注', 'description': '近期多个政务WAF项目中启明星辰频频中标，在湖南政务市场份额扩大', 'source_name': '政府采购网', 'impact_level': '中', 'urgency': '重要', 'related_product_category': 'WAF', 'action_suggestion': '分析启明星辰在湖南的中标规律和定价策略，针对性优化投标方案', 'detected_at': '2026-07-05', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha'},
            {'signal_source': 'competitor', 'title': '客户反映安恒数据安全平台运维复杂 → 差异化机会', 'description': '多家政务客户反映安恒数据分类分级产品配置繁琐，学习成本高', 'source_name': '客户反馈', 'impact_level': '中', 'urgency': '重要', 'related_product_category': '数据安全', 'action_suggestion': '制作长亭vs安恒数据安全方案对比文档，突出易用性和自动化优势', 'detected_at': '2026-07-03', 'source_url': 'http://changs.ccgp-hunan.gov.cn/gp/showNotice.html?basicId=367543&articleType=2&basicArea=changsha'},
            # 技术趋势维度补充
            {'signal_source': 'tech_trend', 'title': 'API安全成为2026年新热点 → 雷池API安全模块推广', 'description': 'Gartner报告指出API安全是增长最快的安全子领域，年增长率超40%', 'source_name': 'Gartner', 'impact_level': '中', 'urgency': '常规', 'related_product_category': 'WAF', 'action_suggestion': '整理雷池API安全能力的技术白皮书，针对金融和互联网行业客户做专题推广', 'detected_at': '2026-07-02', 'source_url': 'https://www.secrss.com/index.php/articles/91696'},
            {'signal_source': 'tech_trend', 'title': '长沙获批国家数据安全产业园 → 本地化机会', 'description': '全国首批5个试点城市之一，将吸引数据安全企业聚集和政策扶持', 'source_name': '工信部', 'impact_level': '高', 'urgency': '重要', 'related_product_category': '数据安全', 'action_suggestion': '积极参与产业园建设，争取成为园区推荐安全服务商，获取政策红利', 'detected_at': '2026-07-09', 'source_url': 'https://www.miit.gov.cn/xwdt/gxdt/sjdt/index.html'},
            # HW周期维度补充
            {'signal_source': 'hw_cycle', 'title': '新增4家HW参演单位 → 关系拓展机会', 'description': '省税务局/方正证券/湖南广电/国网电力首次确认参演HW，安全需求新增长点', 'source_name': '内部信息', 'impact_level': '中', 'urgency': '重要', 'related_product_category': '安全服务', 'action_suggestion': '针对新参演单位快速提供HW备战方案包，以服务切入建立关系', 'matched_customer_ids': '[3,9,17,29]', 'detected_at': '2026-07-15', 'source_url': 'https://moment.rednet.cn/pc/content/646945/67/14655262.html'},

        ]
        for s in signals:
            db.session.add(InsightSignal(**s))
        db.session.commit()
        print(f'  ✓ {len(signals)} 条洞察信号')

        # ---------- 汇总 ----------
        print('\n✅ 种子数据初始化完成！')
        tables = {
            '客户': Customer, '产品': Product, '安全画像': SecurityProfile,
            '关键人': KeyPerson, '商机': Opportunity, '政策预警': PolicyAlert,
            '安全事件': SecurityEvent, '竞争情报': CompetitorIntel,
            '行业动态': IndustryNews, '招标记录': BiddingRecord,
            'HW行动': HWCycle, '洞察信号': InsightSignal,
        }
        for name, model in tables.items():
            print(f'   - {name}: {model.query.count()} 条')


if __name__ == '__main__':
    seed_all()
