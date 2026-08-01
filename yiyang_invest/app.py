"""
益阳高新区智慧招商平台 — Flask 主应用
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_config, UploadConfig
from models import db, User, ParkInfo, IndustryChain, Company, Lead, Project, FollowUp, Space, Policy, Article, BiddingRecord, ParkImage
from auth import login_required, role_required, get_current_user


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.config['MAX_CONTENT_LENGTH'] = UploadConfig.MAX_CONTENT_LENGTH
    app.config['UPLOAD_FOLDER'] = UploadConfig.UPLOAD_FOLDER
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()


# ==================== 上下文注入 ====================
@app.context_processor
def inject_user():
    return {'current_user': get_current_user()}


# ==================== 文件上传工具 ====================
def _allowed_file(filename):
    """检查文件扩展名是否合法"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}


def _save_upload(file, subfolder):
    """保存上传文件并返回 (saved_filename, original_name, file_size)"""
    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    saved_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    folder = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, saved_name)
    file.save(filepath)
    file_size = os.path.getsize(filepath)
    return saved_name, original_name, file_size


@app.route('/api/upload/article-cover', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def api_upload_article_cover():
    """上传新闻封面图"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'msg': '未选择文件'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'ok': False, 'msg': '文件名为空'}), 400
    if not _allowed_file(file.filename):
        return jsonify({'ok': False, 'msg': '仅支持 jpg/png/gif/webp 格式'}), 400

    saved_name, original_name, file_size = _save_upload(file, 'covers')
    url = f'/static/uploads/covers/{saved_name}'
    return jsonify({'ok': True, 'url': url, 'filename': saved_name,
                    'original_name': original_name, 'file_size': file_size})


@app.route('/api/upload/park-image', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def api_upload_park_image():
    """上传园区实景图"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'msg': '未选择文件'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'ok': False, 'msg': '文件名为空'}), 400
    if not _allowed_file(file.filename):
        return jsonify({'ok': False, 'msg': '仅支持 jpg/png/gif/webp 格式'}), 400

    saved_name, original_name, file_size = _save_upload(file, 'park')
    category = request.form.get('category', '园区风光')

    img = ParkImage(
        filename=saved_name, original_name=original_name,
        file_size=file_size, category=category,
        sort_order=ParkImage.query.count()
    )
    db.session.add(img)
    db.session.commit()
    return jsonify({'ok': True, 'image': img.to_dict()})


@app.route('/api/public/park-images')
def api_public_park_images():
    """公开实景图列表（无需登录）"""
    images = ParkImage.query.order_by(ParkImage.sort_order).all()
    return jsonify({'ok': True, 'images': [img.to_dict() for img in images]})


@app.route('/api/park-images', methods=['GET'])
@login_required
@role_required('admin', 'manager')
def api_park_images_list():
    """园区实景图列表"""
    images = ParkImage.query.order_by(ParkImage.sort_order).all()
    return jsonify({'ok': True, 'images': [img.to_dict() for img in images]})


@app.route('/api/park-images/<int:image_id>', methods=['DELETE'])
@login_required
@role_required('admin', 'manager')
def api_park_image_delete(image_id):
    """删除园区实景图"""
    img = ParkImage.query.get_or_404(image_id)
    # 删除物理文件
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'park', img.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(img)
    db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/park-images/<int:image_id>', methods=['PUT'])
@login_required
@role_required('admin', 'manager')
def api_park_image_update(image_id):
    """更新实景图分类/排序"""
    img = ParkImage.query.get_or_404(image_id)
    data = request.get_json() or {}
    if 'category' in data:
        img.category = data['category']
    if 'sort_order' in data:
        img.sort_order = data['sort_order']
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 认证路由 ====================
@app.route('/auth/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username, is_active=True).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['display_name'] = user.display_name
            flash(f'欢迎回来，{user.display_name}', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('用户名或密码错误', 'error')

    return render_template('login.html')


@app.route('/auth/logout', endpoint='logout')
def logout():
    session.clear()
    flash('已安全退出', 'success')
    return redirect(url_for('login'))


# ==================== 对外展示前台 ====================
@app.route('/')
def public_index():
    """首页：园区概览"""
    park = ParkInfo.query.first()
    articles = Article.query.filter_by(is_published=True).order_by(
        Article.publish_date.desc()).limit(4).all()
    chains = IndustryChain.query.filter_by(parent_id=None).order_by(
        IndustryChain.sort_order).all()
    settled = Company.query.filter_by(company_type='settled', status='active').count()
    projects = Project.query.count()

    return render_template('public/index.html',
                           park=park, articles=articles, chains=chains,
                           settled_count=settled, project_count=projects)


@app.route('/industry')
def public_industry():
    """产业生态"""
    chains = [c.to_dict() for c in IndustryChain.query.order_by(IndustryChain.sort_order).all()]
    tracks = ['智能感知', '工业视觉', '装备智能', '算力配套']
    companies = Company.query.filter_by(status='active').all()
    return render_template('public/industry.html',
                           chains=chains, tracks=tracks, companies=companies)


@app.route('/space')
def public_space():
    """空间载体"""
    incubator = Space.query.filter_by(zone='孵化区').all()
    factory = Space.query.filter_by(zone='制造区').all()
    return render_template('public/space.html', incubator=incubator, factory=factory)


@app.route('/policy')
def public_policy():
    """政策服务"""
    policy_type = request.args.get('type', '')
    query = Policy.query.filter_by(status='published')
    if policy_type:
        query = query.filter_by(policy_type=policy_type)
    policies = query.order_by(Policy.publish_date.desc()).all()
    types = sorted(set(p.policy_type for p in Policy.query.all() if p.policy_type))
    return render_template('public/policy.html', policies=policies, types=types, current_type=policy_type)


@app.route('/contact', methods=['GET', 'POST'])
def public_contact():
    """在线对接"""
    if request.method == 'POST':
        lead = Lead(
            company_name=request.form.get('company_name', ''),
            contact_person=request.form.get('contact_person', ''),
            contact_phone=request.form.get('contact_phone', ''),
            source='在线表单',
            industry_track=request.form.get('industry_track', ''),
            intent_level=request.form.get('intent_level', '中'),
            notes=request.form.get('notes', ''),
        )
        db.session.add(lead)
        db.session.commit()
        flash('您的意向已提交成功，招商团队将在1-3个工作日内与您联系！', 'success')
        return redirect(url_for('public_contact'))

    return render_template('public/contact.html')


# ==================== 管理后台 ====================
@app.route('/admin')
@login_required
def admin_dashboard():
    """数据驾驶舱"""
    from sqlalchemy import func

    # KPI 统计
    lead_total = Lead.query.count()
    lead_new_month = Lead.query.filter(
        Lead.created_at >= datetime.utcnow().strftime('%Y-%m') + '-01').count()
    project_negotiating = Project.query.filter_by(stage='洽谈').count()
    project_signed = Project.query.filter_by(stage='签约').count()
    project_amount = db.session.query(func.sum(Project.amount)).filter_by(stage='签约').scalar() or 0
    space_available = Space.query.filter_by(status='available').count()
    space_total = Space.query.count()

    # 项目漏斗
    stages = ['线索', '洽谈', '签约', '落地', '投产']
    funnel = [{'name': s, 'value': Project.query.filter_by(stage=s).count()} for s in stages]

    # 赛道分布
    track_stats = db.session.query(
        Project.industry_track, func.count(Project.id)
    ).filter(Project.industry_track != '').group_by(Project.industry_track).all()
    track_data = [{'name': t or '未分类', 'value': c} for t, c in track_stats]

    # 最近跟进
    recent_followups = FollowUp.query.order_by(FollowUp.created_at.desc()).limit(10).all()

    # 线索来源
    source_stats = db.session.query(
        Lead.source, func.count(Lead.id)
    ).filter(Lead.source != '').group_by(Lead.source).all()
    source_data = [{'name': s, 'value': c} for s, c in source_stats]

    return render_template('admin/dashboard.html',
                           lead_total=lead_total, lead_new_month=lead_new_month,
                           project_negotiating=project_negotiating, project_signed=project_signed,
                           project_amount=project_amount,
                           space_available=space_available, space_total=space_total,
                           funnel=funnel, track_data=track_data,
                           recent_followups=recent_followups, source_data=source_data)


# ==================== 线索管理 ====================
@app.route('/admin/leads')
@login_required
def admin_leads():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    track = request.args.get('track', '')

    query = Lead.query
    if status:
        query = query.filter_by(status=status)
    if track:
        query = query.filter_by(industry_track=track)

    pagination = query.order_by(Lead.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    users = User.query.filter_by(is_active=True).all()
    leads_json = [lead.to_dict() for lead in pagination.items]
    return render_template('admin/leads.html',
                           leads=pagination.items, leads_json=leads_json,
                           pagination=pagination,
                           current_status=status, current_track=track, users=users)


@app.route('/api/leads', methods=['POST'])
@login_required
def api_lead_add():
    data = request.get_json() or {}
    lead = Lead(
        company_name=data.get('company_name', ''),
        contact_person=data.get('contact_person', ''),
        contact_phone=data.get('contact_phone', ''),
        source=data.get('source', '手动录入'),
        industry_track=data.get('industry_track', ''),
        intent_level=data.get('intent_level', '中'),
        notes=data.get('notes', ''),
        assigned_to=data.get('assigned_to') or None,
    )
    db.session.add(lead)
    db.session.commit()
    return jsonify({'ok': True, 'id': lead.id})


@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
@login_required
def api_lead_update(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    data = request.get_json() or {}
    for k in ['company_name', 'contact_person', 'contact_phone', 'source',
              'industry_track', 'intent_level', 'status', 'notes', 'assigned_to']:
        if k in data:
            setattr(lead, k, data[k])
    db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/leads/<int:lead_id>/convert', methods=['PUT'])
@login_required
def api_lead_convert(lead_id):
    """线索转化为项目"""
    lead = Lead.query.get_or_404(lead_id)
    data = request.get_json() or {}

    # 创建或关联企业
    company = Company.query.filter_by(name=lead.company_name).first()
    if not company:
        company = Company(
            name=lead.company_name,
            company_type='target',
            industry_track=lead.industry_track,
            contact_person=lead.contact_person,
            contact_phone=lead.contact_phone,
        )
        db.session.add(company)
        db.session.flush()

    project = Project(
        title=data.get('title', f'{lead.company_name}招商项目'),
        company_id=company.id,
        stage='洽谈',
        amount=data.get('amount', 0),
        industry_track=lead.industry_track,
        owner_id=data.get('owner_id') or session.get('user_id'),
        notes=lead.notes,
    )
    db.session.add(project)
    db.session.flush()

    lead.status = '已转化'
    lead.converted_project_id = project.id
    db.session.commit()
    return jsonify({'ok': True, 'project_id': project.id})


# ==================== 项目管理 ====================
@app.route('/admin/projects')
@login_required
def admin_projects():
    page = request.args.get('page', 1, type=int)
    stage = request.args.get('stage', '')
    track = request.args.get('track', '')

    query = Project.query
    if stage:
        query = query.filter_by(stage=stage)
    if track:
        query = query.filter_by(industry_track=track)

    pagination = query.order_by(Project.updated_at.desc()).paginate(page=page, per_page=20, error_out=False)
    users = User.query.filter_by(is_active=True).all()
    companies = Company.query.filter_by(status='active').order_by(Company.name).all()
    stages = ['线索', '洽谈', '签约', '落地', '投产']

    # 看板数据
    kanban = {s: Project.query.filter_by(stage=s).order_by(Project.updated_at.desc()).all() for s in stages}

    return render_template('admin/projects.html',
                           projects=pagination.items, pagination=pagination,
                           current_stage=stage, current_track=track,
                           users=users, companies=companies, stages=stages, kanban=kanban)


@app.route('/api/projects', methods=['POST'])
@login_required
def api_project_add():
    data = request.get_json() or {}
    project = Project(
        title=data.get('title', ''),
        company_id=data.get('company_id') or None,
        stage=data.get('stage', '线索'),
        amount=data.get('amount', 0),
        industry_track=data.get('industry_track', ''),
        owner_id=data.get('owner_id') or session.get('user_id'),
        expected_date=data.get('expected_date', ''),
        notes=data.get('notes', ''),
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'ok': True, 'id': project.id})


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def api_project_update(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json() or {}
    for k in ['title', 'company_id', 'stage', 'amount', 'industry_track',
              'owner_id', 'expected_date', 'settled_date', 'notes', 'space_id']:
        if k in data:
            setattr(project, k, data[k])
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 跟进记录 ====================
@app.route('/api/projects/<int:project_id>/followups', methods=['GET'])
@login_required
def api_followup_list(project_id):
    followups = FollowUp.query.filter_by(project_id=project_id).order_by(
        FollowUp.created_at.desc()).all()
    return jsonify({'followups': [f.to_dict() for f in followups]})


@app.route('/api/projects/<int:project_id>/followups', methods=['POST'])
@login_required
def api_followup_add(project_id):
    data = request.get_json() or {}
    fu = FollowUp(
        project_id=project_id,
        content=data.get('content', ''),
        next_step=data.get('next_step', ''),
        contact_person=data.get('contact_person', ''),
        follow_date=data.get('follow_date', datetime.utcnow().strftime('%Y-%m-%d')),
        created_by=session.get('user_id'),
    )
    db.session.add(fu)
    db.session.commit()
    return jsonify({'ok': True, 'followup': fu.to_dict()})


# ==================== 客商库 ====================
@app.route('/admin/companies')
@login_required
def admin_companies():
    page = request.args.get('page', 1, type=int)
    ctype = request.args.get('type', '')
    track = request.args.get('track', '')
    search = request.args.get('search', '').strip()

    query = Company.query
    if ctype:
        query = query.filter_by(company_type=ctype)
    if track:
        query = query.filter_by(industry_track=track)
    if search:
        query = query.filter(Company.name.contains(search))

    pagination = query.order_by(Company.name).paginate(page=page, per_page=30, error_out=False)
    tracks = sorted(set(c.industry_track for c in Company.query.all() if c.industry_track))
    return render_template('admin/companies.html',
                           companies=pagination.items, pagination=pagination,
                           current_type=ctype, current_track=track,
                           search=search, tracks=tracks)


@app.route('/api/companies', methods=['POST'])
@login_required
def api_company_add():
    data = request.get_json() or {}
    company = Company(
        name=data.get('name', ''),
        company_type=data.get('company_type', 'target'),
        industry_track=data.get('industry_track', ''),
        scale=data.get('scale', ''),
        city=data.get('city', ''),
        address=data.get('address', ''),
        lat=data.get('lat'),
        lng=data.get('lng'),
        contact_person=data.get('contact_person', ''),
        contact_phone=data.get('contact_phone', ''),
        website=data.get('website', ''),
        description=data.get('description', ''),
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({'ok': True, 'id': company.id})


@app.route('/api/companies/<int:company_id>', methods=['PUT'])
@login_required
def api_company_update(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.get_json() or {}
    for k in ['name', 'company_type', 'industry_track', 'scale', 'city', 'address',
              'lat', 'lng', 'contact_person', 'contact_phone', 'website', 'description', 'status']:
        if k in data:
            setattr(company, k, data[k])
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 空间管理 ====================
@app.route('/admin/spaces')
@login_required
@role_required('admin', 'manager')
def admin_spaces():
    incubator = Space.query.filter_by(zone='孵化区').all()
    factory = Space.query.filter_by(zone='制造区').all()
    return render_template('admin/spaces.html', incubator=incubator, factory=factory)


@app.route('/api/spaces/<int:space_id>', methods=['PUT'])
@login_required
@role_required('admin', 'manager')
def api_space_update(space_id):
    space = Space.query.get_or_404(space_id)
    data = request.get_json() or {}
    for k in ['name', 'zone', 'building', 'floor', 'total_area', 'available_area',
              'floor_height', 'load_capacity', 'power_supply', 'supporting',
              'rent_desc', 'status']:
        if k in data:
            setattr(space, k, data[k])
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 政策管理 ====================
@app.route('/admin/policies')
@login_required
@role_required('admin', 'manager')
def admin_policies():
    policies = Policy.query.order_by(Policy.publish_date.desc()).all()
    return render_template('admin/policies.html', policies=policies)


@app.route('/api/policies', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def api_policy_add():
    data = request.get_json() or {}
    policy = Policy(
        title=data.get('title', ''),
        policy_type=data.get('policy_type', ''),
        issuing_dept=data.get('issuing_dept', ''),
        summary=data.get('summary', ''),
        content=data.get('content', ''),
        applicable_conditions=data.get('applicable_conditions', ''),
        publish_date=data.get('publish_date', datetime.utcnow().strftime('%Y-%m-%d')),
    )
    db.session.add(policy)
    db.session.commit()
    return jsonify({'ok': True, 'id': policy.id})


@app.route('/api/policies/<int:policy_id>', methods=['PUT'])
@login_required
@role_required('admin', 'manager')
def api_policy_update(policy_id):
    policy = Policy.query.get_or_404(policy_id)
    data = request.get_json() or {}
    for k in ['title', 'policy_type', 'issuing_dept', 'summary', 'content',
              'applicable_conditions', 'publish_date', 'status']:
        if k in data:
            setattr(policy, k, data[k])
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 新闻管理 ====================
@app.route('/admin/articles')
@login_required
@role_required('admin', 'manager')
def admin_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin/articles.html', articles=articles)


@app.route('/api/articles', methods=['POST'])
@login_required
@role_required('admin', 'manager')
def api_article_add():
    data = request.get_json() or {}
    article = Article(
        title=data.get('title', ''),
        category=data.get('category', '园区动态'),
        summary=data.get('summary', ''),
        content=data.get('content', ''),
        cover_image=data.get('cover_image', ''),
        is_published=data.get('is_published', False),
        publish_date=data.get('publish_date', datetime.utcnow().strftime('%Y-%m-%d')),
    )
    db.session.add(article)
    db.session.commit()
    return jsonify({'ok': True, 'id': article.id})


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@login_required
@role_required('admin', 'manager')
def api_article_update(article_id):
    article = Article.query.get_or_404(article_id)
    data = request.get_json() or {}
    for k in ['title', 'category', 'summary', 'content', 'cover_image',
              'is_published', 'publish_date']:
        if k in data:
            setattr(article, k, data[k])
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 园区实景图管理 ====================
@app.route('/admin/park-images')
@login_required
@role_required('admin', 'manager')
def admin_park_images():
    return render_template('admin/park_images.html')


# ==================== 用户管理 ====================
@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@app.route('/api/users', methods=['POST'])
@login_required
@role_required('admin')
def api_user_add():
    data = request.get_json() or {}
    if User.query.filter_by(username=data.get('username', '')).first():
        return jsonify({'ok': False, 'msg': '用户名已存在'}), 400
    user = User(
        username=data.get('username', ''),
        display_name=data.get('display_name', ''),
        role=data.get('role', 'staff'),
        phone=data.get('phone', ''),
    )
    user.password_hash = generate_password_hash(data.get('password', '123456'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'ok': True, 'user': user.to_dict()})


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@role_required('admin')
def api_user_update(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    for k in ['display_name', 'role', 'phone', 'is_active']:
        if k in data:
            setattr(user, k, data[k])
    if data.get('password'):
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'ok': True})


# ==================== 数据 API ====================
@app.route('/api/stats/dashboard')
@login_required
def api_dashboard_stats():
    from sqlalchemy import func
    return jsonify({
        'lead_total': Lead.query.count(),
        'project_total': Project.query.count(),
        'project_signed': Project.query.filter_by(stage='签约').count(),
        'project_amount': db.session.query(func.sum(Project.amount)).filter_by(stage='签约').scalar() or 0,
        'company_total': Company.query.count(),
        'space_available': Space.query.filter_by(status='available').count(),
    })


@app.route('/api/stats/map')
def api_map_companies():
    """地图数据：企业坐标"""
    companies = Company.query.filter(
        Company.lat.isnot(None), Company.lng.isnot(None), Company.status == 'active'
    ).all()
    return jsonify({
        'companies': [{
            'id': c.id, 'name': c.name, 'city': c.city,
            'lat': c.lat, 'lng': c.lng,
            'track': c.industry_track, 'type': c.company_type
        } for c in companies]
    })


@app.route('/api/industry-chain')
def api_industry_chain():
    """产业链数据（供 ECharts 使用）"""
    chains = IndustryChain.query.order_by(IndustryChain.sort_order).all()
    # 建立 id → name 映射
    id_to_name = {c.id: c.name for c in chains}
    nodes = []
    links = []
    for c in chains:
        nodes.append({
            'id': c.id, 'name': c.name, 'track': c.track,
            'position': c.chain_position, 'gap': c.gap_level,
            'description': c.description or '',
        })
        if c.parent_id and c.parent_id in id_to_name:
            links.append({
                'source': id_to_name[c.parent_id],
                'target': c.name
            })
    return jsonify({'nodes': nodes, 'links': links})


# ==================== 热力图数据 ====================
def _build_heatmap_data():
    """构建热力图数据（供内部和公开 API 共用）"""
    companies = Company.query.filter(
        Company.lat.isnot(None), Company.lng.isnot(None), Company.status == 'active'
    ).all()

    scale_weight = {'大型': 1.0, '中型': 0.6, '小型': 0.35, '初创': 0.15}

    points = []
    for c in companies:
        intensity = scale_weight.get(c.scale, 0.3)
        if c.company_type == 'settled':
            intensity *= 1.4
        points.append({
            'lat': c.lat, 'lng': c.lng,
            'intensity': round(intensity, 2),
            'name': c.name, 'track': c.industry_track or '',
            'scale': c.scale or '',
        })

    # 长株潭产业集聚区种子数据 — 基于实际产业园区分布，确保热力图有足够密度
    seed_clusters = [
        # 益阳高新区（核心区）
        {'lat': 28.5539, 'lng': 112.3552, 'intensity': 1.0, 'track': '装备智能', 'label': '益阳高新区数字经济产业园'},
        {'lat': 28.5450, 'lng': 112.3480, 'intensity': 0.8, 'track': '智能感知', 'label': '湖南未来光电技术研究院'},
        {'lat': 28.5600, 'lng': 112.3620, 'intensity': 0.7, 'track': '算力配套', 'label': '益阳智算中心'},
        {'lat': 28.5350, 'lng': 112.3400, 'intensity': 0.5, 'track': '装备智能', 'label': '三一中阳产业园'},
        {'lat': 28.5700, 'lng': 112.3700, 'intensity': 0.5, 'track': '工业视觉', 'label': '信维电科'},
        {'lat': 28.5480, 'lng': 112.3300, 'intensity': 0.4, 'track': '智能感知', 'label': '麓宇光电'},
        # 长沙高新区
        {'lat': 28.2200, 'lng': 112.9300, 'intensity': 1.0, 'track': '装备智能', 'label': '长沙高新区'},
        {'lat': 28.2100, 'lng': 112.9200, 'intensity': 0.9, 'track': '智能感知', 'label': '中联重科'},
        {'lat': 28.2300, 'lng': 112.9450, 'intensity': 0.8, 'track': '算力配套', 'label': '国家超算长沙中心'},
        {'lat': 28.2350, 'lng': 112.9150, 'intensity': 0.6, 'track': '工业视觉', 'label': '长沙智能制造研究总院'},
        {'lat': 28.2000, 'lng': 112.9400, 'intensity': 0.5, 'track': '装备智能', 'label': '三一重工'},
        {'lat': 28.2150, 'lng': 112.9250, 'intensity': 0.5, 'track': '智能感知', 'label': '景嘉微电子'},
        {'lat': 28.2250, 'lng': 112.9350, 'intensity': 0.4, 'track': '工业视觉', 'label': '科创信息'},
        # 长沙经开区
        {'lat': 28.1900, 'lng': 113.0800, 'intensity': 0.9, 'track': '装备智能', 'label': '长沙经开区'},
        {'lat': 28.1800, 'lng': 113.0700, 'intensity': 0.7, 'track': '装备智能', 'label': '铁建重工'},
        {'lat': 28.2000, 'lng': 113.0900, 'intensity': 0.6, 'track': '工业视觉', 'label': '蓝思科技星沙基地'},
        {'lat': 28.1700, 'lng': 113.0750, 'intensity': 0.5, 'track': '智能感知', 'label': '国科微电子'},
        # 株洲高新区
        {'lat': 27.8300, 'lng': 113.1300, 'intensity': 0.8, 'track': '装备智能', 'label': '株洲高新区'},
        {'lat': 27.8200, 'lng': 113.1400, 'intensity': 0.7, 'track': '装备智能', 'label': '中车株洲所'},
        {'lat': 27.8400, 'lng': 113.1250, 'intensity': 0.6, 'track': '智能感知', 'label': '株洲时代新材'},
        {'lat': 27.8250, 'lng': 113.1350, 'intensity': 0.5, 'track': '工业视觉', 'label': '麦格米特'},
        # 湘潭高新区
        {'lat': 27.8300, 'lng': 112.9400, 'intensity': 0.6, 'track': '装备智能', 'label': '湘潭高新区'},
        {'lat': 27.8200, 'lng': 112.9500, 'intensity': 0.5, 'track': '智能感知', 'label': '湘电风能'},
        {'lat': 27.8400, 'lng': 112.9350, 'intensity': 0.4, 'track': '工业视觉', 'label': '桑顿新能源'},
        # 长沙麓谷
        {'lat': 28.2350, 'lng': 112.8900, 'intensity': 0.8, 'track': '算力配套', 'label': '长沙麓谷'},
        {'lat': 28.2400, 'lng': 112.8800, 'intensity': 0.7, 'track': '智能感知', 'label': '安克创新'},
        {'lat': 28.2300, 'lng': 112.8850, 'intensity': 0.6, 'track': '工业视觉', 'label': '拓维信息'},
        {'lat': 28.2450, 'lng': 112.8950, 'intensity': 0.5, 'track': '装备智能', 'label': '长城信息'},
    ]

    for s in seed_clusters:
        points.append({
            'lat': s['lat'], 'lng': s['lng'],
            'intensity': s['intensity'],
            'name': s['label'],
            'track': s['track'],
            'scale': '',
        })

    # 无精确坐标但有城市信息的企业，用城市中心点
    city_centers = {
        '长沙': (28.2282, 112.9388), '株洲': (27.8277, 113.1340),
        '湘潭': (27.8297, 112.9441), '益阳': (28.5539, 112.3552),
    }
    city_companies = Company.query.filter(
        (Company.lat.is_(None)) | (Company.lng.is_(None)),
        Company.status == 'active', Company.city.isnot(None)
    ).all()
    for c in city_companies:
        for city_key, (clat, clng) in city_centers.items():
            if city_key in (c.city or ''):
                points.append({
                    'lat': clat, 'lng': clng, 'intensity': 0.3,
                    'name': c.name, 'track': c.industry_track or '',
                    'scale': c.scale or '',
                })
                break

    return {'points': points, 'total': len(points)}


@app.route('/api/stats/heatmap')
@login_required
def api_heatmap_data():
    """产业密度热力图数据（需登录）"""
    return jsonify(_build_heatmap_data())


@app.route('/api/public/heatmap')
def api_public_heatmap():
    """公开热力图数据（无需登录）"""
    return jsonify(_build_heatmap_data())


# ==================== 坐标填充 ====================
@app.route('/api/companies/geocode-all', methods=['POST'])
@login_required
def api_geocode_all():
    """批量填充所有缺失坐标的企业"""
    from utils.data_fetcher import batch_geocode_companies
    result = batch_geocode_companies(db, Company)
    return jsonify({'ok': True, **result})


@app.route('/api/companies/<int:company_id>/geocode', methods=['POST'])
@login_required
def api_company_geocode(company_id):
    """单个企业坐标填充"""
    from utils.data_fetcher import geocode_company
    company = Company.query.get_or_404(company_id)
    lat, lng = geocode_company(company.name)
    if lat and lng:
        company.lat = lat
        company.lng = lng
        db.session.commit()
        return jsonify({'ok': True, 'lat': lat, 'lng': lng})
    return jsonify({'ok': False, 'msg': '坐标获取失败，请确认企业名称在天眼查中可查'}), 400


# ==================== 天眼查集成 ====================
@app.route('/api/tianyancha/status')
@login_required
def api_tianyancha_status():
    """检查天眼查 CLI 是否已配置"""
    from utils.data_fetcher import check_configured
    return jsonify({'ok': True, 'configured': check_configured()})


@app.route('/api/tianyancha/search', methods=['POST'])
@login_required
def api_tianyancha_search():
    """搜索企业"""
    from utils.data_fetcher import check_configured, search_companies

    if not check_configured():
        return jsonify({'ok': False, 'msg': '天眼查 CLI 未配置，请先安装并登录 tyc 命令行工具'}), 400

    data = request.get_json() or {}
    keyword = data.get('keyword', '').strip()
    if len(keyword) < 2:
        return jsonify({'ok': False, 'msg': '请输入至少2个字符的关键词'}), 400

    results = search_companies(keyword)
    return jsonify({'ok': True, 'results': results})


@app.route('/api/tianyancha/import', methods=['POST'])
@login_required
def api_tianyancha_import():
    """从天眼查搜索结果导入企业到客商库"""
    from utils.data_fetcher import fetch_company_detail

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    tianyancha_id = data.get('tianyancha_id', '').strip()

    if not name:
        return jsonify({'ok': False, 'msg': '企业名称不能为空'}), 400

    # 检查是否已存在
    existing = Company.query.filter_by(name=name).first()
    if existing:
        # 已存在，更新天眼查ID
        if tianyancha_id:
            existing.tianyancha_id = tianyancha_id
            db.session.commit()
        return jsonify({'ok': True, 'id': existing.id, 'existed': True})

    # 尝试获取详细信息
    detail = fetch_company_detail(name) or {}

    # 自动匹配赛道
    track = data.get('industry_track', '')
    if not track:
        desc_text = (detail.get('scope', '') + detail.get('industry', '') + detail.get('description', '') + name).lower()
        track = _auto_match_track(desc_text)

    company = Company(
        name=name,
        tianyancha_id=tianyancha_id,
        company_type=data.get('company_type', 'target'),
        industry_track=track,
        scale=_normalize_scale(detail.get('scale', '') or detail.get('staff_num_range', '')),
        city=detail.get('city', ''),
        address=detail.get('address', ''),
        contact_phone=detail.get('phone', ''),
        contact_email=detail.get('email', ''),
        website=detail.get('website', ''),
        description=detail.get('description', detail.get('scope', '')),
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({'ok': True, 'id': company.id, 'existed': False})


@app.route('/api/companies/<int:company_id>/enrich', methods=['POST'])
@login_required
def api_company_enrich(company_id):
    """从天眼查同步企业详细信息"""
    from utils.data_fetcher import fetch_company_detail

    company = Company.query.get_or_404(company_id)
    req_data = request.get_json() or {}
    tianyancha_id = req_data.get('tianyancha_id')

    if not tianyancha_id and not company.tianyancha_id:
        # 尝试通过名称搜索
        from utils.data_fetcher import resolve_company
        name, tyc_id = resolve_company(company.name)
        if name and tyc_id:
            company.tianyancha_id = tyc_id
            tianyancha_id = tyc_id
        else:
            return jsonify({'ok': False, 'msg': f'未找到 "{company.name}" 的天眼查记录，请手动录入天眼查ID'}), 400

    tid = tianyancha_id or company.tianyancha_id
    detail = fetch_company_detail(company.name)
    if not detail:
        return jsonify({'ok': False, 'msg': '获取企业详情失败，请检查天眼查CLI配置'}), 500

    # 更新字段（不覆盖已有的手动填写内容，除非为空）
    for field, src in [('website', 'website'), ('city', 'city'),
                        ('address', 'address'), ('description', 'description')]:
        if detail.get(src) and not getattr(company, field):
            setattr(company, field, detail[src])

    if detail.get('phone') and not company.contact_phone:
        company.contact_phone = detail['phone']
    if detail.get('email') and not company.contact_email:
        company.contact_email = detail['email']

    # 自动匹配赛道（如果还没设置）
    if not company.industry_track:
        desc_text = (detail.get('scope', '') + detail.get('industry', '') + detail.get('description', '') + company.name).lower()
        company.industry_track = _auto_match_track(desc_text)

    # 规模
    if detail.get('scale') and not company.scale:
        company.scale = _normalize_scale(detail['scale'])

    db.session.commit()
    return jsonify({'ok': True, 'company': company.to_dict()})


@app.route('/api/companies/<int:company_id>/sync-bidding', methods=['POST'])
@login_required
def api_company_sync_bidding(company_id):
    """同步企业招投标数据"""
    from utils.data_fetcher import sync_bidding_for_company

    company = Company.query.get_or_404(company_id)
    count = sync_bidding_for_company(company.name, db, BiddingRecord, Company)
    return jsonify({'ok': True, 'new_count': count, 'msg': f'新增 {count} 条招投标记录'})


def _auto_match_track(text):
    """根据文本内容自动匹配产业赛道"""
    if not text:
        return ''
    for kw in ['传感器', '光电', '感知', '激光雷达', '毫米波', '红外']:
        if kw in text:
            return '智能感知'
    for kw in ['视觉', '检测', '质检', 'AOI', '缺陷', '成像', '相机']:
        if kw in text:
            return '工业视觉'
    for kw in ['装备', '数控', '机床', '机器人', '机械臂', 'AGV', '数字孪生', '工业软件']:
        if kw in text:
            return '装备智能'
    for kw in ['算力', '数据中心', '服务器', '存储', 'GPU', '云计算', 'IDC']:
        if kw in text:
            return '算力配套'
    return ''


def _normalize_scale(scale_str):
    """标准化企业规模字段"""
    if not scale_str:
        return ''
    s = scale_str.lower().replace('人以上', '').replace('人以下', '')
    # 天眼查 staffNumRange 格式: "10000人以上"
    try:
        n = int(''.join(c for c in s.split('-')[0] if c.isdigit()))
    except ValueError:
        n = 0
    if n >= 10000 or any(w in s for w in ['大型', '上市', '集团']):
        return '大型'
    if n >= 1000 or '中型' in s:
        return '中型'
    if n >= 100 or '小型' in s:
        return '小型'
    if n > 0 or '初创' in s or '创业' in s:
        return '初创'
    return ''


# ==================== 启动 ====================
if __name__ == '__main__':
    with app.app_context():
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yiyang_invest.db')
        if not os.path.exists(db_path):
            print('⚠️  数据库未初始化，请先运行: python3 seed_data.py')
        else:
            print('✓ 数据库已就绪')
    app.run(debug=True, host='0.0.0.0', port=5096)
