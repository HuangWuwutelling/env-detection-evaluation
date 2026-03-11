"""
评价标准管理页面
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.standard_service import StandardService


def show_standard_management():
    """评价标准管理页面"""
    st.header("评价标准管理")

    tab1, tab2 = st.tabs(["标准列表", "添加标准"])

    with tab1:
        show_standard_list()

    with tab2:
        show_add_standard_form()


def show_standard_list():
    """标准列表展示"""
    st.subheader("评价标准列表")

    db = SessionLocal()
    try:
        service = StandardService(db)
        standards = service.get_standards(limit=100)

        if standards:
            # 转换为 DataFrame 展示
            data = []
            for standard in standards:
                limits = json.loads(standard.limits) if standard.limits else []
                indicators = ", ".join([l.get('indicator', '') for l in limits])
                
                data.append({
                    "ID": standard.id,
                    "标准名称": standard.standard_name,
                    "标准编号": standard.standard_code or "-",
                    "标准类型": standard.standard_type or "-",
                    "指标数量": len(limits),
                    "主要指标": indicators,
                    "更新时间": standard.updated_at.strftime("%Y-%m-%d") if standard.updated_at else "-"
                })

            df = pd.DataFrame(data)
            
            selected_row = st.dataframe(
                df,
                use_container_width=True,
                selection_mode="single",
                key="standard_list"
            )

            # 操作按钮
            col1, col2 = st.columns(2)
            with col1:
                if st.button("查看详情", key="view_standard"):
                    if selected_row and len(selected_row["selection"]["rows"]) > 0:
                        row_idx = selected_row["selection"]["rows"][0]
                        standard = standards[row_idx]
                        show_standard_detail(standard)
            
            with col2:
                if st.button("删除标准", key="delete_standard"):
                    if selected_row and len(selected_row["selection"]["rows"]) > 0:
                        row_idx = selected_row["selection"]["rows"][0]
                        standard = standards[row_idx]
                        if service.delete_standard(standard.id):
                            st.success(f"标准 {standard.standard_name} 已删除")
                            st.rerun()
                        else:
                            st.error("删除失败")
        else:
            st.info("暂无评价标准，请添加标准")

    finally:
        db.close()


def show_standard_detail(standard):
    """显示标准详情"""
    st.subheader(f"标准详情 - {standard.standard_name}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**标准名称**: {standard.standard_name}")
        st.markdown(f"**标准编号**: {standard.standard_code or '-'}")
        st.markdown(f"**标准类型**: {standard.standard_type or '-'}")
    
    with col2:
        st.markdown(f"**描述**: {standard.description or '-'}")
        st.markdown(f"**创建时间**: {standard.created_at.strftime('%Y-%m-%d') if standard.created_at else '-'}")

    # 显示限值配置
    if standard.limits:
        limits = json.loads(standard.limits)
        st.subheader("评价指标限值")
        
        data = []
        for limit in limits:
            data.append({
                "指标名称": limit.get('indicator', ''),
                "操作符": limit.get('operator', '<='),
                "下限值": limit.get('min_limit', '-'),
                "上限值": limit.get('max_limit', '-'),
                "单位": limit.get('unit', '')
            })
        
        st.dataframe(pd.DataFrame(data), use_container_width=True)


def show_add_standard_form():
    """添加标准表单"""
    st.subheader("添加新标准")

    db = SessionLocal()
    try:
        service = StandardService(db)

        with st.form("add_standard_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                standard_name = st.text_input("标准名称 *", placeholder="例如：地表水环境质量标准")
                standard_code = st.text_input("标准编号", placeholder="例如：GB 3838-2002")
                standard_type = st.selectbox(
                    "标准类型",
                    ["地表水", "废水", "大气", "土壤", "噪声", "其他"],
                    help="选择标准适用的环境介质类型"
                )
            
            with col2:
                description = st.text_area("标准描述", placeholder="简要描述该标准的适用范围")

            # 评价指标配置
            st.subheader("评价指标限值配置")
            
            # 使用动态方式添加多个指标
            if "indicators_count" not in st.session_state:
                st.session_state.indicators_count = 1

            num_indicators = st.number_input(
                "指标数量",
                min_value=1,
                max_value=50,
                value=st.session_state.indicators_count,
                key="num_indicators_input"
            )
            
            if num_indicators != st.session_state.indicators_count:
                st.session_state.indicators_count = num_indicators
                st.rerun()

            limits = []
            for i in range(num_indicators):
                st.markdown(f"**指标{i+1}**")
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                
                with col_a:
                    indicator_name = st.text_input(
                        "指标名称",
                        key=f"indicator_{i}_name",
                        placeholder="如 pH"
                    )
                
                with col_b:
                    operator = st.selectbox(
                        "判定规则",
                        ["<=", ">=", "between"],
                        key=f"indicator_{i}_op",
                        format_func=lambda x: {"<=": "≤限值", ">=": "≥限值", "between": "区间内"}[x]
                    )
                
                with col_c:
                    min_limit = st.number_input(
                        "下限值",
                        value=None,
                        key=f"indicator_{i}_min",
                        disabled=(operator == "<=")
                    )
                
                with col_d:
                    max_limit = st.number_input(
                        "上限值",
                        value=None,
                        key=f"indicator_{i}_max",
                        disabled=(operator == ">=")
                    )
                
                with col_e:
                    unit = st.text_input(
                        "单位",
                        key=f"indicator_{i}_unit",
                        placeholder="如 mg/L"
                    )
                
                if indicator_name:
                    limit_config = {
                        "indicator": indicator_name,
                        "operator": operator,
                        "unit": unit
                    }
                    
                    if operator == "<=":
                        limit_config["max_limit"] = max_limit
                    elif operator == ">=":
                        limit_config["min_limit"] = min_limit
                    else:  # between
                        limit_config["min_limit"] = min_limit
                        limit_config["max_limit"] = max_limit
                    
                    limits.append(limit_config)

            submitted = st.form_submit_button("提交标准")
            
            if submitted:
                if not standard_name:
                    st.error("标准名称为必填项")
                elif not limits:
                    st.error("至少需要配置一个评价指标")
                else:
                    try:
                        standard_data = {
                            "standard_name": standard_name,
                            "standard_code": standard_code,
                            "standard_type": standard_type,
                            "limits": json.dumps(limits, ensure_ascii=False),
                            "description": description
                        }
                        
                        service.create_standard(standard_data)
                        st.success(f"标准 {standard_name} 添加成功！")
                        
                        # 重置状态
                        st.session_state.indicators_count = 1
                        
                    except Exception as e:
                        st.error(f"添加失败：{str(e)}")

    finally:
        db.close()
