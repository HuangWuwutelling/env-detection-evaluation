"""
样品管理页面
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import SessionLocal
from services.sample_service import SampleService
from utils.file_import import (
    read_excel_file, 
    read_csv_file, 
    parse_sample_data,
    validate_samples_data
)
from utils.template_generator import create_template_excel


def show_sample_management():
    """样品管理页面"""
    st.header("样品管理")

    tab1, tab2 = st.tabs(["样品列表", "批量导入"])

    with tab1:
        show_sample_list()

    with tab2:
        show_batch_import()


def show_sample_list():
    """样品列表展示"""
    st.subheader("样品列表")

    db = SessionLocal()
    try:
        service = SampleService(db)
        
        # 搜索框
        search_keyword = st.text_input("搜索", placeholder="输入样品编号或名称")
        
        if search_keyword:
            samples = service.search_samples(search_keyword)
        else:
            samples = service.get_samples(limit=100)

        if samples:
            # 转换为 DataFrame 展示
            data = []
            for sample in samples:
                detection_data = json.loads(sample.detection_data) if sample.detection_data else {}
                indicators = ", ".join(detection_data.keys())
                
                data.append({
                    "ID": sample.id,
                    "样品编号": sample.sample_no,
                    "样品名称": sample.sample_name,
                    "样品类型": sample.sample_type or "-",
                    "检测指标": indicators,
                    "检测日期": sample.detection_date.strftime("%Y-%m-%d") if sample.detection_date else "-",
                    "备注": sample.remark or "-"
                })

            df = pd.DataFrame(data)
            
            # 使用事件选择器显示表格
            selected_row = st.dataframe(
                df,
                use_container_width=True,
                selection_mode="single",
                key="sample_list"
            )

            # 操作按钮
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("查看详情", key="view_sample"):
                    if selected_row and len(selected_row["selection"]["rows"]) > 0:
                        row_idx = selected_row["selection"]["rows"][0]
                        sample = samples[row_idx]
                        show_sample_detail(sample)
            
            with col2:
                if st.button("删除样品", key="delete_sample"):
                    if selected_row and len(selected_row["selection"]["rows"]) > 0:
                        row_idx = selected_row["selection"]["rows"][0]
                        sample = samples[row_idx]
                        if service.delete_sample(sample.id):
                            st.success(f"样品 {sample.sample_no} 已删除")
                            st.rerun()
                        else:
                            st.error("删除失败")
            
            with col3:
                if st.button("手动录入", key="add_sample"):
                    st.session_state.show_add_form = True

        else:
            st.info("暂无样品数据，请添加或导入样品")

        # 显示添加表单
        if st.session_state.get("show_add_form", False):
            show_add_sample_form(service, db)

    finally:
        db.close()


def show_sample_detail(sample):
    """显示样品详情"""
    st.subheader(f"样品详情 - {sample.sample_no}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**样品编号**: {sample.sample_no}")
        st.markdown(f"**样品名称**: {sample.sample_name}")
        st.markdown(f"**样品类型**: {sample.sample_type or '-'}")
        st.markdown(f"**样品来源**: {sample.source or '-'}")
    
    with col2:
        st.markdown(f"**采样日期**: {sample.collection_date.strftime('%Y-%m-%d') if sample.collection_date else '-'}")
        st.markdown(f"**检测日期**: {sample.detection_date.strftime('%Y-%m-%d') if sample.detection_date else '-'}")
        st.markdown(f"**备注**: {sample.remark or '-'}")

    # 显示检测数据
    if sample.detection_data:
        detection_data = json.loads(sample.detection_data)
        st.subheader("检测指标数据")
        data = {
            "指标名称": list(detection_data.keys()),
            "检测值": list(detection_data.values())
        }
        st.dataframe(pd.DataFrame(data), use_container_width=True)


def show_add_sample_form(service: SampleService, db: Session):
    """显示添加样品表单"""
    st.subheader("手动录入样品")
    
    with st.form("add_sample_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            sample_no = st.text_input("样品编号 *", placeholder="例如：S20260311001")
            sample_name = st.text_input("样品名称 *", placeholder="例如：地表水样品")
            sample_type = st.text_input("样品类型", placeholder="例如：地表水、废水、大气")
        
        with col2:
            source = st.text_input("样品来源", placeholder="例如：XX 企业、XX 河流")
            collection_date = st.date_input("采样日期", value=datetime.now())
            remark = st.text_area("备注", placeholder="其他需要说明的信息")
        
        # 检测指标数据
        st.subheader("检测指标")
        indicators_input = st.text_area(
            "检测指标（JSON 格式）",
            value='{"pH": 7.2, "COD": 45.5, "氨氮": 0.8}',
            help="请输入 JSON 格式的检测数据，例如：{\"pH\": 7.2, \"COD\": 45.5}"
        )
        
        submitted = st.form_submit_button("提交")
        
        if submitted:
            if not sample_no or not sample_name:
                st.error("样品编号和样品名称为必填项")
            else:
                try:
                    # 验证 JSON 格式
                    detection_data = json.loads(indicators_input)
                    
                    sample_data = {
                        "sample_no": sample_no,
                        "sample_name": sample_name,
                        "sample_type": sample_type,
                        "source": source,
                        "collection_date": collection_date,
                        "detection_data": json.dumps(detection_data, ensure_ascii=False),
                        "remark": remark
                    }
                    
                    service.create_sample(sample_data)
                    st.success(f"样品 {sample_no} 添加成功！")
                    st.session_state.show_add_form = False
                    st.rerun()
                    
                except json.JSONDecodeError:
                    st.error("检测指标数据格式错误，请输入有效的 JSON 格式")
                except Exception as e:
                    st.error(f"添加失败：{str(e)}")


def download_template(standard_type: str):
    """下载指定标准类型的模板"""
    try:
        from utils.template_generator import create_template_excel
        
        excel_data = create_template_excel(standard_type)
        
        file_name = f"{standard_type}样品导入模板.xlsx"
        
        import io
        # 重新生成一次以确保数据完整
        buffer = io.BytesIO(excel_data)
        
        st.download_button(
            label=f"⬇️ 点击下载 {standard_type}模板",
            data=buffer.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_{standard_type}_template"
        )
        
        st.success(f"✅ {standard_type}模板已生成，请点击下载按钮保存")
        
    except Exception as e:
        st.error(f"生成模板失败：{str(e)}")


def show_batch_import():
    """批量导入功能"""
    st.subheader("批量导入样品")

    # 添加模板下载部分
    st.subheader("📋 下载数据模板")
    st.markdown("""
    请先下载与您评价标准对应的数据模板，按格式填写检测数据后再上传。
    这样可以确保数据格式正确，避免导入失败。
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 地表水模板", use_container_width=True):
            download_template('地表水')
        if st.button("📥 地下水模板", use_container_width=True):
            download_template('地下水')
    
    with col2:
        if st.button("📥 土壤模板", use_container_width=True):
            download_template('土壤')
        if st.button("📥 灌溉水模板", use_container_width=True):
            download_template('灌溉水')
    
    st.divider()

    uploaded_file = st.file_uploader(
        "上传 Excel 或 CSV 文件",
        type=["xlsx", "xls", "csv"],
        help="文件格式要求：必须包含'样品编号'和'样品名称'列"
    )

    if uploaded_file:
        try:
            # 保存临时文件
            temp_path = f"data/temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # 读取文件
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = read_excel_file(temp_path)
            else:
                df = read_csv_file(temp_path)

            st.subheader("数据预览")
            st.dataframe(df.head(10), use_container_width=True)
            st.info(f"共读取 {len(df)} 行数据")

            # 解析数据
            samples_data = parse_sample_data(df)
            
            # 验证数据
            valid_samples, errors = validate_samples_data(samples_data)

            if valid_samples:
                st.success(f"验证通过：{len(valid_samples)} 条有效数据")
                
                if st.button("确认导入"):
                    db = SessionLocal()
                    try:
                        service = SampleService(db)
                        created = service.batch_create_samples(valid_samples)
                        st.success(f"成功导入 {len(created)} 条样品数据！")
                        
                        # 清理临时文件
                        import os
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                            
                    finally:
                        db.close()
            else:
                st.error("数据验证失败")

            if errors:
                st.error("错误信息：")
                for error in errors:
                    st.write(f"- {error}")

        except Exception as e:
            st.error(f"导入失败：{str(e)}")
    else:
        st.info("请上传 Excel(.xlsx/.xls) 或 CSV 文件")
        
        # 下载模板
        st.subheader("下载导入模板")
        template_data = {
            "样品编号": ["S20260311001", "S20260311002"],
            "样品名称": ["地表水样品 1", "地表水样品 2"],
            "样品类型": ["地表水", "地表水"],
            "样品来源": ["XX 河流断面 1", "XX 河流断面 2"],
            "采样日期": ["2026-03-10", "2026-03-10"],
            "pH": [7.2, 7.5],
            "COD": [45.5, 38.2],
            "氨氮": [0.8, 0.6],
            "总磷": [0.15, 0.12],
            "备注": ["", ""]
        }
        
        template_df = pd.DataFrame(template_data)
        
        import io
        buffer = io.BytesIO()
        template_df.to_excel(buffer, index=False, engine='openpyxl')
        
        st.download_button(
            label="下载 Excel 模板",
            data=buffer.getvalue(),
            file_name="样品导入模板.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
