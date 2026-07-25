"""
长亭科技湖南办 v2 — 洞察→信号→商机 作战指挥平台
Flask 主应用
"""
import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from models import (db, Customer, KeyPerson, SecurityProfile, InsightSignal,
                    Opportunity, BiddingRecord, PolicyAlert, SecurityEvent,
                    CompetitorIntel, Product, HWCycle, ActionLog, IndustryNews)


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "changting_hunan_v2.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)
    return app


app = create_app()

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """驾驶舱首页 — 七维洞察总览"""
    from sqlalchemy import func

    # KPI 卡片
    signal_total = InsightSignal.query.count()
    signal_high = InsightSignal.query.filter_by(impact_level='高').count()
    opp_total = Opportunity.query.count()
    opp_active = Opportunity.query.filter(Opportunity.stage.in_(
        ['lead', 'contacted', 'needs_analysis', 'solution_proposal', 'quotation', 'negotiation']
    )).count()
    opp_amount = db.session.query(func.sum(Opportunity.amount)).filter(
        Opportunity.stage.in_(['lead', 'contacted', 'needs_analysis', 'solution_proposal', 'quotation', 'negotiation'])
    ).scalar() or 0
    opp_won_amount = db.session.query(func.sum(Opportunity.amount)).filter(
        Opportunity.stage == 'won'
    ).scalar() or 0
    customer_count = Customer.query.count()

    # 本月新线索
    this_month = datetime.utcnow().strftime('%Y-%m')
    new_this_month = Opportunity.query.filter(Opportunity.created_at >= f'{this_month}-01').count()

    # HW倒计时（取最近一次HW）
    latest_hw = HWCycle.query.order_by(HWCycle.hw_start_date.desc()).first()
    hw_days_remaining = None
    if latest_hw and latest_hw.hw_start_date:
        try:
            hw_date = datetime.strptime(latest_hw.hw_start_date, '%Y-%m-%d')
            hw_days_remaining = (hw_date - datetime.utcnow()).days
        except ValueError:
            pass

    # 七维信号来源分布
    signal_source_stats = db.session.query(
        InsightSignal.signal_source, func.count(InsightSignal.id)
    ).group_by(InsightSignal.signal_source).all()
    source_labels = {'policy': '政策合规', 'event': '安全事件', 'bidding': '招投标',
                     'competitor': '竞争情报', 'tech_trend': '技术趋势', 'hw_cycle': 'HW周期'}
    signal_source_data = [{'name': source_labels.get(s, s), 'value': c} for s, c in signal_source_stats]

    # 商机阶段漏斗
    stage_order = ['lead', 'contacted', 'needs_analysis', 'solution_proposal',
                   'quotation', 'negotiation', 'won', 'lost']
    stage_labels = {'lead': '线索', 'contacted': '初步接触', 'needs_analysis': '需求分析',
                    'solution_proposal': '方案提交', 'quotation': '报价中',
                    'negotiation': '商务谈判', 'won': '已赢单', 'lost': '已丢单'}
    stage_data = [{'name': stage_labels.get(s, s), 'value': Opportunity.query.filter_by(stage=s).count()}
                  for s in stage_order if Opportunity.query.filter_by(stage=s).count() > 0]

    # 最新洞察信号
    latest_signals = InsightSignal.query.order_by(InsightSignal.created_at.desc()).limit(8).all()

    # 需关注的客户
    urgency_map = {'紧急': 3, '重要': 2, '常规': 1}
    focus_customers = Customer.query.all()
    focus_list = []
    for c in focus_customers:
        signals = c.signals.filter_by(converted_to_opportunity_id=None).all()
        if signals:
            max_urgency = max(urgency_map.get(s.urgency, 0) for s in signals)
            focus_list.append({'customer': c, 'signal_count': len(signals), 'urgency': max_urgency})
    focus_list.sort(key=lambda x: x['urgency'], reverse=True)

    return render_template('index.html',
                           signal_total=signal_total, signal_high=signal_high,
                           opp_total=opp_total, opp_active=opp_active,
                           opp_amount=opp_amount, opp_won_amount=opp_won_amount,
                           customer_count=customer_count, new_this_month=new_this_month,
                           hw_days_remaining=hw_days_remaining,
                           signal_source_data=signal_source_data, stage_data=stage_data,
                           latest_signals=latest_signals, focus_list=focus_list[:8])


