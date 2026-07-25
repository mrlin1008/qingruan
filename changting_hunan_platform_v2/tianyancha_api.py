"""
天眼查数据接口 — 基于 tyc CLI（162个工具）
前置条件: npm install -g tyc-cli && tyc init --authorization "your_token"
"""
import subprocess
import json


def _run_tyc(args, timeout=60):
    """调用 tyc CLI 并返回解析后的 JSON"""
    cmd = ['tyc', '--compact'] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            stderr = result.stderr.strip()
            if 'Unauthorized' in stderr or '401' in stderr or '403' in stderr:
                return {'error': 'unauthorized', 'message': '天眼查API未认证。请在终端运行: tyc login'}
            return {'error': 'cli_error', 'message': stderr or f'退出码 {result.returncode}'}
        if not result.stdout.strip():
            return []
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {'error': 'timeout', 'message': '请求超时'}
    except json.JSONDecodeError:
        return {'error': 'parse_error', 'message': f'无法解析返回数据: {result.stdout[:200]}'}
    except FileNotFoundError:
        return {'error': 'not_installed', 'message': 'tyc CLI 未安装。请运行: npm install -g tyc-cli'}


def check_configured():
    """检查 tyc CLI 是否已配置"""
    result = _run_tyc(['company', 'base-info', '华为'], timeout=10)
    if isinstance(result, dict) and result.get('error') == 'unauthorized':
        return False, '未认证。请运行: tyc login  或  tyc init --authorization "your_token"'
    if isinstance(result, dict) and result.get('error') == 'not_installed':
        return False, 'tyc CLI 未安装。请运行: npm install -g tyc-cli'
    return True, '已配置'


def resolve_company(keyword):
    """L0 实体锚定：简称 → 精确企业全名"""
    result = _run_tyc(['company', 'companies', keyword], timeout=30)
    if isinstance(result, dict) and 'error' in result:
        return None
    # tyc 返回格式: {"items": [...], "_summary": "..."}
    items = result.get('items', []) if isinstance(result, dict) else result
    if isinstance(items, list) and len(items) > 0:
        return items[0].get('name', keyword)
    return keyword


def fetch_bidding(company_name, page_num=1):
    """
    从天眼查获取指定公司的招投标信息（自动名称解析 + tyc CLI L2）
    返回: list[dict]
    """
    # 先尝试 L0 名称解析
    full_name = resolve_company(company_name)
    search_name = full_name if full_name else company_name

    result = _run_tyc(['operation', 'bidding-info', search_name], timeout=30)

    if isinstance(result, dict) and 'error' in result:
        return result
    # tyc 返回格式: {"items": [...], "total": N, "_summary": "..."}
    items = result.get('items', []) if isinstance(result, dict) else result
    if not isinstance(items, list):
        return []

    records = []
    for item in items:
        records.append({
            'project_name': item.get('title') or item.get('projectName', ''),
            'bidder_name': item.get('purchaser') or item.get('buyer', company_name),
            'winner_name': item.get('winner') or item.get('supplier') or item.get('bidWinner', ''),
            'bid_amount': _parse_amount(item.get('amount') or item.get('bidAmount', '')),
            'publish_date': item.get('publishDate') or item.get('publishTime') or item.get('announceDate', ''),
            'bid_url': item.get('bidUrl', ''),  # 天眼查移动端详情页直链
            'source_url': item.get('sourceUrl') or item.get('url', ''),
            'summary': item.get('summary') or item.get('abstract', ''),
            'source': '天眼查CLI',
        })
    return records


def search_bids_cross(keyword):
    """
    跨公司搜索招投标（使用 tyc CLI L3 工具）
    按项目名称/采购人等关键词搜索
    """
    result = _run_tyc(['operation', 'bids', keyword], timeout=30)
    if isinstance(result, dict) and 'error' in result:
        return result
    # tyc CLI 返回 {"items": [...], ...} 或直接是 list
    if isinstance(result, dict):
        items = result.get('items', [])
    elif isinstance(result, list):
        items = result
    else:
        return []

    records = []
    for item in items:
        records.append({
            'project_name': item.get('title') or item.get('projectName', ''),
            'bidder_name': item.get('purchaser') or item.get('buyer', ''),
            'winner_name': item.get('winner') or item.get('bidWinner', ''),
            'bid_amount': _parse_amount(item.get('amount') or item.get('bidAmount', '')),
            'publish_date': item.get('publishDate') or item.get('publishTime') or item.get('announceDate', ''),
            'source_url': item.get('sourceUrl') or item.get('url', ''),
            'bid_url': item.get('bidUrl', ''),
            'summary': item.get('summary') or item.get('abstract', ''),
            'source': f'天眼查(关键词:{keyword})',
        })
    return records


def _parse_amount(val):
    if not val:
        return 0
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(str(val).replace('万', '').replace('元', '').replace(',', '').strip() or 0)
    except ValueError:
        return 0


def search_bidding_sync(company_name, max_results=20):
    """兼容 Flask 调用的同步接口"""
    result = fetch_bidding(company_name)
    if isinstance(result, dict) and 'error' in result:
        return result
    return result[:max_results]


def set_token(token):
    """兼容旧版接口：tyc CLI 已通过 OAuth 登录，不需要手动设 token"""
    print("tyc CLI 已通过 tyc login 完成 OAuth 认证，无需手动设置 Token")
    ok, msg = check_configured()
    print(msg)


def get_token():
    """检查 tyc CLI 配置状态"""
    ok, msg = check_configured()
    return f'{"✅" if ok else "❌"} {msg}'


def bulk_fetch_bidding(customer_names, max_per=20):
    """
    批量获取多个客户的招投标信息
    customer_names: 客户名称列表
    返回: {name: [records]}
    """
    results = {}
    for name in customer_names:
        print(f'  查询: {name}...')
        data = fetch_bidding(name)
        if isinstance(data, list):
            results[name] = data[:max_per]
        else:
            results[name] = []
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == '--set-token':
        set_token(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == '--token':
        print(get_token())
    elif len(sys.argv) >= 2:
        company = sys.argv[1]
        print(f'🔍 {company} 招投标信息:\n')
        data = fetch_bidding(company)
        if isinstance(data, dict) and 'error' in data:
            print(f"❌ {data['message']}")
        elif not data:
            print('未找到记录')
        else:
            for i, r in enumerate(data):
                print(f'{i+1}. {r["project_name"][:80]}')
                print(f'   招标方: {r["bidder_name"]}  中标: {r["winner_name"]}  金额: {r["bid_amount"]}万  {r["publish_date"]}')
                print()
    else:
        print("天眼查 CLI 接口（基于 tyc CLI · 162工具）")
        print("用法:")
        print("  python3 tianyancha_api.py --set-token \"your_token\"  配置认证")
        print("  python3 tianyancha_api.py --token                     检查状态")
        print("  python3 tianyancha_api.py \"公司名称\"                  查询招投标")
        print()
        print("前置条件: npm install -g tyc-cli")
        print("获取Token: https://open.tianyancha.com")
