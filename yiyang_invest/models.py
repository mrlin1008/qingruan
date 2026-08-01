"""
益阳高新区智慧招商平台 — 数据模型（11张核心表）
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ==================== 用户 ====================
class User(db.Model):
    __tablename__ = 'yy_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff')       # admin / manager / staff
    display_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    leads = db.relationship('Lead', backref='assignee', lazy='dynamic',
                            foreign_keys='Lead.assigned_to')
    projects = db.relationship('Project', backref='owner', lazy='dynamic',
                               foreign_keys='Project.owner_id')
    follow_ups = db.relationship('FollowUp', backref='creator', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id, 'username': self.username,
            'role': self.role, 'display_name': self.display_name,
            'phone': self.phone, 'is_active': self.is_active
        }

    @property
    def role_label(self):
        labels = {'admin': '管理员', 'manager': '招商经理', 'staff': '招商专员'}
        return labels.get(self.role, self.role)

    # Flask-Login 兼容
    @property
    def is_authenticated(self): return True

    @property
    def is_anonymous(self): return False

    def get_id(self): return str(self.id)


# ==================== 园区信息 ====================
class ParkInfo(db.Model):
    """园区基本信息（单条记录）"""
    __tablename__ = 'yy_park_info'
    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(200), default='益阳高新区数字经济产业园')
    overview = db.Column(db.Text)           # 园区概况
    location_desc = db.Column(db.Text)      # 区位交通
    total_area = db.Column(db.String(50))
    incubator_area = db.Column(db.String(50))      # 孵化区 14.5万㎡
    factory_area = db.Column(db.String(50))         # 制造区 10栋标准厂房
    settled_count = db.Column(db.Integer, default=0)
    investment_total = db.Column(db.Float, default=0)
    key_resources = db.Column(db.Text)              # JSON：智算中心、研究院等
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== 产业链节点 ====================
class IndustryChain(db.Model):
    __tablename__ = 'yy_industry_chains'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    track = db.Column(db.String(30))          # 智能感知/工业视觉/装备智能/算力配套
    chain_position = db.Column(db.String(20))  # 上游/中游/下游/配套
    description = db.Column(db.Text)
    gap_level = db.Column(db.String(10))       # 空白/薄弱/完善
    parent_id = db.Column(db.Integer, db.ForeignKey('yy_industry_chains.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)

    children = db.relationship('IndustryChain', backref=db.backref('parent', remote_side=[id]))
    companies = db.relationship('Company', backref='chain_node', lazy='dynamic')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ==================== 企业 ====================
class Company(db.Model):
    __tablename__ = 'yy_companies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    company_type = db.Column(db.String(20), default='target')   # settled入驻 / target目标客商
    industry_track = db.Column(db.String(30))     # 四大赛道
    chain_node_id = db.Column(db.Integer, db.ForeignKey('yy_industry_chains.id'), nullable=True)
    scale = db.Column(db.String(20))               # 大型/中型/小型/初创
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address = db.Column(db.String(300))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(30))
    contact_email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    certifications = db.Column(db.Text)             # 资质证书
    products_services = db.Column(db.Text)          # 主营产品/服务
    annual_revenue = db.Column(db.String(50))       # 年营收
    employee_count = db.Column(db.Integer)          # 员工数
    advantage_tags = db.Column(db.String(300))      # 优势标签，逗号分隔
    tianyancha_id = db.Column(db.String(50))       # 天眼查企业ID
    status = db.Column(db.String(20), default='active')  # active/inactive
    is_chain_leader = db.Column(db.Boolean, default=False)  # 是否链主企业
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship('Project', backref='company', lazy='dynamic')
    demands = db.relationship('ProcurementDemand', backref='chain_company', lazy='dynamic')

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['chain_node_name'] = self.chain_node.name if self.chain_node else ''
        return d


# ==================== 招商线索 ====================
class Lead(db.Model):
    __tablename__ = 'yy_leads'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(200))
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(30))
    source = db.Column(db.String(50))               # 展会/推介会/以商招商/网络线索/在线表单
    industry_track = db.Column(db.String(30))
    intent_level = db.Column(db.String(10))          # 高/中/低
    status = db.Column(db.String(20), default='待处理')  # 待处理/对接中/已转化/已关闭
    assigned_to = db.Column(db.Integer, db.ForeignKey('yy_users.id'), nullable=True)
    notes = db.Column(db.Text)
    converted_project_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['assignee_name'] = self.assignee.display_name if self.assignee else ''
        return d


# ==================== 招商项目 ====================
class Project(db.Model):
    __tablename__ = 'yy_projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('yy_companies.id'), nullable=True)
    space_id = db.Column(db.Integer, db.ForeignKey('yy_spaces.id'), nullable=True)
    stage = db.Column(db.String(20), default='线索')     # 线索/洽谈/签约/落地/投产
    amount = db.Column(db.Float, default=0)               # 投资金额（万元）
    industry_track = db.Column(db.String(30))
    owner_id = db.Column(db.Integer, db.ForeignKey('yy_users.id'), nullable=True)
    expected_date = db.Column(db.String(20))              # 预计落地日期
    settled_date = db.Column(db.String(20))               # 实际落地日期
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    follow_ups = db.relationship('FollowUp', backref='project', lazy='dynamic',
                                 cascade='all, delete-orphan', order_by='FollowUp.created_at.desc()')

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['company_name'] = self.company.name if self.company else ''
        d['owner_name'] = self.owner.display_name if self.owner else ''
        d['space_name'] = self.space.name if self.space else ''
        return d


# ==================== 跟进记录 ====================
class FollowUp(db.Model):
    __tablename__ = 'yy_followups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('yy_projects.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    next_step = db.Column(db.Text)
    contact_person = db.Column(db.String(50))
    follow_date = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey('yy_users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['creator_name'] = self.creator.display_name if self.creator else ''
        return d


# ==================== 空间资源 ====================
class Space(db.Model):
    __tablename__ = 'yy_spaces'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(20))              # 孵化区/制造区
    building = db.Column(db.String(50))
    floor = db.Column(db.String(20))
    total_area = db.Column(db.Float)              # 总面积（㎡）
    available_area = db.Column(db.Float)          # 可用面积（㎡）
    floor_height = db.Column(db.String(20))       # 层高
    load_capacity = db.Column(db.String(50))      # 承重
    power_supply = db.Column(db.String(100))      # 配电
    supporting = db.Column(db.Text)               # 配套设施
    rent_desc = db.Column(db.String(100))         # 租金说明
    status = db.Column(db.String(20), default='available')  # available/reserved/occupied
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship('Project', backref='space', lazy='dynamic')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ==================== 招商政策 ====================
class Policy(db.Model):
    __tablename__ = 'yy_policies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    policy_type = db.Column(db.String(50))          # 税收优惠/人才补贴/租金减免/科技创新/金融支持
    issuing_dept = db.Column(db.String(100))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    applicable_conditions = db.Column(db.Text)
    publish_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='published')  # published/draft
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ==================== 新闻动态 ====================
class Article(db.Model):
    __tablename__ = 'yy_articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50))              # 园区动态/产业资讯/招商成果/政策解读
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    cover_image = db.Column(db.String(300))
    source_url = db.Column(db.String(500))            # 原文链接
    is_published = db.Column(db.Boolean, default=False)
    publish_date = db.Column(db.String(20))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# ==================== 招投标记录 ====================
class BiddingRecord(db.Model):
    __tablename__ = 'yy_bidding_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('yy_companies.id'), nullable=True)
    project_name = db.Column(db.String(500))
    bidder_name = db.Column(db.String(200))
    winner_name = db.Column(db.String(200))
    bid_amount = db.Column(db.Float, default=0)
    publish_date = db.Column(db.String(20))
    product_detail = db.Column(db.Text)
    source = db.Column(db.String(50))
    source_url = db.Column(db.String(500))
    industry_track = db.Column(db.String(30))        # 匹配的赛道
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== 链主采购需求 ====================
class ProcurementDemand(db.Model):
    """链主企业发布的采购需求 / 供应商招募"""
    __tablename__ = 'yy_procurement_demands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chain_company_id = db.Column(db.Integer, db.ForeignKey('yy_companies.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50))              # 原材料/零部件/设备/软件/服务
    demand_type = db.Column(db.String(30), default='供应商招募')  # 年度采购/紧急采购/供应商招募
    amount_estimate = db.Column(db.String(100))      # 预估采购金额
    quantity_desc = db.Column(db.String(200))        # 采购数量描述
    deadline = db.Column(db.String(20))              # 报名截止日期
    requirements = db.Column(db.Text)                # 供应商资质要求
    description = db.Column(db.Text)                 # 需求详细描述
    contact_info = db.Column(db.String(200))         # 对接人联系方式
    industry_track = db.Column(db.String(30))        # 关联赛道
    status = db.Column(db.String(20), default='open')  # open/closed
    published_at = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['chain_company_name'] = self.chain_company.name if self.chain_company else ''
        d['chain_company_track'] = self.chain_company.industry_track if self.chain_company else ''
        return d


# ==================== 采购需求响应 ====================
class DemandResponse(db.Model):
    """供应商对采购需求的响应/报名"""
    __tablename__ = 'yy_demand_responses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    demand_id = db.Column(db.Integer, db.ForeignKey('yy_procurement_demands.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(30))
    contact_email = db.Column(db.String(100))
    qualification_desc = db.Column(db.Text)      # 资质说明
    advantage_desc = db.Column(db.Text)           # 优势说明
    status = db.Column(db.String(20), default='pending')  # pending/reviewing/approved/rejected
    reviewed_at = db.Column(db.String(20))
    review_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    demand = db.relationship('ProcurementDemand', backref=db.backref('responses', lazy='dynamic'))

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['demand_title'] = self.demand.title if self.demand else ''
        return d


# ==================== 链主技术能力（下游专区） ====================
class TechCapability(db.Model):
    """链主企业对外开放的技术/产品/服务能力，吸引下游客户"""
    __tablename__ = 'yy_tech_capabilities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chain_company_id = db.Column(db.Integer, db.ForeignKey('yy_companies.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    capability_type = db.Column(db.String(50))    # 算力服务/产线测试/技术合作/产品供应/联合研发
    description = db.Column(db.Text)
    applicable_scenarios = db.Column(db.Text)     # 适用场景
    contact_info = db.Column(db.String(200))
    industry_track = db.Column(db.String(30))
    status = db.Column(db.String(20), default='open')
    published_at = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chain_company = db.relationship('Company', backref=db.backref('tech_capabilities', lazy='dynamic'))

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d['chain_company_name'] = self.chain_company.name if self.chain_company else ''
        return d


# ==================== 园区实景图 ====================
class ParkImage(db.Model):
    __tablename__ = 'yy_park_images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(300), nullable=False)
    original_name = db.Column(db.String(300))
    file_size = db.Column(db.Integer, default=0)       # bytes
    category = db.Column(db.String(30), default='园区风光')  # 园区风光/孵化空间/制造厂房/配套设施
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def url(self):
        return f'/static/uploads/park/{self.filename}'

    def to_dict(self):
        return {
            'id': self.id, 'filename': self.filename,
            'original_name': self.original_name,
            'file_size': self.file_size, 'category': self.category,
            'sort_order': self.sort_order, 'url': self.url,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }
