from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_query_in_iframe(driver,cource_code="01010110"):
    """
    在iframe内部点击查询按钮
    
    Args:
        driver: WebDriver 实例
    
    Returns:
        bool: 成功点击返回True，否则返回False
    """
    try:
        print("🔍 在iframe内部点击查询按钮...")
        
        # 首先切换到iframe内部
        print("🔄 切换到iframe...")
        iframe = driver.find_element(By.ID, "iframename")
        driver.switch_to.frame(iframe)
        print("✅ 已切换到iframe内部")
        
        # 保存iframe内部页面（查询前）
        with open("iframe_before_query.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ iframe查询前页面已保存到 iframe_before_query.html")
        print(f"📝 填写课程代码: {cource_code}")
        driver.find_element(By.NAME, "pageKcmc").clear()
        driver.find_element(By.NAME, "pageKcmc").send_keys(cource_code)
        print("✅ 课程代码填写完成")
        # 根据页面结构，查询按钮的ID是 "a_anniu" 或者包含在 "chaxun_an" 元素中
        query_button = None
        
        # 方法1: 通过ID查找
        try:
            query_button = driver.find_element(By.ID, "a_anniu")
            print("✅ 通过ID找到查询按钮: a_anniu")
        except:
            pass
        
        # 方法2: 通过文本查找
        if not query_button:
            try:
                query_button = driver.find_element(By.XPATH, "//a[contains(text(), '查询')]")
                print("✅ 通过文本找到查询按钮")
            except:
                pass
        
        # 方法3: 通过onclick属性查找
        if not query_button:
            try:
                query_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'queryLike')]")
                print("✅ 通过onclick属性找到查询按钮")
            except:
                pass
        
        if not query_button:
            print("❌ 未找到查询按钮")
            # 显示所有可点击元素
            print("🔍 所有链接和按钮:")
            links = driver.find_elements(By.TAG_NAME, "a")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            inputs = driver.find_elements(By.XPATH, "//input[@type='button' or @type='submit']")
            
            for element in links + buttons + inputs:
                text = element.text.strip() or element.get_attribute('value') or element.get_attribute('innerText')
                if text:
                    print(f"   - '{text}'")
            
            driver.switch_to.default_content()
            return False
        
        # 点击查询按钮
        print(f"🖱️ 点击查询按钮: {query_button.text}")
        driver.execute_script("arguments[0].click();", query_button)
        
        # 等待查询结果
        print("⏳ 等待查询结果...")
        time.sleep(3)
        
        # 保存查询后的iframe页面
        with open("iframe_after_query.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ iframe查询后页面已保存到 iframe_after_query.html")
        
        # 检查是否有查询结果
        page_source = driver.page_source
        if "不在学生选课时间范围内" in page_source:
            print("⚠️ 系统提示: 不在学生选课时间范围内")
            print("📅 选课时间: 2025-09-05 12:30 至 2025-09-08 17:00")
        elif "课程代码" in page_source and "课程名称" in page_source:
            print("✅ 查询成功，显示课程列表")
        else:
            print("⚠️ 查询完成，但无法确定结果")
        
        # 切换回主文档
        driver.switch_to.default_content()
        
        # 保存主页面
        with open("main_after_query.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ 主页面已保存到 main_after_query.html")
        
        return True
        
    except Exception as e:
        print(f"❌ 点击查询按钮失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 确保切换回主文档
        try:
            driver.switch_to.default_content()
        except:
            pass
        
        return False

def fill_query_form(driver, xnxq="2025-20261", kkxiaoqu="", kkyx=""):
    """
    填写查询表单
    
    Args:
        driver: WebDriver 实例
        xnxq (str): 学年学期，默认 "2025-20261" (2025秋季)
        kkxiaoqu (str): 开课校区，如 "1" (一校区)
        kkyx (str): 开课院系代码
    """
    try:
        print("📝 填写查询表单...")
        
        # 切换到iframe内部
        iframe = driver.find_element(By.ID, "iframename")
        driver.switch_to.frame(iframe)
        
        # 选择学年学期
        if xnxq:
            xnxq_select = driver.find_element(By.ID, "pageXnxq")
            driver.execute_script(f"arguments[0].value = '{xnxq}';", xnxq_select)
            print(f"✅ 设置学年学期: {xnxq}")
        
        # 选择开课校区
        if kkxiaoqu:
            kkxiaoqu_select = driver.find_element(By.NAME, "pageKkxiaoqu")
            driver.execute_script(f"arguments[0].value = '{kkxiaoqu}';", kkxiaoqu_select)
            print(f"✅ 设置开课校区: {kkxiaoqu}")
        
        # 选择开课院系
        if kkyx:
            kkyx_select = driver.find_element(By.NAME, "pageKkyx")
            driver.execute_script(f"arguments[0].value = '{kkyx}';", kkyx_select)
            print(f"✅ 设置开课院系: {kkyx}")
        
        # 保存填写后的表单
        with open("iframe_filled_form.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✅ 填写后的表单已保存到 iframe_filled_form.html")
        
        # 切换回主文档
        driver.switch_to.default_content()
        
        return True
        
    except Exception as e:
        print(f"❌ 填写表单失败: {e}")
        try:
            driver.switch_to.default_content()
        except:
            pass
        return False

def analyze_course_list(driver):
    """
    分析课程列表
    """
    try:
        print("\n📊 分析课程列表...")
        
        # 切换到iframe内部
        iframe = driver.find_element(By.ID, "iframename")
        driver.switch_to.frame(iframe)
        
        page_source = driver.page_source
        
        # 检查是否有课程表格
        if "课程代码" in page_source and "课程名称" in page_source:
            print("✅ 检测到课程列表表格")
            
            # 查找课程行
            course_rows = driver.find_elements(By.XPATH, "//table[@class='bot_line']//tr[position()>1]")
            print(f"📋 找到 {len(course_rows)} 个课程行")
            
            if course_rows:
                # 显示前几个课程
                for i, row in enumerate(course_rows[:5]):
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        course_code = cells[2].text if len(cells) > 2 else "N/A"
                        course_name = cells[3].text if len(cells) > 3 else "N/A"
                        print(f"   {i+1}. {course_code} - {course_name}")
            
            # 检查是否有"没有数据"的提示
            if "没有数据" in page_source or "暂无数据" in page_source:
                print("📭 课程列表为空")
        else:
            print("📭 未找到课程列表")
        
        # 检查选课时间提示
        if "不在学生选课时间范围内" in page_source:
            print("⏰ 系统提示: 不在学生选课时间范围内")
            # 提取选课时间信息
            import re
            time_match = re.search(r'选课时间：(.+?)&nbsp;至&nbsp;(.+?)<', page_source)
            if time_match:
                start_time = time_match.group(1)
                end_time = time_match.group(2)
                print(f"📅 选课时间: {start_time} 至 {end_time}")
        
        # 切换回主文档
        driver.switch_to.default_content()
        
    except Exception as e:
        print(f"❌ 分析课程列表失败: {e}")
        try:
            driver.switch_to.default_content()
        except:
            pass

# 使用示例
if __name__ == "__main__":
    from login import base_login
    from course_selection import click_student_course_selection
    
    driver = base_login(keep_driver=True)      
    
    if driver:
        try:
            # 点击专业限选及专业选修
            success = click_student_course_selection(driver, selection_type="专业限选及专业选修")
            
            if success:
                # 保存点击后的页面
                with open("after_click.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("✅ 点击后页面已保存到 after_click.html")
                
                # 分析课程列表
                analyze_course_list(driver)
                
                # 填写查询表单（可选）
                fill_query_form(driver, xnxq="2025-20261", kkxiaoqu="1")
                
                # 点击查询按钮
                query_success = click_query_in_iframe(driver)
                
                if query_success:
                    print("✅ 查询操作完成!")
                else:
                    print("❌ 查询操作失败")
            else:
                print("❌ 进入选课页面失败")
                
        finally:
            input("\n按回车键关闭浏览器...")
            driver.quit()