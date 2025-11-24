from login import base_login
from course_selection import click_student_course_selection
from query_iframe import click_query_in_iframe
if __name__ == "__main__":
    driver = base_login(keep_driver=True)      
    if driver:
        try:
            success = click_student_course_selection(driver, selection_type="专业限选及专业选修")
            print("success:", success)
            if success:
                query_success = click_query_in_iframe(driver,cource_code="22CS32000") 
                if query_success:
                    print("✅ 查询操作完成!")
                else:
                    print("❌ 查询操作失败")
            else:
                print("❌ 进入选课页面失败")
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
