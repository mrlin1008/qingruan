"""
长亭科技湖南办 v2 — 洞察→信号→商机 作战指挥平台
数据模型（12张表）
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Customer(db.Model):
    """客户组织"""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))
    industry = db.Column(db.String(50))
    org_type = db.Column(db.String(50))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    scale = db.Column(db.String(20))
    it_budget_level = db.Column(db.String(20))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    key_persons = db.relationship('KeyPerson', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    security_profiles = db.relationship('SecurityProfile', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    opportunities = db.relationship('Opportunity', backref='customer', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'name_en': self.name_en,
            'industry': self.industry, 'org_type': self.org_type,
            'city': self.city, 'district': self.district,
            'scale': self.scale, 'it_budget_level': self.it_budget_level,
            'website': self.website, 'description': self.description,
            'lat': self.lat, 'lng': self.lng,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else '',
        }

    @property
    def profile_coverage(self):
        """安全画像覆盖率（已覆盖品类数/总品类数）"""
        covered = set(p.product_category for p in self.security_profiles.all() if p.product_category)
        all_cats = {'WAF', '主机安全', '威胁情报', '渗透测试', '等保测评', '数据安全', '云安全', '安全运营', '安全服务'}
        return round(len(covered & all_cats) / len(all_cats) * 100) if all_cats else 0


class KeyPerson(db.Model):
    """关键人"""
    __tablename__ = 'key_persons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100))
    department = db.Column(db.String(50))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    wechat = db.Column(db.String(50))
    email = db.Column(db.String(100))
    personality_notes = db.Column(db.Text)
    relationship_level = db.Column(db.String(20))
    last_contact_at = db.Column(db.String(20))
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id, 'customer_id': self.customer_id,
            'name': self.name, 'title': self.title, 'department': self.department,
            'role': self.role, 'phone': self.phone, 'wechat': self.wechat,
            'email': self.email, 'personality_notes': self.personality_notes,
            'relationship_level': self.relationship_level,
            'last_contact_at': self.last_contact_at, 'notes': self.notes,
        }


class SecurityProfile(db.Model):
    """客户安全画像"""
    __tablename__ = 'security_profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_category = db.Column(db.String(50))
    current_solution = db.Column(db.String(200))
    purchase_year = db.Column(db.String(10))
    renewal_date = db.Column(db.String(20))
    satisfaction = db.Column(db.String(10))
    gap_analysis = db.Column(db.String(30))
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id, 'customer_id': self.customer_id,
            'product_category': self.product_category,
            'current_solution': self.current_solution, 'purchase_year': self.purchase_year,
            'renewal_date': self.renewal_date, 'satisfaction': self.satisfaction,
            'gap_analysis': self.gap_analysis, 'notes': self.notes,
        }


class InsightSignal(db.Model):
    """洞察信号 —— 核心表，七维框架的统一信号模型"""
    __tablename__ = 'insight_signals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    signal_source = db.Column(db.String(30), nullable=False, comment='policy/event/bidding/competitor/tech_trend/hw_cycle')
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    source_url = db.Column(db.String(500))
    source_name = db.Column(db.String(100))
    impact_level = db.Column(db.String(10), default='中')
    urgency = db.Column(db.String(10), default='重要')
    related_customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    related_product_category = db.Column(db.String(50))
    action_suggestion = db.Column(db.Text)
    matched_customer_ids = db.Column(db.Text, comment='JSON数组，自动匹配的受影响客户ID')
    converted_to_opportunity_id = db.Column(db.Integer, nullable=True)
    detected_at = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    related_customer = db.relationship('Customer', backref=db.backref('signals', lazy='dynamic'), foreign_keys=[related_customer_id])

    def to_dict(self):
        return {
            'id': self.id, 'signal_source': self.signal_source,
            'title': self.title, 'description': self.description,
            'source_url': self.source_url, 'source_name': self.source_name,
            'impact_level': self.impact_level, 'urgency': self.urgency,
            'related_customer_id': self.related_customer_id,
            'related_customer_name': self.related_customer.name if self.related_customer else '',
            'related_product_category': self.related_product_category,
            'action_suggestion': self.action_suggestion,
            'matched_customer_ids': self.matched_customer_ids,
            'converted_to_opportunity_id': self.converted_to_opportunity_id,
            'detected_at': self.detected_at,
        }


class Opportunity(db.Model):
    """商机管线"""
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_category = db.Column(db.String(50))
    product_detail = db.Column(db.String(200))
    signal_id = db.Column(db.Integer, nullable=True, comment='溯源：从哪个洞察信号转化而来')
    stage = db.Column(db.String(30), default='lead')
    amount = db.Column(db.Float)
    probability = db.Column(db.Integer, default=10)
    expected_close_date = db.Column(db.String(20))
    pain_point = db.Column(db.Text)
    our_solution = db.Column(db.Text)
    competitor_involved = db.Column(db.String(200))
    contact_person_id = db.Column(db.Integer, db.ForeignKey('key_persons.id'), nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contact_person = db.relationship('KeyPerson', backref='opportunities', foreign_keys=[contact_person_id])

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else '',
            'customer_city': self.customer.city if self.customer else '',
            'product_category': self.product_category, 'product_detail': self.product_detail,
            'signal_id': self.signal_id,
            'stage': self.stage, 'amount': self.amount, 'probability': self.probability,
            'expected_close_date': self.expected_close_date,
            'pain_point': self.pain_point, 'our_solution': self.our_solution,
            'competitor_involved': self.competitor_involved,
            'contact_person_id': self.contact_person_id,
            'contact_person_name': self.contact_person.name if self.contact_person else '',
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else '',
        }


class BiddingRecord(db.Model):
    """招投标记录"""
    __tablename__ = 'bidding_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    project_name = db.Column(db.String(300))
    bidder_name = db.Column(db.String(200))
    winner_name = db.Column(db.String(200))
    bid_amount = db.Column(db.Float)
    publish_date = db.Column(db.String(20))
    bid_deadline = db.Column(db.String(20))
    project_number = db.Column(db.String(100))
    product_category = db.Column(db.String(50))
    product_detail = db.Column(db.Text)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    is_won = db.Column(db.Boolean, default=False, comment='我方是否中标')
    loss_reason = db.Column(db.Text, comment='丢单原因分析')
    next_opportunity_date = db.Column(db.String(20), comment='下次机会时间（维保到期/替换窗口）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref=db.backref('bidding_records', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id, 'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else '',
            'project_name': self.project_name, 'bidder_name': self.bidder_name,
            'winner_name': self.winner_name, 'bid_amount': self.bid_amount,
            'publish_date': self.publish_date, 'bid_deadline': self.bid_deadline,
            'project_number': self.project_number,
            'product_category': self.product_category, 'product_detail': self.product_detail,
            'source': self.source, 'source_url': self.source_url,
            'is_won': self.is_won, 'loss_reason': self.loss_reason,
            'next_opportunity_date': self.next_opportunity_date,
        }


class PolicyAlert(db.Model):
    """政策法规预警"""
    __tablename__ = 'policy_alerts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    issuing_body = db.Column(db.String(100))
    policy_type = db.Column(db.String(50))
    effective_date = db.Column(db.String(20))
    impact_level = db.Column(db.String(10))
    affected_industries = db.Column(db.String(200))
    compliance_deadline = db.Column(db.String(20))
    opportunity_relevance = db.Column(db.Text)
    source_url = db.Column(db.String(500))
    published_at = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'issuing_body': self.issuing_body,
            'policy_type': self.policy_type, 'effective_date': self.effective_date,
            'impact_level': self.impact_level, 'affected_industries': self.affected_industries,
            'compliance_deadline': self.compliance_deadline,
            'opportunity_relevance': self.opportunity_relevance,
            'source_url': self.source_url, 'published_at': self.published_at,
        }


class SecurityEvent(db.Model):
    """安全事件"""
    __tablename__ = 'security_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    event_type = db.Column(db.String(50))
    affected_org = db.Column(db.String(200))
    location = db.Column(db.String(100))
    severity = db.Column(db.String(10))
    description = db.Column(db.Text)
    estimated_loss = db.Column(db.String(100))
    our_relevance = db.Column(db.Text)
    target_customers_to_contact = db.Column(db.Text)
    source_url = db.Column(db.String(500))
    occurred_at = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'event_type': self.event_type,
            'affected_org': self.affected_org, 'location': self.location,
            'severity': self.severity, 'description': self.description,
            'estimated_loss': self.estimated_loss, 'our_relevance': self.our_relevance,
            'target_customers_to_contact': self.target_customers_to_contact,
            'source_url': self.source_url, 'occurred_at': self.occurred_at,
        }


class IndustryNews(db.Model):
    """行业动态"""
    __tablename__ = 'industry_news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False)
    summary = db.Column(db.Text)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    category = db.Column(db.String(50))
    published_at = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'summary': self.summary,
            'source': self.source, 'source_url': self.source_url,
            'category': self.category, 'published_at': self.published_at,
        }


class CompetitorIntel(db.Model):
    """竞争情报"""
    __tablename__ = 'competitor_intel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    competitor_name = db.Column(db.String(100), nullable=False)
    product_category = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    activity_type = db.Column(db.String(30))
    title = db.Column(db.String(300))
    description = db.Column(db.Text)
    threat_level = db.Column(db.String(10))
    our_countermeasure = db.Column(db.Text)
    source = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    occurred_at = db.Column(db.String(20))

    customer = db.relationship('Customer', backref=db.backref('competitor_intel', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id, 'competitor_name': self.competitor_name,
            'product_category': self.product_category, 'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else '',
            'activity_type': self.activity_type, 'title': self.title,
            'description': self.description, 'threat_level': self.threat_level,
            'our_countermeasure': self.our_countermeasure,
            'source': self.source, 'source_url': self.source_url,
            'occurred_at': self.occurred_at,
        }


class Product(db.Model):
    """产品知识库"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    subcategory = db.Column(db.String(100))
    description = db.Column(db.Text)
    key_features = db.Column(db.Text)
    target_customers = db.Column(db.String(200))
    typical_deal_size = db.Column(db.Float)
    sales_cycle_months = db.Column(db.Integer)
    competitive_advantages = db.Column(db.Text)
    case_study_summary = db.Column(db.Text)
    pricing_model = db.Column(db.String(200))
    brochure_url = db.Column(db.String(300))

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'category': self.category,
            'subcategory': self.subcategory, 'description': self.description,
            'key_features': self.key_features, 'target_customers': self.target_customers,
            'typical_deal_size': self.typical_deal_size,
            'sales_cycle_months': self.sales_cycle_months,
            'competitive_advantages': self.competitive_advantages,
            'case_study_summary': self.case_study_summary,
            'pricing_model': self.pricing_model, 'brochure_url': self.brochure_url,
        }