@app.route('/signals')
def signals():
    """市场洞察与情报分析 — 四大模块：政策雷达 / 招投标情报 / 区域热力地图 / 行业动态"""
    from sqlalchemy import func

    active_tab = request.args.get('tab', 'policy')

    # ---- 模块1: 政策雷达 ----
    policy_list = PolicyAlert.query.order_by(PolicyAlert.published_at.desc()).all()
    policy_types = [[r[0], r[1]] for r in db.session.query(
        PolicyAlert.policy_type, func.count(PolicyAlert.id)
    ).group_by(PolicyAlert.policy_type).all()]

    # ---- 模块2: 招投标情报 ----
    bid_source = request.args.get('bid_source', '')
    bid_industry = request.args.get('bid_industry', '')
    bid_query = BiddingRecord.query
    if bid_source:
        bid_query = bid_query.filter_by(source=bid_source)
    bid_list = bid_query.order_by(BiddingRecord.publish_date.desc()).all()

    # 按产品分类统计招标
    bid_cat_stats = [[r[0] or '未分类', r[1]] for r in db.session.query(
        BiddingRecord.product_category, func.count(BiddingRecord.id)
    ).group_by(BiddingRecord.product_category).all()]
    # 按来源统计
    bid_source_stats = [[r[0], r[1]] for r in db.session.query(
        BiddingRecord.source, func.count(BiddingRecord.id)
    ).group_by(BiddingRecord.source).all()]

    # ---- 模块3: 区域热力地图 ----
    city_stats = db.session.query(
        Customer.city, func.count(Customer.id),
        func.sum(Customer.id)  # placeholder, real heat uses customer count + bidding count
    ).group_by(Customer.city).all()

    # 每个城市的客户数 + 招标数 + 商机数
    city_heat = []
    for city, cust_cnt, _ in city_stats:
        if not city:
            continue
        bid_cnt = BiddingRecord.query.join(Customer, BiddingRecord.customer_id == Customer.id)\
            .filter(Customer.city == city).count()
        opp_cnt = Opportunity.query.join(Customer, Opportunity.customer_id == Customer.id)\
            .filter(Customer.city == city).count()
        city_heat.append({
            'name': city, 'customer_count': cust_cnt,
            'bid_count': bid_cnt, 'opp_count': opp_cnt,
            'heat': cust_cnt * 2 + bid_cnt * 3 + opp_cnt * 2
        })

    # 湖南14地市完整列表
    hunan_cities = ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界',
                    '益阳', '郴州', '永州', '怀化', '娄底', '湘西']
    city_heat_map = {c['name']: c for c in city_heat}
    city_heat_full = []
    for cn in hunan_cities:
        if cn in city_heat_map:
            city_heat_full.append(city_heat_map[cn])
        else:
            city_heat_full.append({'name': cn, 'customer_count': 0, 'bid_count': 0,
                                   'opp_count': 0, 'heat': 0})

    # ---- 模块4: 行业动态 ----
    news_category = request.args.get('news_cat', '')
    news_query = IndustryNews.query
    if news_category:
        news_query = news_query.filter_by(category=news_category)
    news_list = news_query.order_by(IndustryNews.published_at.desc()).all()
    news_cats = [[r[0], r[1]] for r in db.session.query(
        IndustryNews.category, func.count(IndustryNews.id)
    ).group_by(IndustryNews.category).all()]

    return render_template('signals.html',
                           active_tab=active_tab,
                           policy_list=policy_list, policy_types=policy_types,
                           bid_list=bid_list, bid_cat_stats=bid_cat_stats,
                           bid_source_stats=bid_source_stats, bid_source=bid_source,
                           city_heat_full=city_heat_full,
                           news_list=news_list, news_cats=news_cats, news_category=news_category)


@app.route('/customers')
def customers():
    """客户列表"""
    industry = request.args.get('industry', '')
    city = request.args.get('city', '')
    search = request.args.get('search', '').strip()

    query = Customer.query
    if industry:
        query = query.filter_by(industry=industry)
    if city:
        query = query.filter_by(city=city)
    if search:
        query = query.filter(Customer.name.contains(search))

    customers_list = query.order_by(Customer.name).all()
    industries = sorted(set(c.industry for c in Customer.query.all() if c.industry))
    cities = sorted(set(c.city for c in Customer.query.all() if c.city))

    return render_template('customers.html', customers=customers_list,
                           industry=industry, city=city, search=search,
                           industries=industries, cities=cities)


@app.route('/customer/<int:customer_id>')
def customer_detail(customer_id):
    """客户360详情 — 5 Tab布局"""
    customer = Customer.query.get_or_404(customer_id)
    profiles = customer.security_profiles.order_by(SecurityProfile.product_category).all()
    key_persons = customer.key_persons.order_by(KeyPerson.role).all()
    opportunities = customer.opportunities.order_by(Opportunity.updated_at.desc()).all()
    signals_list = customer.signals.order_by(InsightSignal.created_at.desc()).all()

    # 实时从天眼查拉取本年度招投标
    tyc_bids = []
    tyc_error = None
    try:
        from tianyancha_api import fetch_bidding
        data = fetch_bidding(customer.name)
        if isinstance(data, dict) and 'error' in data:
            tyc_error = data.get('message', '天眼查查询失败')
        else:
            tyc_bids = [r for r in data if (r.get('publish_date', '') or '').startswith('2026')][:20]
    except Exception as e:
        tyc_error = str(e)

    bidding = customer.bidding_records.order_by(BiddingRecord.publish_date.desc()).all()
    competitor_wins = customer.competitor_intel.order_by(CompetitorIntel.occurred_at.desc()).all()
    hw_records = customer.hw_cycles.order_by(HWCycle.year.desc()).all()

    all_categories = ['WAF', '主机安全', '威胁情报', '渗透测试', '等保测评',
                      '数据安全', '云安全', '安全运营', '安全服务']
    covered = set(p.product_category for p in profiles)
    gaps = [c for c in all_categories if c not in covered]

    return render_template('customer_detail.html', customer=customer,
                           profiles=profiles, key_persons=key_persons,
                           opportunities=opportunities, signals=signals_list,
                           bidding=bidding, competitor_wins=competitor_wins,
                           hw_records=hw_records, all_categories=all_categories,
                           gaps=gaps, covered=covered,
                           tyc_bids=tyc_bids, tyc_error=tyc_error)


@app.route('/opportunities')
def opportunities():
    """商机管线 — 来自招投标模块，仅展示未中标项目"""

    def detect_category(project_name):
        name = (project_name or '')
        if any(kw in name for kw in ['WAF', '防火墙', 'Web应用']): return 'WAF'
        if any(kw in name for kw in ['主机', '终端', '服务器', 'EDR', '杀毒']): return '主机安全'
        if any(kw in name for kw in ['渗透测试', '渗透']): return '渗透测试'
        if any(kw in name for kw in ['等保测评', '等保', '等级保护']): return '安全服务'
        if any(kw in name for kw in ['安全运维', '维保服务', '安全防护有效性']): return '安全运营'
        if any(kw in name for kw in ['安全运营', 'SOC', '态势感知', '日志审计', '上网行为']): return '安全运营'
        if any(kw in name for kw in ['数据安全', '分类分级', '脱敏']): return '数据安全'
        if any(kw in name for kw in ['云安全', '政务云']): return '云安全'
        if any(kw in name for kw in ['威胁情报', 'APT']): return '威胁情报'
        if any(kw in name for kw in ['消防']): return '其他'
        if any(kw in name for kw in ['安全评估', '安全检测', '安全监测', '信息安全评估', '并网安全检测']): return '安全服务'
        if any(kw in name for kw in ['安全服务', '安全保障', '网络安全', '信息安全', '密码', '商用密码', '密评']): return '安全服务'
        return '安全服务'

    # 取所有未中标项目
    bids = BiddingRecord.query.filter(
        (BiddingRecord.winner_name == None) | (BiddingRecord.winner_name == '')
    ).order_by(BiddingRecord.publish_date.desc()).all()

    # 自动分类
    for b in bids:
        if not b.product_category:
            b.product_category = detect_category(b.project_name)

    # 品类过滤
    category_filter = request.args.get('category', '')
    if category_filter:
        bids = [b for b in bids if b.product_category == category_filter]

    # 按品类分组
    cat_order = ['WAF', '主机安全', '安全服务', '安全运营', '数据安全', '云安全', '威胁情报', '渗透测试']
    category_colors = {
        'WAF': 'primary', '主机安全': 'success', '安全服务': 'warning',
        '安全运营': 'info', '数据安全': 'danger', '云安全': 'purple',
        '威胁情报': 'dark', '渗透测试': 'secondary'
    }

    pipeline = {}
    for cat in cat_order:
        group = [b for b in bids if b.product_category == cat]
        if group:
            pipeline[cat] = {
                'label': cat, 'color': category_colors.get(cat, 'secondary'),
                'bids': group, 'count': len(group)
            }
    uncat = [b for b in bids if b.product_category not in cat_order]
    if uncat:
        pipeline['其他'] = {'label': '其他', 'color': 'secondary', 'bids': uncat, 'count': len(uncat)}

    total_amount = sum(b.bid_amount or 0 for b in bids)
    categories = sorted(set(b.product_category for b in bids if b.product_category))
    total_count = sum(col['count'] for col in pipeline.values())

    return render_template('opportunities.html', pipeline=pipeline,
                           category_filter=category_filter,
                           total_amount=total_amount, total_count=total_count,
                           categories=categories)


