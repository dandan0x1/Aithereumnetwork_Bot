import requests
import json
import os
import random
import time
from datetime import datetime
from urllib.parse import quote
from colorama import init, Fore, Style


def show_copyright():
    """展示版权信息"""
    copyright_info = f"""{Fore.CYAN}
    *****************************************************
    *           X:https://x.com/ariel_sands_dan         *
    *           Tg:https://t.me/sands0x1                *
    *           Aithereumnetwork BOT Version 1.0        *
    *           Copyright (c) 2025                      *
    *           All Rights Reserved                     *
    *****************************************************
    """
    {Style.RESET_ALL}
    print(copyright_info)
    print('=' * 50)
    print(f"{Fore.GREEN}申请key: https://661100.xyz/ {Style.RESET_ALL}")
    print(f"{Fore.RED}联系Dandan: \n QQ:712987787 QQ群:1036105927 \n 电报:sands0x1 电报群:https://t.me/+fjDjBiKrzOw2NmJl \n 微信: dandan0x1{Style.RESET_ALL}")
    print('=' * 50)
    print(f"{Fore.GREEN}动态ip跑脚本推荐： https://www.nstproxy.com/?utm_source=dandan{Style.RESET_ALL}")
    print('=' * 50)

# 初始化 colorama
init(autoreset=True)

# 颜色配置
class Colors:
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    WHITE = Fore.WHITE
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

# 日志记录器
class Logger:
    @staticmethod
    def info(msg):
        print(f"{Colors.WHITE}[✓] {msg}{Colors.RESET}")
    
    @staticmethod
    def warn(msg):
        print(f"{Colors.YELLOW}[⚠] {msg}{Colors.RESET}")
    
    @staticmethod
    def error(msg):
        print(f"{Colors.RED}[✗] {msg}{Colors.RESET}")
    
    @staticmethod
    def success(msg):
        print(f"{Colors.GREEN}[✅] {msg}{Colors.RESET}")
    
    @staticmethod
    def loading(msg):
        print(f"{Colors.CYAN}[→] {msg}{Colors.RESET}")

logger = Logger()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

API_BASE = 'https://api.aithereumnetwork.com/api'
CONFIG_DIR = 'config'
ACCOUNTS_FILE = os.path.join(CONFIG_DIR, 'accounts.json')
PROXY_FILE = os.path.join(CONFIG_DIR, 'proxy.txt')
RF_CODE_FILE = os.path.join(CONFIG_DIR, 'rf_code.txt')

GIFT_CODES = [
    'TGEENDOFDEC',
    'CEXENDOFDEC',
    'DEC31UTC',
    'CMCSOON',
    'AFDSECXR'
]


