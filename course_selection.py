from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_student_course_selection(driver, selection_type="必修"):
    """
    点击学生选课相关功能
    
    Args:
        driver: WebDriver 实例
        selection_type (str): 选课类型，可选值：
            - "必修" (默认)
            - "专业限选及专业选修"
            - "英语"
            - "体育"
            - "全校任选"
            - 等等...
    """
    try:
        print(f"🎯 尝试点击学生选课: {selection_type}")
        
        # 等待页面加载完成
        wait = WebDriverWait(driver, 0.1)
        
        # 方法1: 直接通过文本查找链接
        print("📋 方法1: 直接查找链接...")
        selection_xpaths = [
            f"//a[contains(text(), '{selection_type}')]",
            f"//a[text()='{selection_type}']",
            f"//*[contains(text(), '{selection_type}')]"
        ]
        
        selection_link = None
        for xpath in selection_xpaths:
            try:
                selection_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                print(f"✅ 使用XPath找到元素: {xpath}")
                break
            except:
                continue
        
        if not selection_link:
            # 方法2: 先找到学生选课区域，再找具体选项
            print("📋 方法2: 在学生选课区域内查找...")
            try:
                # 找到包含"学生选课"标题的span
                xk_span_xpath = "//span[p[@class='navi_title' and contains(text(), '学生选课')]]"
                xk_span = wait.until(EC.presence_of_element_located((By.XPATH, xk_span_xpath)))
                print("✅ 找到学生选课区域")
                
                # 在该区域内查找具体选项
                selection_link = xk_span.find_element(By.XPATH, f".//a[contains(text(), '{selection_type}')]")
            except Exception as e:
                print(f"❌ 方法2失败: {e}")
        
        if not selection_link:
            # 方法3: 查找所有链接并匹配文本
            print("📋 方法3: 查找所有链接...")
            all_links = driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                if selection_type in link.text:
                    selection_link = link
                    print(f"✅ 通过文本匹配找到链接: {link.text}")
                    break
        
        if not selection_link:
            print(f"❌ 未找到文本为 '{selection_type}' 的链接")
            # 显示所有可用的链接文本
            print("🔍 当前页面所有链接文本:")
            all_links = driver.find_elements(By.TAG_NAME, "a")
            unique_texts = set()
            for link in all_links:
                text = link.text.strip()
                if text and len(text) < 50:  # 过滤掉过长的文本
                    unique_texts.add(text)
            
            for text in sorted(unique_texts):
                print(f"   - '{text}'")
            return False
        
        # 点击链接
        print(f"🖱️ 点击: {selection_type}")
        # 使用JavaScript点击，避免元素被遮挡等问题
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selection_link)
        time.sleep(0.1)
        driver.execute_script("arguments[0].click();", selection_link)
        
        # 等待页面加载
        print("⏳ 等待页面加载...")
        time.sleep(0.1)
        
        # 检查是否成功跳转或iframe加载
        current_url = driver.current_url
        print(f"📍 当前URL: {current_url}")
        
        # 检查iframe内容
        try:
            iframe = driver.find_element(By.ID, "iframename")
            iframe_src = iframe.get_attribute("src")
            print(f"🖼️ iframe src: {iframe_src}")
            
            if iframe_src and iframe_src != "about:blank":
                print("✅ iframe内容已更新")
                return True
        except Exception as e:
            print(f"⚠️ 检查iframe时出错: {e}")
        
        # 如果URL变化也算成功
        if "xsxk" in current_url or "select" in current_url.lower():
            print(f"✅ 成功进入选课相关页面")
            return True
        else:
            print("⚠️ URL未明显变化，但可能页面内容已更新")
            return True
            
    except Exception as e:
        print(f"❌ 点击学生选课失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_all_course_selection_options(driver):
    """
    获取学生选课菜单下的所有可选选项
    """
    try:
        print("🔍 获取学生选课所有选项...")
        
        wait = WebDriverWait(driver, 10)
        
        # 找到学生选课区域
        xk_span_xpath = "//span[p[@class='navi_title' and contains(text(), '学生选课')]]"
        xk_span = wait.until(EC.presence_of_element_located((By.XPATH, xk_span_xpath)))
        
        # 获取该区域内的所有链接
        links = xk_span.find_elements(By.TAG_NAME, "a")
        
        options = []
        for link in links:
            text = link.text.strip()
            if text:
                options.append(text)
        
        print("📋 学生选课选项:")
        for option in sorted(options):
            print(f"   - {option}")
        
        return options
        
    except Exception as e:
        print(f"❌ 获取选课选项失败: {e}")
        
        # 备用方法：获取页面所有链接
        print("🔍 备用方法：获取页面所有链接...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        unique_texts = set()
        for link in all_links:
            text = link.text.strip()
            if text and len(text) < 50:
                unique_texts.add(text)
        
        print("📋 页面所有链接:")
        for text in sorted(unique_texts):
            print(f"   - '{text}'")
        
        return list(unique_texts)

# 简化版本 - 直接点击
def simple_click_student_course(driver, selection_type="必修"):
    """
    简化版本：直接点击学生选课
    """
    try:
        print(f"🎯 简化版本：点击 {selection_type}")
        
        # 使用更简单的定位方式
        xpath = f"//a[contains(text(), '{selection_type}')]"
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        
        print(f"✅ 找到链接: {link.text}")
        driver.execute_script("arguments[0].click();", link)
        time.sleep(3)
        
        print("✅ 点击完成")
        return True
        
    except Exception as e:
        print(f"❌ 简化版本失败: {e}")
        return False

# 使用示例
if __name__ == "__main__":
    from login import base_login
    
    print("=" * 60)
    print("HIT 教务系统 - 学生选课操作")
    print("=" * 60)
    
    # 登录并保持浏览器打开
    driver = base_login(keep_driver=True)
    
    if driver:
        try:
            # 先保存当前页面
            with open("before_click.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("✅ 点击前页面已保存到 before_click.html")
            
            # 获取所有选项
            options = get_all_course_selection_options(driver)
            
            # 尝试点击
            selection_type = "必修"
            
            # 先尝试简化版本
            print(f"\n🎯 尝试简化版本点击: {selection_type}")
            if simple_click_student_course(driver, selection_type):
                print("✅ 简化版本成功!")
            else:
                print("🔄 简化版本失败，尝试完整版本...")
                if click_student_course_selection(driver, selection_type):
                    print("✅ 完整版本成功!")
                else:
                    print("❌ 所有方法都失败")
            
            # 保存点击后的页面
            with open("after_click.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("✅ 点击后页面已保存到 after_click.html")
            
        finally:
            input("\n按回车键关闭浏览器...")
            driver.quit()