@app.route('/bidding')
def bidding():
    """招投标情报"""
    customer_id = request.args.get('customer_id', type=int, default=0)
    category = request.args.get('category', '')
    industry = request.args.get('industry', '')
    search = request.args.get('search', '').strip()
    page = request.args.get('page', type=int, default=1)
    per_page = 50

    query = BiddingRecord.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if category:
        query = query.filter_by(product_category=category)
    if search:
        query = query.filter(db.or_(
            BiddingRecord.project_name.contains(search),
            BiddingRecord.bidder_name.contains(search),
            BiddingRecord.winner_name.contains(search),
        ))
    if industry:
        query = query.join(Customer).filter(Customer.industry == industry)
    query = query.order_by(BiddingRecord.publish_date.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    records = pagination.items

    # 关键词从 product_detail 字段读取（存储在入库时已匹配）
    record_kw = {}
    for r in records:
        if r.product_detail:
            record_kw[r.id] = [k.strip() for k in r.product_detail.split(',') if k.strip()][:3]
        else:
            record_kw[r.id] = []

    from sqlalchemy import func
    total_records = query.count()
    total_amount = db.session.query(func.sum(BiddingRecord.bid_amount)).scalar() or 0
    customers_list = Customer.query.order_by(Customer.name).all()
    categories = sorted(set(r.product_category for r in BiddingRecord.query.all() if r.product_category))
    industries = sorted(set(c.industry for c in Customer.query.join(BiddingRecord).filter(BiddingRecord.customer_id == Customer.id).all() if c.industry))

    return render_template('bidding.html', records=records, total_records=total_records,
                           total_amount=total_amount, customer_id=customer_id,
                           category=category, search=search, industry=industry,
                           customers=customers_list, categories=categories, industries=industries,
                           pagination=pagination, record_kw=record_kw)


@app.route('/competitors')
def competitors():
    """竞争情报"""
    competitor = request.args.get('competitor', '')
    threat = request.args.get('threat', '')
    query = CompetitorIntel.query
    if competitor:
        query = query.filter_by(competitor_name=competitor)
    if threat:
        query = query.filter_by(threat_level=threat)
    intel_list = query.order_by(CompetitorIntel.occurred_at.desc()).all()

    from sqlalchemy import func
    competitor_stats = [[r[0], r[1]] for r in db.session.query(
        CompetitorIntel.competitor_name, func.count(CompetitorIntel.id)
    ).group_by(CompetitorIntel.competitor_name).all()]
    threat_stats = [[r[0], r[1]] for r in db.session.query(
        CompetitorIntel.threat_level, func.count(CompetitorIntel.id)
    ).group_by(CompetitorIntel.threat_level).all()]

    competitor_names = sorted(set(c.competitor_name for c in CompetitorIntel.query.all()))
    product_cats = sorted(set(c.product_category for c in CompetitorIntel.query.all() if c.product_category))

    return render_template('competitors.html', intel_list=intel_list,
                           competitor=competitor, threat=threat,
                           competitor_stats=competitor_stats, threat_stats=threat_stats,
                           competitor_names=competitor_names, product_cats=product_cats)


@app.route('/insights')
def insights():
    """市场洞察（政策/事件/动态）"""
    tab = request.args.get('tab', 'policies')
    policies = PolicyAlert.query.order_by(PolicyAlert.published_at.desc()).all()
    events = SecurityEvent.query.order_by(SecurityEvent.occurred_at.desc()).all()
    news_list = []
    if tab == 'news':
        from models import IndustryNews as INews
        news_list = INews.query.order_by(INews.published_at.desc()).all()
    return render_template('insights.html', tab=tab, policies=policies,
                           events=events, news_list=news_list)


@app.route('/hw-cycle')
def hw_cycle():
    """HW行动管理"""
    year = request.args.get('year', type=int, default=2026)
    hw_records = HWCycle.query.filter_by(year=year).order_by(HWCycle.status, HWCycle.unit_name).all()
    hw_years = sorted(set(h.year for h in HWCycle.query.all()), reverse=True)

    from sqlalchemy import func
    total_contract = db.session.query(func.sum(HWCycle.contract_amount)).filter_by(year=year).scalar() or 0

    status_counts = {'备战': 0, '进行中': 0, '复盘': 0, '完成': 0}
    for h in hw_records:
        status_counts[h.status] = status_counts.get(h.status, 0) + 1

    customers_list = Customer.query.order_by(Customer.name).all()
    return render_template('hw_cycle.html', hw_records=hw_records,
                           year=year, hw_years=hw_years,
                           total_contract=total_contract, status_counts=status_counts,
                           customers=customers_list)


# ==================== API 路由 ====================

@app.route('/api/stats')
def api_stats():
    from sqlalchemy import func
    return jsonify({
        'customer_count': Customer.query.count(),
        'signal_total': InsightSignal.query.count(),
        'signal_high': InsightSignal.query.filter_by(impact_level='高').count(),
        'opp_total': Opportunity.query.count(),
        'opp_active': Opportunity.query.filter(Opportunity.stage.in_(
            ['lead', 'contacted', 'needs_analysis', 'solution_proposal', 'quotation', 'negotiation']
        )).count(),
        'opp_amount': db.session.query(func.sum(Opportunity.amount)).filter(
            Opportunity.stage.in_(['lead', 'contacted', 'needs_analysis', 'solution_proposal', 'quotation', 'negotiation'])
        ).scalar() or 0,
    })


@app.route('/api/signals')
def api_signals():
    signals_list = InsightSignal.query.order_by(InsightSignal.created_at.desc()).all()
    return jsonify([s.to_dict() for s in signals_list])


@app.route('/api/signals/convert/<int:sig_id>', methods=['POST'])
def api_convert_signal(sig_id):
    """核心API：信号转为商机"""
    sig = InsightSignal.query.get_or_404(sig_id)
    if sig.converted_to_opportunity_id:
        return jsonify({'error': '该信号已转为商机'}), 400

    opp = Opportunity(
        title=sig.title,
        customer_id=sig.related_customer_id,
        product_category=sig.related_product_category,
        signal_id=sig.id,
        stage='lead',
        notes=f'来源：{sig.signal_source} - {sig.action_suggestion or sig.description or ""}',
    )
    db.session.add(opp)
    db.session.flush()
    sig.converted_to_opportunity_id = opp.id
    _log_action('signal', sig.id, 'convert', f'信号转为商机 #{opp.id}')
    db.session.commit()
    return jsonify(opp.to_dict()), 201


@app.route('/api/opportunities', methods=['POST'])
def api_create_opportunity():
    data = request.get_json() or {}
    for f in ['title', 'customer_id', 'product_category']:
        if not data.get(f):
            return jsonify({'error': f'缺少必填字段: {f}'}), 400
    opp = Opportunity(
        title=data['title'], customer_id=data['customer_id'],
        product_category=data.get('product_category', ''),
        product_detail=data.get('product_detail', ''),
        signal_id=data.get('signal_id'),
        stage=data.get('stage', 'lead'),
        amount=data.get('amount'), probability=data.get('probability', 10),
        expected_close_date=data.get('expected_close_date', ''),
        pain_point=data.get('pain_point', ''),
        our_solution=data.get('our_solution', ''),
        competitor_involved=data.get('competitor_involved', ''),
        notes=data.get('notes', ''),
    )
    db.session.add(opp)
    _log_action('opportunity', opp.id, 'create', f'创建商机: {opp.title}')
    db.session.commit()
    return jsonify(opp.to_dict()), 201


@app.route('/api/opportunities/<int:opp_id>', methods=['PUT'])
def api_update_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    data = request.get_json() or {}
    for field in ['title', 'stage', 'amount', 'probability', 'expected_close_date',
                  'product_category', 'product_detail', 'pain_point', 'our_solution',
                  'competitor_involved', 'notes']:
        if field in data:
            setattr(opp, field, data[field])
    _log_action('opportunity', opp.id, 'update', f'更新商机阶段→{opp.stage}')
    db.session.commit()
    return jsonify(opp.to_dict())


@app.route('/api/opportunities/<int:opp_id>', methods=['DELETE'])
def api_delete_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    db.session.delete(opp)
    db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': '客户名称不能为空'}), 400
    c = Customer(name=data['name'], name_en=data.get('name_en', ''),
                 industry=data.get('industry', ''), org_type=data.get('org_type', ''),
                 city=data.get('city', ''), district=data.get('district', ''),
                 scale=data.get('scale', ''), it_budget_level=data.get('it_budget_level', ''),
                 website=data.get('website', ''), description=data.get('description', ''))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route('/api/key-persons', methods=['POST'])
def api_create_key_person():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('customer_id'):
        return jsonify({'error': '姓名和客户ID不能为空'}), 400
    kp = KeyPerson(customer_id=data['customer_id'], name=data['name'],
                   title=data.get('title', ''), department=data.get('department', ''),
                   role=data.get('role', ''), phone=data.get('phone', ''),
                   wechat=data.get('wechat', ''), email=data.get('email', ''),
                   personality_notes=data.get('personality_notes', ''),
                   relationship_level=data.get('relationship_level', '认识'),
                   last_contact_at=data.get('last_contact_at', ''), notes=data.get('notes', ''))
    db.session.add(kp)
    db.session.commit()
    return jsonify(kp.to_dict()), 201


@app.route('/api/security-profiles', methods=['POST'])
def api_create_security_profile():
    data = request.get_json() or {}
    if not data.get('customer_id'):
        return jsonify({'error': '客户ID不能为空'}), 400
    sp = SecurityProfile(customer_id=data['customer_id'],
                         product_category=data.get('product_category', ''),
                         current_solution=data.get('current_solution', ''),
                         purchase_year=data.get('purchase_year', ''),
                         renewal_date=data.get('renewal_date', ''),
                         satisfaction=data.get('satisfaction', ''),
                         gap_analysis=data.get('gap_analysis', ''),
                         notes=data.get('notes', ''))
    db.session.add(sp)
    db.session.commit()
    return jsonify(sp.to_dict()), 201


@app.route('/api/security-profiles/<int:sp_id>', methods=['DELETE'])
def api_delete_security_profile(sp_id):
    sp = SecurityProfile.query.get_or_404(sp_id)
    db.session.delete(sp)
    db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/bidding/upload', methods=['POST'])
def api_bidding_upload():
    import csv, io
    file = request.files.get('file')
    if not file:
        return jsonify({'error': '请选择文件'}), 400
    try:
        content = file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(content))
    except Exception as e:
        return jsonify({'error': f'文件解析失败: {str(e)}'}), 400
    customer_map = {c.name: c.id for c in Customer.query.all()}
    imported = 0
    for row in reader:
        project_name = (row.get('项目名称') or row.get('project_name') or '').strip()
        if not project_name:
            continue
        bidder = (row.get('招标方') or row.get('bidder_name') or '').strip()
        cid = None
        for cn, ci in customer_map.items():
            if cn in bidder or bidder in cn:
                cid = ci; break
        try:
            amount = float((row.get('中标金额') or row.get('bid_amount') or '0').replace(',', '').replace('万', '').replace('元', ''))
        except ValueError:
            amount = 0
        db.session.add(BiddingRecord(
            customer_id=cid, project_name=project_name, bidder_name=bidder,
            winner_name=(row.get('中标方') or row.get('winner_name') or '').strip(),
            bid_amount=amount,
            publish_date=(row.get('发布日期') or row.get('publish_date') or '').strip(),
            product_category=(row.get('采购品类') or row.get('product_category') or '').strip(),
            product_detail=(row.get('采购内容') or row.get('product_detail') or '').strip(),
            source=row.get('来源', 'CSV导入').strip(),
            source_url=(row.get('链接') or row.get('source_url') or '').strip(),
        ))
        imported += 1
    db.session.commit()
    return jsonify({'ok': True, 'imported': imported, 'message': f'成功导入 {imported} 条'})