class HWCycle(db.Model):
    """HW行动管理"""
    __tablename__ = 'hw_cycles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    unit_name = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    role = db.Column(db.String(20), comment='攻击方/防守方/组织方')
    status = db.Column(db.String(20), default='备战')
    our_involvement = db.Column(db.Text)
    contract_amount = db.Column(db.Float)
    key_lessons = db.Column(db.Text)
    prep_start_date = db.Column(db.String(20))
    hw_start_date = db.Column(db.String(20))
    hw_end_date = db.Column(db.String(20))

    customer = db.relationship('Customer', backref=db.backref('hw_cycles', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id, 'year': self.year, 'unit_name': self.unit_name,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else '',
            'role': self.role, 'status': self.status,
            'our_involvement': self.our_involvement, 'contract_amount': self.contract_amount,
            'key_lessons': self.key_lessons,
            'prep_start_date': self.prep_start_date,
            'hw_start_date': self.hw_start_date, 'hw_end_date': self.hw_end_date,
        }


class ActionLog(db.Model):
    """行动日志 —— 追溯每一步操作"""
    __tablename__ = 'action_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    related_type = db.Column(db.String(30))
    related_id = db.Column(db.Integer)
    action = db.Column(db.String(30))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'related_type': self.related_type,
            'related_id': self.related_id, 'action': self.action,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }
