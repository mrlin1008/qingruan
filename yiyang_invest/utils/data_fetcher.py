"""
益阳高新区智慧招商平台 — 外部数据获取
天眼查企业信息查询 + 招投标数据同步

使用 tyc CLI (v0.3.8+) 的 4 层工具架构:
  L0: tyc company companies <keyword>           — 实体锚定搜索
  L1: tyc company registration-info <keyword>    — 核心登记信息
  L2: tyc company profile / contact-info / scale — 维度下钻
  L2: tyc operation bidding-info <keyword>       — 招投标
  L3: tyc operation bids <keyword>               — 跨公司招投标搜索
"""
import os
import json
import time
import subprocess
from datetime import datetime

# 天眼查 CLI 路径
TYC_CLI = 'tyc'

# AI/光电领域招投标关键词
BIDDING_KEYWORDS = [
    '传感器', '光电', '工业视觉', '机器视觉', 'AI检测',
    '工业软件', '智能制造', '智能装备', '算力', '数据中心',
    '半导体', '芯片', '光学', '激光', '人工智能', '物联网',
    '数字化改造', '数字化转型', '智能制造', '自动化',
]

# 湖南省内标识
HUNAN_MARKERS = ['湖南', '长沙', '益阳', '株洲', '湘潭', '岳阳', '衡阳',
                 '常德', '郴州', '永州', '邵阳', '怀化', '娄底', '张家界', '湘西']


