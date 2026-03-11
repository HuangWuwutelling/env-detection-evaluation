"""
环境检测数据评价系统 - 主入口
"""
import streamlit as st

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
    st.header("样品管理")

    tab1, tab2 = st.tabs(["样品列表", "批量导入"])

    with tab1:
        st.subheader("样品列表")
        st.info("功能开发中：样品列表展示和手动录入")

    with tab2:
        st.subheader("批量导入")
        st.info("功能开发中：支持Excel/CSV文件批量导入")


def show_standard_management():
    """评价标准管理页面"""
    st.header("评价标准管理")

    tab1, tab2 = st.tabs(["标准列表", "添加标准"])

    with tab1:
        st.subheader("评价标准列表")
        st.info("功能开发中：标准列表展示")

    with tab2:
        st.subheader("添加新标准")
        st.info("功能开发中：标准配置表单")


def show_evaluation():
    """数据评价页面"""
    st.header("数据评价")

    st.info("功能开发中：选择样品和标准进行评价")


def show_results():
    """评价结果页面"""
    st.header("评价结果")

    st.info("功能开发中：评价结果展示和导出")


if __name__ == "__main__":
    main()
