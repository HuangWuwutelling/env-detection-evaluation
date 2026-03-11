"""
环境检测数据评价系统 - 主入口
"""
import streamlit as st
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 初始化数据库
from models.database import init_db
init_db()

# 页面配置
st.set_page_config(
    page_title="环境检测数据评价系统",
    page_icon="🔬",
    layout="wide"
)


def main():
    """主函数"""
    st.title("🔬 环境检测数据评价系统")

    # 侧边栏导航
    st.sidebar.title("导航菜单")
    page = st.sidebar.radio(
        "选择功能模块",
        ["首页", "样品管理", "评价标准", "数据评价", "评价结果"]
    )

    # 根据选择显示不同页面
    if page == "首页":
        show_homepage()
    elif page == "样品管理":
        show_sample_management()
    elif page == "评价标准":
        show_standard_management()
    elif page == "数据评价":
        show_evaluation()
    elif page == "评价结果":
        show_results()


def show_homepage():
    """首页"""
    st.header("欢迎使用环境检测数据评价系统")

    st.markdown("""
    ### 系统功能
    
    - **样品管理**: 录入和管理检测样品信息，支持批量导入
    - **评价标准**: 配置检测指标和评价标准
    - **数据评价**: 根据标准对检测数据进行自动评价
    - **评价结果**: 查看和管理评价结果
    
    ### 使用流程
    
    1. 先在「评价标准」中配置评价标准
    2. 在「样品管理」中录入或导入检测数据
    3. 在「数据评价」中选择样品和标准进行评价
    4. 在「评价结果」中查看和导出评价结果
    """)


def show_sample_management():
    """样品管理页面"""
    from pages.sample_management import show_sample_management as show_sm
    show_sm()


def show_standard_management():
    """评价标准管理页面"""
    from pages.standard_management import show_standard_management as show_ssm
    show_ssm()


def show_evaluation():
    """数据评价页面"""
    from pages.evaluation import show_evaluation as show_eval
    show_eval()


def show_results():
    """评价结果页面"""
    from pages.results import show_results as show_res
    show_res()


if __name__ == "__main__":
    main()