def check_configured():
    """检查天眼查 CLI 是否已配置"""
    try:
        result = subprocess.run([TYC_CLI, '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False


def resolve_company(keyword):
    """
    L0 实体锚定：将企业简称解析为精确全名
    返回: (company_name, tianyancha_id) 或 (None, None)
    """
    try:
        result = subprocess.run(
            [TYC_CLI, 'company', 'companies', keyword, '--pageSize', '1', '--compact'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            items = data.get('items', [])
            if items:
                item = items[0]
                return item.get('name'), str(item.get('id', ''))
    except Exception as e:
        print(f'[天眼查] 企业解析失败: {keyword} - {e}')
    return None, None


def search_companies(keyword, limit=10):
    """
    L0 模糊搜索企业列表
    实际调用: tyc company companies <searchKey> --pageSize <limit>
    返回: [{name, tianyancha_id, legal_person, reg_capital, reg_status,
            established_date, credit_code}]
    """
    try:
        result = subprocess.run(
            [TYC_CLI, 'company', 'companies', keyword, '--pageSize', str(limit), '--compact'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            items = data.get('items', [])
            return [{
                'name': item.get('name', ''),
                'tianyancha_id': str(item.get('id', '')),
                'legal_person': item.get('legalPersonName', ''),
                'reg_capital': item.get('regCapital', ''),
                'reg_status': item.get('regStatus', ''),
                'established_date': (item.get('establishTime') or item.get('estiblishTime') or '')[:10],
                'credit_code': item.get('creditCode', ''),
            } for item in items]
    except Exception as e:
        print(f'[天眼查] 企业搜索失败: {keyword} - {e}')
    return []


def fetch_company_detail(company_name):
    """
    通过企业名称获取详细信息（L1 + L2 组合）:
    - registration-info: 核心登记信息
    - profile: 企业简介
    - contact-info: 联系方式 + 注册地址
    - scale: 企业规模
    返回: dict 或 None
    """
    detail = {}
    try:
        # L1: 核心登记信息
        result = subprocess.run(
            [TYC_CLI, 'company', 'registration-info', company_name, '--compact'],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            # registration-info 输出格式: { sources: { base: {...}, type: {...} } }
            base = data.get('sources', {}).get('base', data)
            detail['name'] = base.get('name', company_name)
            detail['tianyancha_id'] = str(base.get('id', ''))
            detail['legal_person'] = base.get('legalPersonName', '')
            detail['reg_capital'] = base.get('regCapital', '')
            est = base.get('estiblishTime') or base.get('fromTime') or base.get('establishTime') or ''
            detail['established_date'] = est[:10] if est else ''
            detail['credit_code'] = base.get('creditCode', '')
            detail['reg_status'] = base.get('regStatus', '')
            detail['scope'] = base.get('businessScope', base.get('scope', ''))
            detail['industry'] = base.get('industry', '')
            detail['address'] = base.get('regLocation', base.get('address', ''))
            detail['city'] = base.get('city', '')
            detail['phone'] = base.get('phoneNumber', '')
            detail['email'] = base.get('email', '')
            detail['staff_num_range'] = base.get('staffNumRange', '')
            detail['company_org_type'] = base.get('companyOrgType', '')
            detail['reg_institute'] = base.get('regInstitute', '')

        # L2: 企业简介
        result = subprocess.run(
            [TYC_CLI, 'company', 'profile', company_name, '--compact'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            detail['description'] = data.get('profile', '')

        # L2: 联系方式
        result = subprocess.run(
            [TYC_CLI, 'company', 'contact-info', company_name, '--compact'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            detail['phone'] = data.get('phoneNumber', '')
            detail['email'] = data.get('email', '')
            detail['website'] = data.get('website', '')
            # regLocation 作为地址补充
            if data.get('regLocation') and not detail.get('address'):
                detail['address'] = data['regLocation']

        # L2: 企业规模
        result = subprocess.run(
            [TYC_CLI, 'company', 'scale', company_name, '--compact'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            detail['scale'] = data.get('scale', '')

        return detail if detail else None

    except Exception as e:
        print(f'[天眼查] 企业详情获取失败: {company_name} - {e}')
    return detail if detail else None


def fetch_bidding(company_name, page_num=1):
    """
    L2: 获取指定企业的招投标信息
    实际调用: tyc operation bidding-info <searchKey>
    返回: [{project_name, bidder_name, winner_name, bid_amount,
            publish_date, source_url, summary}] 或 []
    """
    try:
        result = subprocess.run(
            [TYC_CLI, 'operation', 'bidding-info', company_name,
             '--pageNum', str(page_num), '--compact'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            records = data.get('items', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            return [{
                'project_name': r.get('title', r.get('projectName', '')),
                'bidder_name': r.get('bidderName', company_name),
                'winner_name': r.get('winnerName', r.get('winBidderName', '')),
                'bid_amount': _parse_amount(r.get('bidAmount', r.get('amount', 0))),
                'publish_date': r.get('publishDate', r.get('publishTime', ''))[:10],
                'source_url': r.get('bidUrl', r.get('sourceUrl', r.get('url', ''))),
                'summary': r.get('description', r.get('summary', r.get('content', ''))),
            } for r in records]
    except Exception as e:
        print(f'[天眼查] 招投标查询失败: {company_name} - {e}')
    return []


def search_bids_cross(keyword):
    """
    L3: 跨公司关键词搜索招投标
    实际调用: tyc operation bids <keyword>
    """
    try:
        result = subprocess.run(
            [TYC_CLI, 'operation', 'bids', keyword, '--compact'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            records = data.get('items', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            return [{
                'project_name': r.get('title', r.get('projectName', '')),
                'bidder_name': r.get('bidderName', ''),
                'winner_name': r.get('winnerName', r.get('winBidderName', '')),
                'bid_amount': _parse_amount(r.get('bidAmount', r.get('amount', 0))),
                'publish_date': r.get('publishDate', r.get('publishTime', ''))[:10],
                'source_url': r.get('bidUrl', r.get('sourceUrl', r.get('url', ''))),
                'summary': r.get('description', r.get('summary', r.get('content', ''))),
            } for r in records]
    except Exception as e:
        print(f'[天眼查] 关键词搜索失败: {keyword} - {e}')
    return []


def sync_bidding_for_company(company_name, db_session, BiddingRecord, Company):
    """同步单个企业的招投标数据到数据库"""
    records = fetch_bidding(company_name)
    company = Company.query.filter_by(name=company_name).first()
    new_count = 0

    for r in records:
        existing = BiddingRecord.query.filter_by(
            project_name=r['project_name'], bidder_name=r['bidder_name']
        ).first()
        if existing:
            continue

        # 关键词匹配赛道
        track = ''
        if r.get('summary') or r.get('project_name'):
            text = (r.get('summary', '') + r.get('project_name', '')).lower()
            for kw in ['传感器', '光电', '感知']:
                if kw in text:
                    track = '智能感知'
                    break
            for kw in ['视觉', '检测', '质检']:
                if kw in text:
                    track = track or '工业视觉'
                    break
            for kw in ['装备', '智能', '机械', '数字孪生']:
                if kw in text:
                    track = track or '装备智能'
                    break
            for kw in ['算力', '数据', '存储', '服务器']:
                if kw in text:
                    track = track or '算力配套'
                    break

        record = BiddingRecord(
            company_id=company.id if company else None,
            project_name=r['project_name'],
            bidder_name=r['bidder_name'],
            winner_name=r['winner_name'],
            bid_amount=r['bid_amount'],
            publish_date=r['publish_date'],
            product_detail=r['summary'],
            source='天眼查',
            source_url=r['source_url'],
            industry_track=track,
        )
        db_session.add(record)
        new_count += 1

    if new_count:
        db_session.session.commit()
        print(f'  [{company_name}] 新增 {new_count} 条招投标记录')
    return new_count


def _parse_amount(val):
    """解析金额为浮点数（万元）"""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        val = val.replace(',', '').replace('，', '').replace('万元', '').replace('万', '').strip()
        try:
            return float(val)
        except ValueError:
            return 0
    return 0


def geocode_company(company_name):
    """
    通过天眼查获取企业经纬度（GCJ-02 坐标系，适配高德地图）
    返回: (lat, lng) 或 (None, None)
    """
    try:
        result = subprocess.run(
            [TYC_CLI, 'company', 'location', company_name, '--compact'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            lat = data.get('latitude')
            lng = data.get('longitude')
            if lat and lng:
                return float(lat), float(lng)
    except Exception as e:
        print(f'[天眼查] 坐标获取失败: {company_name} - {e}')
    return None, None


def batch_geocode_companies(db_session, Company):
    """
    批量填充所有缺失坐标的企业 lat/lng 字段
    返回: {'total': int, 'filled': int, 'failed': int, 'details': [...]}
    """
    companies = Company.query.filter(
        (Company.lat.is_(None)) | (Company.lng.is_(None))
    ).all()

    total = len(companies)
    filled = 0
    failed = 0
    details = []

    for c in companies:
        lat, lng = geocode_company(c.name)
        if lat and lng:
            c.lat = lat
            c.lng = lng
            filled += 1
            details.append({'id': c.id, 'name': c.name, 'lat': lat, 'lng': lng, 'status': 'ok'})
            print(f'  ✓ [{c.name}] → ({lat:.6f}, {lng:.6f})')
        else:
            failed += 1
            details.append({'id': c.id, 'name': c.name, 'status': 'failed'})
            print(f'  ✗ [{c.name}] 坐标获取失败')

    if filled:
        db_session.session.commit()
        print(f'\n批量填充完成: {filled}/{total} 成功, {failed} 失败')

    return {'total': total, 'filled': filled, 'failed': failed, 'details': details}


if __name__ == '__main__':
    print(f'天眼查CLI已配置: {check_configured()}')
    # 测试坐标获取
    name = '蓝思科技股份有限公司'
    lat, lng = geocode_company(name)
    print(f'{name}: lat={lat}, lng={lng}')
