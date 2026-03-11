"""
评价结果页面
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from sqlalchemy.orm import Session
import io

from models.database import SessionLocal
from services.result_service import EvaluationResultService
from services.sample_service import SampleService
from services.standard_service import StandardService


def show_results():
    """评价结果页面"""
    st.header("评价结果")

    db = SessionLocal()
    try:
        result_service = EvaluationResultService(db)
        sample_service = SampleService(db)
        standard_service = StandardService(db)

        tab1, tab2 = st.tabs(["结果列表", "结果详情"])

        with tab1:
            show_result_list(result_service)

        with tab2:
            show_result_detail(result_service, sample_service, standard_service)

    finally:
        db.close()


def show_result_list(result_service: EvaluationResultService):
    """结果列表展示"""
    st.subheader("历史评价记录")

    results = result_service.get_results(limit=100)

    if results:
        data = []
        for result in results:
            details = json.loads(result.evaluation_details) if result.evaluation_details else []
            total_indicators = len(details)
            exceed_count = sum(1 for d in details if d.get("result") == "超标")
            
            data.append({
                "ID": result.id,
                "样品编号": result.sample_no,
                "评价标准": result.standard_name,
                "总体结果": result.overall_result,
                "指标总数": total_indicators,
                "超标数": exceed_count,
                "评价时间": result.evaluated_at.strftime("%Y-%m-%d %H:%M")
            })

        df = pd.DataFrame(data)
        
        # 根据总体结果着色
        def color_overall(val):
            if val == "达标":
                return "background-color: #d4edda; color: #155724"
            else:
                return "background-color: #f8d7da; color: #721c24"
        
        styled_df = df.style.applymap(color_overall, subset=["总体结果"])
        
        st.dataframe(styled_df, use_container_width=True)

        # 导出按钮
        if st.button("导出为 Excel"):
            export_to_excel(df)

    else:
        st.info("暂无评价结果")


def show_result_detail(
    result_service: EvaluationResultService,
    sample_service: SampleService,
    standard_service: StandardService
):
    """结果详情查看"""
    st.subheader("查看详细评价结果")

    results = result_service.get_results(limit=100)
    
    if not results:
        st.info("暂无评价结果")
        return

    result_options = {
        f"{r.sample_no} - {r.standard_name} ({r.evaluated_at.strftime('%Y-%m-%d')})": r 
        for r in results
    }
    
    selected_str = st.selectbox(
        "选择要查看的评价记录",
        list(result_options.keys())
    )

    if selected_str:
        selected_result = result_options[selected_str]
        
        # 基本信息
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**样品编号**: {selected_result.sample_no}")
            st.markdown(f"**评价标准**: {selected_result.standard_name}")
            st.markdown(f"**评价时间**: {selected_result.evaluated_at.strftime('%Y-%m-%d %H:%M')}")
        
        with col2:
            if selected_result.overall_result == "达标":
                st.success(f"**总体评价**: {selected_result.overall_result}")
            else:
                st.error(f"**总体评价**: {selected_result.overall_result}")
            
            st.markdown(f"**评价结论**: {selected_result.conclusion or '-'}")

        # 详细评价数据
        st.subheader("各指标评价详情")
        
        details = json.loads(selected_result.evaluation_details) if selected_result.evaluation_details else []
        
        if details:
            data = []
            for detail in details:
                status_icon = "✅" if detail["result"] == "达标" else ("⚠️" if detail["result"] == "未检测" else "❌")
                
                data.append({
                    "状态": status_icon,
                    "指标名称": detail.get("indicator", ""),
                    "检测值": f"{detail.get('value', '未检测')} {detail.get('unit', '')}" if detail.get('value') is not None else "未检测",
                    "标准限值": format_limit(detail),
                    "评价结果": detail.get("result", ""),
                    "备注说明": detail.get("remark", "")
                })

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            # 下载详细报告
            if st.button("下载详细报告 (Excel)"):
                download_detailed_report(selected_result, details)


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


def export_to_excel(df: pd.DataFrame):
    """导出结果为 Excel"""
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='评价结果汇总')
        
        # 调整列宽
        worksheet = writer.sheets['评价结果汇总']
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + i)].width = column_width
    
    st.download_button(
        label="点击下载 Excel 文件",
        data=buffer.getvalue(),
        file_name=f"评价结果汇总_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def download_detailed_report(result, details: list):
    """下载详细报告"""
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # 工作表 1：详细信息
        data = []
        for detail in details:
            data.append({
                "指标名称": detail.get("indicator", ""),
                "检测值": detail.get('value'),
                "单位": detail.get('unit', ''),
                "下限值": detail.get('min_limit', ''),
                "上限值": detail.get('max_limit', ''),
                "评价结果": detail.get("result", ""),
                "备注": detail.get("remark", "")
            })
        
        df_details = pd.DataFrame(data)
        df_details.to_excel(writer, index=False, sheet_name='详细评价数据')
        
        # 工作表 2：基本信息
        df_info = pd.DataFrame({
            "项目": ["样品编号", "评价标准", "总体结果", "评价时间", "结论"],
            "内容": [
                result.sample_no,
                result.standard_name,
                result.overall_result,
                result.evaluated_at.strftime("%Y-%m-%d %H:%M"),
                result.conclusion or "-"
            ]
        })
        df_info.to_excel(writer, index=False, sheet_name='基本信息', startcol=3)
    
    st.download_button(
        label="点击下载详细报告",
        data=buffer.getvalue(),
        file_name=f"{result.sample_no}_评价报告_{result.evaluated_at.strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
