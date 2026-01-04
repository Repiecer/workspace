import requests
import time
import json
from datetime import datetime

class CourseSelectorAdvanced:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://xsxk.nuist.edu.cn"
        self._init_complete_headers()
        
    def _init_complete_headers(self):
        """初始化完整的浏览器级别请求头"""
        # 完整的浏览器请求头
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'Host': 'xsxk.nuist.edu.cn',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        
    def set_auth(self, token: str, batch_id: str):
        """设置认证信息 - 更完整的方式"""
        # 更新头部
        self.session.headers.update({
            'authorization': token,
            'batchid': batch_id,
            'Origin': self.base_url,
        })
        
        # 更完整的 Cookie 设置
        self.session.cookies.update({
            'route': 'e8621a4a430d4c44ae231be5b47e4a48',
            'Authorization': token,
            # 可能需要的其他 Cookie
            'JSESSIONID': '',  # 如果有的话
        })
        
        # 设置 Referer
        referer = f"{self.base_url}/xsxk/elective/grablessons?batchId={batch_id}"
        self.session.headers['Referer'] = referer
        
    def _add_timestamp_headers(self):
        """添加时间戳相关头部（某些系统需要）"""
        timestamp = int(time.time() * 1000)
        self.session.headers.update({
            'X-Requested-With': 'XMLHttpRequest',
            'X-Timestamp': str(timestamp),
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })
        
    def _simulate_browser_flow(self):
        """模拟浏览器访问流程"""
        print("模拟浏览器访问流程...")
        
        # 1. 先访问首页获取初始 Cookie
        try:
            home_url = f"{self.base_url}/xsxk/elective/index"
            print(f"1. 访问首页: {home_url}")
            resp = self.session.get(home_url, timeout=5)
            print(f"   状态码: {resp.status_code}")
            print(f"   获得 Cookie: {dict(self.session.cookies)}")
        except:
            print("   跳过首页访问")
            
        # 2. 访问选课页面
        batch_id = self.session.headers.get('batchid')
        if batch_id:
            grab_url = f"{self.base_url}/xsxk/elective/grablessons?batchId={batch_id}"
            print(f"2. 访问选课页面: {grab_url}")
            resp = self.session.get(grab_url, timeout=5)
            print(f"   状态码: {resp.status_code}")
            
    def select_course_with_retry(self, clazz_id: str, secret_val: str, clazz_type: str = "FANKC", retries: int = 3):
        """带重试的选课方法"""
        
        for attempt in range(retries):
            print(f"\n{'='*60}")
            print(f"尝试第 {attempt + 1} 次选课...")
            
            # 每次尝试前模拟浏览器流程
            self._simulate_browser_flow()
            self._add_timestamp_headers()
            
            # 构建请求
            url = f"{self.base_url}/xsxk/elective/clazz/add"
            data = {
                'clazzType': clazz_type,
                'clazzId': clazz_id,
                'secretVal': secret_val
            }
            
            print(f"请求URL: {url}")
            print(f"请求数据: {data}")
            print(f"完整请求头:")
            for k, v in self.session.headers.items():
                print(f"  {k}: {v}")
            
            try:
                # 添加随机延迟，模拟人工操作
                time.sleep(1 + attempt * 0.5)
                
                response = self.session.post(url, data=data, timeout=10)
                print(f"响应状态码: {response.status_code}")
                
                # 打印响应头
                print(f"响应头:")
                for k, v in response.headers.items():
                    if k.lower() in ['content-type', 'server', 'date']:
                        print(f"  {k}: {v}")
                
                # 解析响应
                try:
                    result = response.json()
                    print(f"响应JSON: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
                    # 分析响应
                    msg = result.get('msg', '')
                    
                    if "系统刚重启" in msg:
                        print("检测到'系统刚重启'消息，尝试刷新页面状态...")
                        # 重新模拟浏览器流程
                        continue
                    elif "暂未开始" in msg:
                        print("❌ 选课尚未开始！")
                        return result
                    elif result.get('code') == 200:
                        print("✅ 选课成功！")
                        return result
                    else:
                        print(f"⚠️  其他错误: {msg}")
                        return result
                        
                except json.JSONDecodeError:
                    print(f"响应文本: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"请求异常: {e}")
                
            # 等待后重试
            if attempt < retries - 1:
                wait_time = 2 * (attempt + 1)
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        print("所有重试均失败")
        return None

# 使用示例
def main():
    # 创建高级选课器
    selector = CourseSelectorAdvanced()
    
    # 设置认证信息
    token = "eyJhbGciOiJIUzUxMiJ9.eyJ0aW1lIjoxNzY2OTgwNTgxNDU0LCJsb2dpbl91c2VyX2tleSI6IjIwMjU4MzMwMDUyMCIsInRva2VuIjoicjBjbW0wZHExZWhwNnFtcmdvNGg4ajBsYTAifQ.R5AyilXTIsHQLPfYZs77U4U8Hu987NioGrbS0jb0oUx0M3qDF5atkLQKbx9icXYTGqJfFjZfDum8p4l7nlPBoQ"
    batch_id = "e49350a1926a4bfb95cf24eb361411c3"
    
    selector.set_auth(token, batch_id)
    
    # 课程信息
    course_info = {
        'clazzType': 'FANKC',
        'clazzId': '2025202621300051504',
        'secretVal': 'gvQAbZNbV7WUcNlo2NuGHjRh1xL6it12PcEDhIKIT98VtYv/C4GCVAMRHP4p6JY7N+LoCHCDvgk+TwP7XriXtRFAmN9sxVOkSqUBfbZ5cZANkJ1lo+IiEVQpHQN2zFK/FBlB6jLF1+dTEzuN8Eg6zQnDwCmejXIXgBeYHExT9R/s='
    }
    
    # 执行选课
    result = selector.select_course_with_retry(
        clazz_id=course_info['clazzId'],
        secret_val=course_info['secretVal'],
        clazz_type=course_info['clazzType'],
        retries=3
    )
    
    return result

if __name__ == "__main__":
    main()