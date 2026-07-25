"""
天眼查招标信息自动查询工具
需要提供天眼查账号，首次运行需手动登录一次，后续复用session

使用方式：
1. 命令行: python3 tianyancha_scraper.py --company "中芯国际" --login
2. Flask调用: from tianyancha_scraper import search_bidding; results = search_bidding("中芯国际")
"""
import os
import json
import time
import asyncio
from playwright.async_api import async_playwright

SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.tyc_session.json')


async def _new_browser_context(playwright, headless=False):
    """创建浏览器上下文，尝试加载已保存的session"""
    browser = await playwright.chromium.launch(
        headless=headless,
        args=['--disable-blink-features=AutomationControlled']
    )

    # 尝试加载已保存的session
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                storage_state = json.load(f)
            context = await browser.new_context(
                storage_state=storage_state,
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            return browser, context, True  # session loaded
        except Exception:
            pass

    context = await browser.new_context(
        viewport={'width': 1280, 'height': 800},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
    return browser, context, False


async def login_manual():
    """手动登录天眼查，保存session供后续使用"""
    async with async_playwright() as p:
        browser, context, has_session = await _new_browser_context(p, headless=False)
        page = await context.new_page()

        print("🌐 正在打开天眼查登录页...")
        await page.goto('https://www.tianyancha.com/login', wait_until='networkidle', timeout=30000)

        if has_session:
            await page.goto('https://www.tianyancha.com', wait_until='networkidle', timeout=15000)
            if 'login' not in page.url.lower():
                print("✅ 已有有效session，无需重新登录！")
                await browser.close()
                return True
            else:
                print("⚠️  旧session已过期，需要重新登录")

        print("\n📱 请在打开的浏览器中完成登录（手机号/微信扫码均可）")
        print("   等待登录完成...（自动检测，登录后继续）")

        # 自动检测登录完成（最多等5分钟）
        for i in range(150):
            await page.wait_for_timeout(2000)
            current_url = page.url.lower()
            if 'login' not in current_url and 'passport' not in current_url:
                print(f"\n✅ 检测到登录成功！当前页面: {page.url[:60]}")
                break
            if i % 15 == 14:
                print(f"   ...已等待{(i+1)*2}秒，请继续在浏览器中完成登录")

        # 保存session
        storage_state = await context.storage_state()
        with open(SESSION_FILE, 'w') as f:
            json.dump(storage_state, f)
        print("✅ Session已保存到 .tyc_session.json")

        await browser.close()
        return True


async def search_bidding(company_name, max_results=20):
    """
    在天眼查搜索指定公司的招标信息
    返回: list of dict 招标记录
    """
    async with async_playwright() as p:
        browser, context, has_session = await _new_browser_context(p, headless=True)
        page = await context.new_page()

        if not has_session:
            await browser.close()
            return {'error': 'no_session', 'message': '未找到登录session，请先运行: python3 tianyancha_scraper.py --login'}

        results = []
        try:
            # 1. 搜索公司
            search_url = f'https://www.tianyancha.com/search?key={company_name}'
            await page.goto(search_url, wait_until='networkidle', timeout=20000)
            await page.wait_for_timeout(2000)

            # 检查是否需要重新登录
            if 'login' in page.url.lower():
                await browser.close()
                return {'error': 'session_expired', 'message': 'Session已过期，请重新登录: python3 tianyancha_scraper.py --login'}

            # 2. 点击第一个公司结果进入详情
            company_link = await page.query_selector('.search-result-single a, .result-list a, [class*="company"] a')
            if company_link:
                company_url = await company_link.get_attribute('href')
                if company_url:
                    await page.goto(company_url, wait_until='networkidle', timeout=20000)
                    await page.wait_for_timeout(2000)
            else:
                # 可能直接在搜索结果中，尝试找公司名链接
                pass

            # 3. 找"招标信息"或"经营状况"标签
            # 天眼查的招标信息通常在 经营状况 -> 招投标 中
            bid_tab = await page.query_selector('text=招投标')
            if not bid_tab:
                bid_tab = await page.query_selector('text=招标信息')
            if not bid_tab:
                bid_tab = await page.query_selector('[data-id="bid"]')
            if not bid_tab:
                bid_tab = await page.query_selector('a:has-text("招投标")')

            if bid_tab:
                await bid_tab.click()
                await page.wait_for_timeout(3000)
            else:
                # 尝试直接构建URL
                current_url = page.url
                if 'company' in current_url:
                    bid_url = current_url.rstrip('/') + '/bid'
                    await page.goto(bid_url, wait_until='networkidle', timeout=20000)
                    await page.wait_for_timeout(2000)

            # 4. 解析招标列表
            bid_items = await page.query_selector_all('table tr, .bid-item, [class*="bid"] .list-item, .search-result-item')
            if not bid_items:
                bid_items = await page.query_selector_all('.result-list > div, [class*="result"] > div')

            count = 0
            for item in bid_items:
                if count >= max_results:
                    break
                try:
                    text_content = await item.inner_text()
                    if not text_content.strip():
                        continue

                    # 跳过表头
                    if '发布日期' in text_content or '项目名称' in text_content:
                        continue

                    lines = [l.strip() for l in text_content.split('\n') if l.strip()]
                    if len(lines) < 2:
                        continue

                    record = {
                        'bidder_name': company_name,
                        'project_name': lines[0] if len(lines) > 0 else '',
                        'winner_name': '',
                        'bid_amount': 0,
                        'publish_date': '',
                        'source': '天眼查(自动)',
                    }

                    # 尝试从各行提取信息
                    for line in lines:
                        if '万' in line and any(c.isdigit() for c in line):
                            try:
                                amount_str = line.replace(',', '').replace('万', '').strip()
                                record['bid_amount'] = float(amount_str)
                            except ValueError:
                                pass
                        if len(line) == 10 and '-' in line:  # 日期格式 2026-03-15
                            record['publish_date'] = line
                        if '中标' in line or '成交' in line:
                            record['winner_name'] = line.replace('中标方：', '').replace('中标', '').strip()

                    results.append(record)
                    count += 1
                except Exception:
                    continue

        except Exception as e:
            results = {'error': 'scrape_error', 'message': str(e)}
        finally:
            await browser.close()

    return results


def search_bidding_sync(company_name, max_results=20):
    """同步版本，供Flask调用"""
    return asyncio.run(search_bidding(company_name, max_results))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='天眼查招标信息查询工具')
    parser.add_argument('--login', action='store_true', help='手动登录并保存session')
    parser.add_argument('--company', type=str, help='要查询的公司名称')
    parser.add_argument('--max', type=int, default=20, help='最多获取条数')
    args = parser.parse_args()

    if args.login:
        asyncio.run(login_manual())
    elif args.company:
        print(f'🔍 正在查询: {args.company} ...')
        results = asyncio.run(search_bidding(args.company, args.max))
        if isinstance(results, dict) and 'error' in results:
            print(f"❌ {results['message']}")
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
