import requests
import json
from pprint import pprint
import time

def diagnose_differences():
    """诊断浏览器请求和Python请求的差异"""
    
    # Python请求的示例
    python_headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': '你的token',
        'batchid': 'e49350a1926a4bfb95cf24eb361411c3',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'route=e8621a4a430d4c44ae231be5b47e4a48; Authorization=你的token',
        'referer': 'https://xsxk.nuist.edu.cn/xsxk/elective/grablessons?batchId=e49350a1926a4bfb95cf24eb361411c3',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...'
    }
    
    # 浏览器可能有而Python缺少的头部
    missing_headers = [
        'Connection',  # keep-alive
        'Upgrade-Insecure-Requests',  # 1
        'Sec-Fetch-Site',  # same-origin
        'Sec-Fetch-Mode',  # cors
        'Sec-Fetch-Dest',  # empty
        'Accept-Encoding',  # 浏览器会发送完整的编码
        'Accept-Language',  # 完整的语言列表
        'Cache-Control',  # no-cache
        'Pragma',  # no-cache
        'X-Requested-With',  # XMLHttpRequest
    ]
    
    print("可能缺少的请求头:")
    for header in missing_headers:
        print(f"  - {header}")
    
    # 测试不同的User-Agent
    user_agents = [
        # 你当前的User-Agent
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        # 尝试更常见的
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # 移动端User-Agent
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    ]
    
    return missing_headers, user_agents

def test_different_approaches():
    """测试不同的请求方法"""
    
    test_cases = [
        {
            'name': '方法1: 完整浏览器模拟',
            'headers': {
                'Host': 'xsxk.nuist.edu.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        },
        {
            'name': '方法2: 最小化请求',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        },
        {
            'name': '方法3: 带时间戳',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Timestamp': str(int(time.time() * 1000)),
            }
        }
    ]
    
    # 测试每个方法
    url = "https://xsxk.nuist.edu.cn/xsxk/elective/clazz/add"
    data = {
        'clazzType': 'FANKC',
        'clazzId': '2025202621300051504',
        'secretVal': 'gvQAbZNbV7WUcNlo2NuGHjRh1xL6it12PcEDhIKIT98VtYv/C4GCVAMRHP4p6JY7N+LoCHCDvgk+TwP7XriXtRFAmN9sxVOkSqUBfbZ5cZANkJ1lo+IiEVQpHQN2zFK/FBlB6jLF1+dTEzuN8Eg6zQnDwCmejXIXgBeYHExT9R/s='
    }
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"测试: {test['name']}")
        print(f"请求头: {json.dumps(test['headers'], indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(url, headers=test['headers'], data=data, timeout=10)
            print(f"状态码: {response.status_code}")
            if response.headers.get('content-type', '').startswith('application/json'):
                result = response.json()
                print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            else:
                print(f"响应文本: {response.text[:200]}")
        except Exception as e:
            print(f"错误: {e}")

# 运行诊断
diagnose_differences()
test_different_approaches()