class AithereumBot:
    def __init__(self, user_id=None, email=None, name=None, proxy=None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.proxy = proxy
        self.user_agent = random.choice(USER_AGENTS)
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.8',
            'content-type': 'application/json',
            'user-agent': self.user_agent,
            'referer': 'https://aithereumnetwork.com/',
            'origin': 'https://aithereumnetwork.com',
        }
        # 设置代理
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy
            }

    @staticmethod
    def generate_random_email():
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        length = random.randint(8, 12)
        username = ''.join(random.choice(chars) for _ in range(length))
        
        domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']
        domain = random.choice(domains)
        
        return f"{username}@{domain}"

    @staticmethod
    def generate_random_name():
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa', 'Tom', 'Anna']
        last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return f"{first_name} {last_name}"

    def get_ip_address(self):
        """获取当前IP地址"""
        try:
            # 尝试从多个IP检测服务获取IP
            ip_services = [
                {'url': 'https://api.ipify.org?format=json', 'key': 'ip'},
                {'url': 'https://api.myip.com', 'key': 'ip'},
                {'url': 'https://ipinfo.io/json', 'key': 'ip'},
                {'url': 'https://httpbin.org/ip', 'key': 'origin'},
            ]
            
            for service_info in ip_services:
                try:
                    response = self.session.get(service_info['url'], timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        # 根据不同服务的返回格式提取IP
                        ip = data.get(service_info['key'])
                        if ip:
                            # 如果是 httpbin.org，origin 可能是 "ip1, ip2" 格式，取第一个
                            if isinstance(ip, str) and ',' in ip:
                                ip = ip.split(',')[0].strip()
                            if ip:
                                logger.loading(f'获取到IP地址: {ip}')
                                return ip
                except Exception as e:
                    continue
            
            logger.warn('无法获取IP地址，将生成随机IP')
            # 如果所有服务都失败，生成一个随机IP
            random_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            logger.info(f'使用随机IP: {random_ip}')
            return random_ip
        except Exception as error:
            logger.warn(f'获取IP地址失败: {str(error)}，使用随机IP')
            random_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            logger.info(f'使用随机IP: {random_ip}')
            return random_ip

    def register_account(self, referral_code):
        try:
            email = AithereumBot.generate_random_email()
            name = AithereumBot.generate_random_name()
            google_id = str(random.randint(100000000000000000, 999999999999999999))
            
            # 获取IP地址
            ip_address = self.get_ip_address()

            payload = {
                'googleId': google_id,
                'email': email,
                'name': name,
                'picture': f'https://ui-avatars.com/api/?name={quote(name)}&background=random',
                'referralCode': referral_code,
                'ipAddress': ip_address
            }

            url = f'{API_BASE}/auth/google'

            response = self.session.post(url, json=payload, headers=self.headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data') or data.get('user') or data
                
                if user_data and user_data.get('_id'):
                    return {
                        'success': True,
                        'userId': user_data['_id'],
                        'email': user_data.get('email', email),
                        'name': user_data.get('name', name),
                        'referralCode': user_data.get('referralCode', 'N/A'),
                        'afdTokens': user_data.get('afdTokens', 0)
                    }

            return {
                'success': False,
                'message': '注册失败 - 响应格式无效',
                'response': response.text
            }
        except requests.exceptions.RequestException as error:
            if hasattr(error, 'response') and error.response is not None:
                try:
                    error_data = error.response.json()
                    return {
                        'success': False,
                        'message': error_data.get('message') or error_data.get('error') or '注册错误',
                        'details': json.dumps(error_data)
                    }
                except:
                    pass
            return {'success': False, 'message': str(error)}

    def get_user_info(self):
        try:
            response = self.session.get(f'{API_BASE}/users/{self.user_id}', headers=self.headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as error:
            logger.error(f'获取用户信息失败: {str(error)}')
            return None

    def get_active_tasks(self):
        try:
            response = self.session.get(f'{API_BASE}/tasks/active', headers=self.headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as error:
            logger.error(f'获取任务列表失败: {str(error)}')
            return None

    def complete_task(self, task_type, task_name, task_id=None):
        try:
            payload = {
                'userId': self.user_id,
                'taskType': task_type,
                'taskName': task_name,
            }

            if task_id:
                payload['taskId'] = task_id

            response = self.session.post(
                f'{API_BASE}/tasks/complete',
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            
            error_data = response.json() if response.text else {}
            return {
                'success': False,
                'message': error_data.get('message', '任务完成失败')
            }
        except Exception as error:
            return {'success': False, 'message': str(error)}

    def daily_check_in(self):
        logger.loading('正在尝试每日签到...')
        result = self.complete_task('daily_checkin', 'Daily Check-in')
        
        if result.get('success'):
            reward = result.get('reward', 0)
            new_balance = result.get('newBalance', 0)
            logger.success(f'每日签到成功！获得 +{reward} $AFD 代币')
            logger.info(f'新余额: {new_balance} $AFD')
            return True
        else:
            logger.warn(f'每日签到: {result.get("message", "失败")}')
            return False

    def complete_tasks(self):
        logger.loading('正在获取活动任务...')
        tasks_data = self.get_active_tasks()

        if not tasks_data or not tasks_data.get('success'):
            logger.error('获取任务列表失败')
            return

        tasks = tasks_data.get('data', [])
        logger.info(f'找到 {len(tasks)} 个活动任务')

        user_info = self.get_user_info()
        completed_task_types = []
        if user_info and user_info.get('success'):
            completed_tasks = user_info.get('data', {}).get('completedTasks', [])
            completed_task_types = [t.get('taskType') for t in completed_tasks if t.get('taskType')]

        for task in tasks:
            task_type = task.get('taskType')
            if task_type in completed_task_types:
                task_title = task.get('title', '未知任务')
                logger.info(f'任务 "{task_title}" 已完成，跳过...')
                continue

            task_title = task.get('title', '未知任务')
            logger.loading(f'正在完成任务: {task_title}')
            self.delay(2000)

            result = self.complete_task(task_type, task_title, task.get('_id'))

            if result.get('success'):
                reward = result.get('reward', 0)
                new_balance = result.get('newBalance', 0)
                logger.success(f'任务 "{task_title}" 完成！获得 +{reward} $AFD 代币')
                logger.info(f'新余额: {new_balance} $AFD')
            else:
                logger.warn(f'任务 "{task_title}": {result.get("message", "失败")}')

            self.delay(1000)

    def claim_gift_code(self, code):
        try:
            payload = {
                'userId': self.user_id,
                'code': code,
            }

            response = self.session.post(
                f'{API_BASE}/gift-codes/claim',
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            
            error_data = response.json() if response.text else {}
            return {
                'success': False,
                'message': error_data.get('message', '礼品码兑换失败')
            }
        except Exception as error:
            return {'success': False, 'message': str(error)}

    def claim_all_gift_codes(self):
        logger.loading('正在检查礼品码...')
        
        user_info = self.get_user_info()
        claimed_codes = []
        if user_info and user_info.get('success'):
            claimed_codes = user_info.get('data', {}).get('claimedGiftCodes', [])

        logger.info(f'找到 {len(GIFT_CODES)} 个可用礼品码')

        for code in GIFT_CODES:
            if code in claimed_codes:
                logger.info(f'礼品码 "{code}" 已兑换，跳过...')
                continue

            logger.loading(f'正在兑换礼品码: {code}')
            self.delay(2000)

            result = self.claim_gift_code(code)

            if result.get('success'):
                data = result.get('data', {})
                reward = data.get('reward', 0)
                claims_left = data.get('claimsLeft', 0)
                new_balance = data.get('newBalance', 0)
                logger.success(f'礼品码 "{code}" 兑换成功！获得 +{reward} $AFD 代币')
                logger.info(f'剩余兑换次数: {claims_left} | 新余额: {new_balance} $AFD')
            else:
                logger.warn(f'礼品码 "{code}": {result.get("message", "失败")}')

            self.delay(1000)

    def delay(self, ms):
        time.sleep(ms / 1000.0)


def load_proxies():
    """加载代理列表"""
    proxies = []
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
    except Exception as error:
        logger.warn(f'加载代理列表失败: {str(error)}')
    return proxies


def load_referral_codes():
    """加载邀请码列表"""
    codes = []
    try:
        if os.path.exists(RF_CODE_FILE):
            with open(RF_CODE_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        codes.append(line)
    except Exception as error:
        logger.warn(f'加载邀请码列表失败: {str(error)}')
    return codes


def load_accounts():
    try:
        # 确保 config 目录存在
        os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as error:
        logger.error(f'加载账户列表失败: {str(error)}')
    return []


def save_accounts(accounts):
    try:
        # 确保 config 目录存在
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(accounts, f, ensure_ascii=False, indent=2)
        return True
    except Exception as error:
        logger.error(f'保存账户列表失败: {str(error)}')
        return False


def main():
    show_copyright()
    time.sleep(5)

    # 确保 config 目录存在
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # 加载邀请码列表
    referral_codes = load_referral_codes()
    
    if not referral_codes:
        logger.error(f'未找到邀请码文件 {RF_CODE_FILE}，或文件中没有有效的邀请码！')
        logger.info('请先创建配置文件并添加邀请码。')
        return
    
    # 显示邀请码列表供用户选择
    logger.info(f'找到 {len(referral_codes)} 个邀请码：')
    for idx, code in enumerate(referral_codes, 1):
        print(f"  {Colors.CYAN}{idx}. {code}{Colors.RESET}")
    print('')

    # 如果只有一个邀请码，直接使用
    if len(referral_codes) == 1:
        referral_code = referral_codes[0]
        logger.info(f'只有一个邀请码，自动选择: {referral_code}')
    else:
        try:
            choice = input(f"{Colors.YELLOW}请选择要使用的邀请码（输入序号 1-{len(referral_codes)}，直接回车默认选择第1个）: {Colors.RESET}").strip()
            
            # 如果用户直接回车，默认选择第一个
            if not choice:
                choice_num = 1
                logger.info('未输入选择，默认使用第一个邀请码')
            else:
                choice_num = int(choice)
            
            if choice_num < 1 or choice_num > len(referral_codes):
                logger.error(f'无效的选择。请输入 1 到 {len(referral_codes)} 之间的数字。')
                return
            
            referral_code = referral_codes[choice_num - 1]
        except ValueError:
            logger.error('无效的选择。请输入有效的数字，或直接回车使用默认选项。')
            return
    
    logger.success(f'使用邀请码: {referral_code}')
    print('')

    # 加载代理列表
    proxies = load_proxies()
    proxy_index = 0
    
    if proxies:
        logger.info(f'已加载 {len(proxies)} 个代理，将循环使用')
    else:
        logger.warn('未找到代理，将不使用代理运行')
    print('')

    count = input(f"{Colors.YELLOW}请输入要注册的账户数量: {Colors.RESET}").strip()
    try:
        num_accounts = int(count)
    except ValueError:
        logger.error('无效的数字。请输入有效的数字。')
        return

    if num_accounts < 1:
        logger.error('无效的数字。请输入有效的数字。')
        return

    print('')
    logger.info(f'开始为 {num_accounts} 个账户进行注册和设置...')
    print('')

    accounts = load_accounts()
    success_count = 0

    for i in range(1, num_accounts + 1):
        print(f"{Colors.MAGENTA}{Colors.WHITE}---------------- 账户 {i}/{num_accounts} ----------------{Colors.RESET}")

        # 获取代理（循环使用）
        current_proxy = None
        if proxies:
            current_proxy = proxies[proxy_index % len(proxies)]
            # 隐藏代理中的敏感信息用于显示
            display_proxy = current_proxy
            if '@' in display_proxy:
                display_proxy = display_proxy.split('@')[-1]
            logger.info(f'使用代理 [{proxy_index % len(proxies) + 1}/{len(proxies)}]: {display_proxy}')
            proxy_index += 1

        logger.loading(f'正在注册账户 {i}...')
        temp_bot = AithereumBot(proxy=current_proxy)
        result = temp_bot.register_account(referral_code)

        if not result.get('success'):
            logger.error(f'账户 {i} 注册失败: {result.get("message", "未知错误")}')
            if result.get('details') or result.get('response'):
                logger.warn(f'详情: {result.get("details") or result.get("response")}')
            print('')
            temp_bot.delay(3000)
            continue

        logger.success(f'账户 {i} 注册成功！')
        logger.info(f'邮箱: {result.get("email")}')
        logger.info(f'姓名: {result.get("name")}')
        logger.info(f'用户ID: {result.get("userId")}')
        logger.info(f'您的推荐码: {result.get("referralCode")}')
        logger.info(f'使用的推荐码: {referral_code}')
        logger.info(f'余额: {result.get("afdTokens")} $AFD')
        print('')

        account_data = {
            'userId': result.get('userId'),
            'email': result.get('email'),
            'name': result.get('name'),
            'referralCode': result.get('referralCode'),
            'proxy': current_proxy if current_proxy else None,
            'registeredAt': datetime.now().isoformat()
        }
        accounts.append(account_data)
        save_accounts(accounts)

        logger.info(f'账户已保存到 {ACCOUNTS_FILE}')
        print('')

        # 自动执行日常任务
        logger.info('正在为该账户执行初始任务...')
        print('')

        # 创建机器人实例并执行任务
        bot = AithereumBot(result.get('userId'), result.get('email'), result.get('name'), proxy=current_proxy)

        try:
            # 1. 领取礼品码
            bot.claim_all_gift_codes()
            print('')

            # 2. 完成任务
            bot.complete_tasks()
            print('')

            # 3. 每日签到
            bot.daily_check_in()
            print('')

            # 获取最终余额
            final_info = bot.get_user_info()
            if final_info and final_info.get('success'):
                final_balance = final_info.get('data', {}).get('afdTokens', 0)
                initial_balance = result.get('afdTokens', 0)
                earned = final_balance - initial_balance
                logger.success(f'初始任务完成！最终余额: {final_balance} $AFD')
                if earned > 0:
                    logger.success(f'本次获得: +{earned} $AFD 代币')
        except Exception as error:
            logger.error(f'执行初始任务时发生错误: {str(error)}')

        success_count += 1
        print('')
        
        if i < num_accounts:
            logger.info('等待 5 秒后处理下一个账户...')
            temp_bot.delay(5000)
            print('')

    logger.success(f'完成！成功注册 {success_count}/{num_accounts} 个账户。')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warn('\n用户中断操作')
    except Exception as error:
        logger.error(f'机器人错误: {str(error)}')
        import traceback
        traceback.print_exc()