@app.route('/api/tianyancha/search', methods=['POST'])
def api_tianyancha_search():
    """从天眼查查询指定公司的招标信息并导入"""
    data = request.get_json() or {}
    company_name = data.get('company', '').strip()
    if not company_name:
        return jsonify({'error': '请提供公司名称'}), 400

    try:
        from tianyancha_api import search_bidding_sync
        results = search_bidding_sync(company_name, max_results=20)
    except ImportError:
        return jsonify({'error': '天眼查API模块未就绪'}), 500

    if isinstance(results, dict) and 'error' in results:
        return jsonify(results), 400

    if not results:
        return jsonify({'ok': True, 'imported': 0, 'message': '未找到 ' + company_name + ' 的招投标记录'})

    customer_map = {c.name: c.id for c in Customer.query.all()}
    imported = 0
    for r in results:
        cid = None
        for cn, ci in customer_map.items():
            if cn in company_name or company_name in cn:
                cid = ci
                break
        existing = BiddingRecord.query.filter_by(
            project_name=r.get('project_name', ''), bidder_name=r.get('bidder_name', company_name)
        ).first()
        if existing:
            continue
        record = BiddingRecord(
            customer_id=cid,
            project_name=r.get('project_name', ''),
            bidder_name=r.get('bidder_name', company_name),
            winner_name=r.get('winner_name', ''),
            bid_amount=r.get('bid_amount', 0),
            publish_date=r.get('publish_date', ''),
            product_detail=r.get('summary', '') or r.get('project_name', ''),
            source='天眼查API',
            source_url=r.get('bid_url', '') or r.get('source_url', ''),
        )
        db.session.add(record)
        imported += 1
    db.session.commit()
    return jsonify({'ok': True, 'imported': imported, 'message': '从天眼查API获取并保存了 ' + str(imported) + ' 条新招标记录'})


