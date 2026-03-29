"""
数据评价页面
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.sample_service import SampleService
from services.standard_service import StandardService
from services.evaluation_engine import EvaluationEngine
from services.result_service import EvaluationResultService


def show_evaluation():
    """数据评价页面"""
    st.header("数据评价")

    db = SessionLocal()
    try:
        sample_service = SampleService(db)
        standard_service = StandardService(db)
        result_service = EvaluationResultService(db)

        # 选择样品
        st.subheader("1. 选择样品")
        samples = sample_service.get_samples(limit=100)
        
        if not samples:
            st.warning("暂无样品，请先添加或导入样品")
            return

        sample_options = {f"{s.sample_no} - {s.sample_name}": s for s in samples}
        selected_sample_str = st.selectbox(
            "选择要评价的样品",
            list(sample_options.keys())
        )
        
        if not selected_sample_str:
            return
            
        selected_sample = sample_options[selected_sample_str]

        # 显示样品信息
        with st.expander("样品信息预览"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**样品编号**: {selected_sample.sample_no}")
                st.markdown(f"**样品名称**: {selected_sample.sample_name}")
            
            with col2:
                st.markdown(f"**采样日期**: {selected_sample.collection_date.strftime('%Y-%m-%d') if selected_sample.collection_date else '-'}")
                st.markdown(f"**检测日期**: {selected_sample.detection_date.strftime('%Y-%m-%d') if selected_sample.detection_date else '-'}")

        # 选择评价标准
        st.subheader("2. 选择评价标准")
        standards = standard_service.get_standards(limit=100)
        
        if not standards:
            st.warning("暂无评价标准，请先添加标准")
            return

        standard_options = {f"{s.standard_name} ({s.standard_code or '无编号'})": s for s in standards}
        selected_standard_str = st.selectbox(
            "选择评价标准",
            list(standard_options.keys())
        )
        
        if not selected_standard_str:
            return
            
        selected_standard = standard_options[selected_standard_str]

        # 如果是土壤标准，显示用地类型选择
        land_use_type = ''
        agri_sub_type = ''
        ph_range = ''
        
        if '土壤' in selected_standard.standard_type:
            st.subheader("3. 土壤用地类型信息")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                land_use_type = st.selectbox(
                    "用地类型",
                    ['农用地', '建设用地第一类', '建设用地第二类'],
                    help="根据 GB 36600-2018 和 GB 15618-2018 选择"
                )
            
            with col2:
                if land_use_type == '农用地':
                    agri_sub_type = st.selectbox(
                        "农用地细分",
                        ['水田', '果园', '其他'],
                        help="GB 15618-2018 规定的农用地类型"
                    )
                else:
                    agri_sub_type = ''
                    st.selectbox("农用地细分", [''], disabled=True)
            
            with col3:
                if land_use_type == '农用地':
                    ph_range = st.selectbox(
                        "pH 分段",
                        ['<5.5', '5.5-6.5', '6.5-7.5', '>7.5'],
                        help="根据实际 pH 值选择对应范围"
                    )
                else:
                    ph_range = ''
                    st.selectbox("pH 分段", [''], disabled=True)

        # 显示标准信息
        with st.expander("标准限值预览"):
            limits = json.loads(selected_standard.limits) if selected_standard.limits else []
            st.markdown(f"**标准名称**: {selected_standard.standard_name}")
            st.markdown(f"**评价指标数量**: {len(limits)}")
            
            limit_df = pd.DataFrame([{
                "指标": l.get('indicator', ''),
                "规则": l.get('operator', ''),
                "限值": f"{l.get('min_limit', '')} ~ {l.get('max_limit', '')}",
                "单位": l.get('unit', '')
            } for l in limits])
            st.dataframe(limit_df, use_container_width=True)

        # 执行评价
        st.subheader("4. 执行评价")
        
        if st.button("开始评价", type="primary"):
            try:
                # 获取样品检测数据
                detection_data = json.loads(selected_sample.detection_data) if selected_sample.detection_data else {}
                
                if not detection_data:
                    st.error("该样品没有检测数据")
                    return

                # 使用评价引擎进行评价
                overall_result, details = EvaluationEngine.evaluate_sample(
                    detection_data,
                    limits,
                    land_use_type if '土壤' in selected_standard.standard_type else '',
                    agri_sub_type if '土壤' in selected_standard.standard_type else '',
                    ph_range if '土壤' in selected_standard.standard_type else ''
                )

                # 保存评价结果
                result_data = {
                    "sample_id": selected_sample.id,
                    "sample_no": selected_sample.sample_no,
                    "standard_id": selected_standard.id,
                    "standard_name": selected_standard.standard_name,
                    "evaluation_details": json.dumps(details, ensure_ascii=False),
                    "overall_result": overall_result,
                    "conclusion": f"根据{selected_standard.standard_name}评价，该样品{overall_result}"
                }
                
                result = result_service.create_result(result_data)

                # 显示评价结果
                st.success("评价完成！")
                show_evaluation_result(details, overall_result)

            except Exception as e:
                st.error(f"评价失败：{str(e)}")

    finally:
        db.close()


def show_evaluation_result(details: list, overall_result: str):
    """显示评价结果"""
    st.subheader("评价结果详情")

    # 总体评价
    if overall_result == "达标":
        st.success(f"✅ 总体评价：**{overall_result}**")
    else:
        st.error(f"❌ 总体评价：**{overall_result}**")

    # 各指标评价详情
    st.markdown("### 各指标评价情况")
    
    data = []
    for detail in details:
        status_icon = "✅" if detail["result"] == "达标" else ("⚠️" if detail["result"] == "未检测" else "❌")
        
        row_data = {
            "评价": status_icon,
            "指标名称": detail["indicator"],
            "检测值": f"{detail['value']} {detail.get('unit', '')}" if detail["value"] is not None else "未检测",
            "标准限值": format_limit(detail),
            "评价结果": detail["result"],
            "备注": detail.get("remark", "")
        }
        data.append(row_data)

    df = pd.DataFrame(data)
    
    # 根据结果着色
    def color_result(val):
        if val == "达标":
            return "background-color: #d4edda"
        elif val == "超标":
            return "background-color: #f8d7da"
        else:
            return ""
    
    styled_df = df.style.applymap(color_result, subset=["评价结果"])
    st.dataframe(styled_df, use_container_width=True)


def format_limit(detail: dict) -> str:
    """格式化限值显示"""
    min_limit = detail.get("min_limit")
    max_limit = detail.get("max_limit")
    
    if min_limit is not None and max_limit is not None:
        return f"{min_limit} ~ {max_limit}"
    elif max_limit is not None:
        return f"≤ {max_limit}"
    elif min_limit is not None:
        return f"≥ {min_limit}"
    else:
        return "-"
