from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import time
from dotenv import load_dotenv

# load_dotenv()

# USERNAME = os.getenv("JW_USERNAME", "")
# PASSWORD = os.getenv("JW_PASSWORD", "")
# BASE_URL = "http://jwts.hit.edu.cn"
# LOGIN_URL = f"{BASE_URL}/loginCAS"


def base_login(close_way="hand", keep_driver=False):
    """
    简单的登录函数
    
    Args:
        close_way (str): "hand" 时在登录后等待用户输入后关闭；若为其他值则自动关闭。
        keep_driver (bool): True 时登录成功后返回 driver 对象而不关闭浏览器，允许后续操作；
                          False 时按 close_way 决定是否关闭（默认）。
    
    Returns:
        driver or bool: 若 keep_driver=True 且登录成功，返回 WebDriver 实例；
                       否则返回 True（成功）或 False（失败）。
    """
    load_dotenv()
    USERNAME = os.getenv("JW_USERNAME", "")
    PASSWORD = os.getenv("JW_PASSWORD", "")
    BASE_URL = "http://jwts.hit.edu.cn"
    LOGIN_URL = f"{BASE_URL}/loginCAS"
    # 检查凭证
    if not USERNAME or not PASSWORD:
        print("❌ 错误：未设置 JW_USERNAME 或 JW_PASSWORD")
        return False
    
    # 启动浏览器
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 打开登录页面
        driver.get(LOGIN_URL)
        print("✓ 打开登录页面")
        print(f"  当前URL: {driver.current_url}")
        
        # 等待表单完全加载
        wait = WebDriverWait(driver, 0.1)
        wait.until(EC.presence_of_element_located((By.ID, "pwdFromId")))
        print("✓ 登录表单已加载")
        time.sleep(1.5)  # 等待加密脚本加载
        
        # 输入用户名
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys(USERNAME)
        print("✓ 输入用户名")
        
        # 输入密码
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        print("✓ 输入密码")
        
        # 等待加密完成
        time.sleep(0.1)
        
        # 通过JavaScript提交表单（会触发加密和验证逻辑）
        print("✓ 提交登录表单")
        driver.execute_script("""
            // 触发密码加密
            var password = document.getElementById('password').value;
            var salt = document.getElementById('pwdEncryptSalt').value;
            if (typeof encryptPassword === 'function') {
                var encryptedPassword = encryptPassword(password, salt);
                document.getElementById('saltPassword').value = encryptedPassword;
            }
            // 提交表单
            document.getElementById('pwdFromId').submit();
        """)
        
        # 等待重定向
        print("⏳ 等待页面加载...")
        time.sleep(0.1)
        
        current_url = driver.current_url
        print(f"✓ 当前URL: {current_url}")
        
        # 如果在 CAS 或登录页面，继续等待
        if "ids.hit.edu.cn" in current_url or "loginCAS" in current_url:
            print("⏳ 正在进行认证，继续等待...")
            time.sleep(0.1)
            current_url = driver.current_url
            print(f"✓ 重定向后URL: {current_url}")
        with open("base_login_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("  页面源码已保存到 base_login_debug.html")
        # 检查最终结果
        if "jwts.hit.edu.cn" in current_url:
            print("✅ 登录成功！")
            if keep_driver:
                print("✓ 浏览器保持打开，返回 driver 实例以供后续操作。")
                return driver
            if close_way == "hand":
                input("按回车关闭浏览器...")
            driver.quit()
            return True
        elif "ids.hit.edu.cn" in current_url and "login" in current_url:
            print("❌ 登录失败：仍在CAS登录页面")
            print("  可能原因：")
            print("  1. 用户名或密码错误")
            print("  2. 账号被冻结（并行会话数过多）")
            print("  3. 账号被锁定（登录失败次数过多）")
            # 保存页面源码用于调试
            with open("base_login_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("  页面源码已保存到 base_login_debug.html")
            input("按回车关闭浏览器...")
            driver.quit()
            return False
        else:
            print("⚠️  无法确定登录状态")
            print(f"  最终URL: {current_url}")
            input("按回车关闭浏览器...")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        input("按回车关闭浏览器...")
        driver.quit()
        return False
    finally:
        # 若 keep_driver=True 且已返回 driver，不会执行到这里
        # 若其他情况，driver 应已在 return 路径中关闭
        pass

if __name__ == "__main__":
    print("=" * 50)
    print("HIT 教务系统登录")
    print("=" * 50)
    base_login()