@app.route('/customer/<int:customer_id>/bidding')
def customer_bidding(customer_id):
    """客户招投标页 —— 服务端渲染天眼查数据"""
    customer = Customer.query.get_or_404(customer_id)
    records = []
    error = None
    try:
        from tianyancha_api import fetch_bidding
        data = fetch_bidding(customer.name)
        if isinstance(data, dict) and 'error' in data:
            error = data.get('message', str(data))
        else:
            this_year = [r for r in data if (r.get('publish_date', '') or '').startswith('2026')]
            records = this_year[:30]
    except ImportError:
        error = '天眼查模块未就绪，请确认 tyc CLI 已安装并登录'
    except Exception as e:
        error = f'查询异常: {str(e)}'

    return render_template('customer_bidding.html', customer=customer, records=records, error=error)


@app.route('/api/customer/<int:customer_id>/tianyancha-bidding')
def api_customer_tianyancha_bidding(customer_id):
    """实时从天眼查拉取指定客户的招投标数据（本年度）"""
    customer = Customer.query.get_or_404(customer_id)
    try:
        from tianyancha_api import fetch_bidding
        data = fetch_bidding(customer.name)
    except ImportError:
        return jsonify({'error': '天眼查模块未就绪，请确认 tyc CLI 已安装并登录: tyc login'}), 500
    except Exception as e:
        return jsonify({'error': f'查询异常: {str(e)}'}), 500

    if isinstance(data, dict) and 'error' in data:
        msg = data.get('message', str(data))
        return jsonify({'error': f'天眼查API: {msg}', 'customer_name': customer.name, 'total': 0, 'items': []}), 200

    # 只保留2026年的，最多20条
    this_year = [r for r in data if (r.get('publish_date', '') or '').startswith('2026')][:20]
    return jsonify({'customer_name': customer.name, 'total': len(this_year), 'items': this_year})


def _log_action(rtype, rid, action, desc=''):
    db.session.add(ActionLog(related_type=rtype, related_id=rid, action=action, description=desc))


if __name__ == '__main__':
    with app.app_context():
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changting_hunan_v2.db')
        if not os.path.exists(db_path):
            print('⚠️  数据库未初始化，请先运行: python seed_data.py')
        else:
            print('✓ 数据库已就绪')
    app.run(debug=True, host='0.0.0.0', port=5092)
