import requests
import json
import os
import random
import time
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
    {Style.RESET_ALL}"""
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

GIFT_CODES = [
    'TGEENDOFDEC',
    'CEXENDOFDEC',
    'DEC31UTC',
    'CMCSOON',
    'AFDSECXR'
]


class AithereumBot:
    def __init__(self, user_id, email=None, name=None, proxy=None):
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


def load_accounts():
    """加载账户列表"""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as error:
        logger.error(f'加载账户列表失败: {str(error)}')
    return []


def main():
    show_copyright()
    time.sleep(5)

    # 确保 config 目录存在
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # 加载账户列表
    accounts = load_accounts()
    
    if not accounts:
        logger.error(f'未找到账户文件 {ACCOUNTS_FILE}，或文件中没有账户！')
        logger.info('请先使用 bot.py 注册账户。')
        return
    
    logger.info(f'找到 {len(accounts)} 个账户，开始执行日常任务...')
    print('')

    success_count = 0
    fail_count = 0

    for idx, account in enumerate(accounts, 1):
        user_id = account.get('userId')
        email = account.get('email', 'N/A')
        name = account.get('name', 'N/A')
        proxy = account.get('proxy')
        
        print(f"{Colors.MAGENTA}{Colors.WHITE}---------------- 账户 {idx}/{len(accounts)} ----------------{Colors.RESET}")
        logger.info(f'邮箱: {email}')
        logger.info(f'姓名: {name}')
        
        if proxy:
            display_proxy = proxy
            if '@' in display_proxy:
                display_proxy = display_proxy.split('@')[-1]
            logger.info(f'使用代理: {display_proxy}')
        
        print('')

        # 创建机器人实例
        bot = AithereumBot(user_id, email, name, proxy=proxy)

        # 检查账户是否有效
        user_info = bot.get_user_info()
        if not user_info or not user_info.get('success'):
            logger.error(f'账户无效或无法获取信息，跳过...')
            fail_count += 1
            print('')
            continue

        initial_balance = user_info.get('data', {}).get('afdTokens', 0)
        logger.info(f'当前余额: {initial_balance} $AFD')
        print('')

        # 执行所有任务
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
                earned = final_balance - initial_balance
                logger.success(f'任务完成！最终余额: {final_balance} $AFD')
                if earned > 0:
                    logger.success(f'本次获得: +{earned} $AFD 代币')
                elif earned < 0:
                    logger.warn(f'余额变化: {earned} $AFD 代币')

            success_count += 1
        except Exception as error:
            logger.error(f'执行任务时发生错误: {str(error)}')
            fail_count += 1

        print('')
        
        # 如果不是最后一个账户，等待一段时间
        if idx < len(accounts):
            logger.info('等待 3 秒后处理下一个账户...')
            bot.delay(3000)
            print('')

    # 输出总结
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("-----------------------------------------")
    print(f" 任务完成统计")
    print("-----------------------------------------")
    print(f"{Colors.RESET}")
    logger.success(f'成功: {success_count} 个账户')
    if fail_count > 0:
        logger.warn(f'失败: {fail_count} 个账户')
    logger.info(f'总计: {len(accounts)} 个账户')
    print('')
    
    return True


def countdown_timer(hours=24):
    """倒计时函数，显示剩余时间"""
    total_seconds = hours * 3600
    
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print(f" 所有任务已完成！将在 {hours} 小时后自动重新执行")
    print("=" * 60)
    print(f"{Colors.RESET}")
    print(f"{Colors.YELLOW}提示：按 Ctrl+C 可以退出程序{Colors.RESET}")
    print('')
    
    try:
        while total_seconds > 0:
            hours_left = total_seconds // 3600
            minutes_left = (total_seconds % 3600) // 60
            seconds_left = total_seconds % 60
            
            # 实时更新显示
            countdown_str = f"{Colors.CYAN}[倒计时] 距离下次执行还有: {int(hours_left):02d}小时 {int(minutes_left):02d}分钟 {int(seconds_left):02d}秒{Colors.RESET}"
            print(f"\r{countdown_str}", end='', flush=True)
            
            time.sleep(1)
            total_seconds -= 1
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}用户中断，程序退出{Colors.RESET}")
        raise
    
    print(f"\n\n{Colors.GREEN}倒计时结束，准备开始下一轮任务...{Colors.RESET}\n")


if __name__ == '__main__':
    try:
        # 持续循环运行
        while True:
            try:
                # 执行一次完整的任务
                main()
                
                # 等待24小时后再次执行
                countdown_timer(24)
                
            except KeyboardInterrupt:
                logger.warn('\n\n用户中断操作，程序退出')
                break
            except Exception as error:
                logger.error(f'任务执行错误: {str(error)}')
                import traceback
                traceback.print_exc()
                logger.info('等待 10 秒后重试...')
                time.sleep(10)
                
    except KeyboardInterrupt:
        logger.warn('\n程序已退出')
    except Exception as error:
        logger.error(f'程序错误: {str(error)}')
        import traceback
        traceback.print_exc()

