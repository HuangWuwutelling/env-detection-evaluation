"""
Excel/CSV文件导入工具
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict


def read_excel_file(file_path: str) -> pd.DataFrame:
    """读取 Excel 文件"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        raise Exception(f"读取 Excel 文件失败：{str(e)}")


def read_csv_file(file_path: str) -> pd.DataFrame:
    """读取 CSV 文件"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except Exception as e:
        # 尝试其他编码
        try:
            df = pd.read_csv(file_path, encoding='gbk')
            return df
        except Exception as e2:
            raise Exception(f"读取 CSV 文件失败：{str(e2)}")


def parse_sample_data(df: pd.DataFrame) -> List[Dict]:
    """
    将 DataFrame 解析为样品数据列表（支持统一模板）
    
    期望的列名：
    - 样品编号 (必需)
    - 样品名称 (必需)
    - 样品类型
    - 样品来源
    - 采样日期
    - 评价标准
    - 用地类型
    - 农用地细分
    - pH 分段
    - 水质类别
    - 检测指标... (动态列)
    
    Returns:
        样品数据列表，每个包含：
        {
            "sample_no": "编号",
            "sample_name": "名称",
            "sample_type": "类型",
            "source": "来源",
            "collection_date": datetime,
            "standard_code": "GB 编号",
            "land_use_type": "用地类型",
            "agri_sub_type": "农用地细分",
            "ph_range": "pH 分段",
            "water_class": "水质类别",
            "detection_data": json_string,
            "remark": ""
        }
    """
    samples_data = []

    # 必需的列
    required_columns = ['样品编号', '样品名称']
    
    # 检查必需列
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"缺少必需列：{col}")

    # 遍历每一行
    for index, row in df.iterrows():
        try:
            # 提取基本信息
            sample_data = {
                "sample_no": str(row['样品编号']).strip(),
                "sample_name": str(row['样品名称']).strip(),
                "sample_type": str(row.get('样品类型', '')).strip(),
                "source": str(row.get('样品来源', '')).strip(),
                "remark": str(row.get('备注', '')).strip(),
                # 新增字段
                "standard_code": str(row.get('评价标准', '')).strip() if pd.notna(row.get('评价标准')) else '',
                "land_use_type": str(row.get('用地类型', '')).strip() if pd.notna(row.get('用地类型')) else '',
                "agri_sub_type": str(row.get('农用地细分', '')).strip() if pd.notna(row.get('农用地细分')) else '',
                "ph_range": str(row.get('pH 分段', '')).strip() if pd.notna(row.get('pH 分段')) else '',
                "water_class": str(row.get('水质类别', '')).strip() if pd.notna(row.get('水质类别')) else ''
            }

            # 处理采样日期
            if '采样日期' in row and pd.notna(row['采样日期']):
                if isinstance(row['采样日期'], datetime):
                    sample_data["collection_date"] = row['采样日期']
                else:
                    try:
                        sample_data["collection_date"] = datetime.strptime(
                            str(row['采样日期']), '%Y-%m-%d'
                        )
                    except:
                        sample_data["collection_date"] = None
            else:
                sample_data["collection_date"] = None

            # 提取检测指标数据（除了已处理的列之外的所有列）
            excluded_cols = ['样品编号', '样品名称', '样品类型', '样品来源', 
                           '采样日期', '备注', '评价标准', '用地类型', 
                           '农用地细分', 'pH 分段', '水质类别']
            detection_data = {}
            
            for col in df.columns:
                if col not in excluded_cols:
                    if pd.notna(row[col]):
                        try:
                            detection_data[col] = float(row[col])
                        except (ValueError, TypeError):
                            detection_data[col] = str(row[col])

            # 转为 JSON 字符串存储
            import json
            sample_data["detection_data"] = json.dumps(detection_data, ensure_ascii=False)

            samples_data.append(sample_data)

        except Exception as e:
            print(f"解析第{index + 1}行失败：{str(e)}")
            continue

    return samples_data


def validate_samples_data(samples_data: List[Dict]) -> tuple:
    """
    验证样品数据
    
    Returns:
        (valid_samples, errors) 有效数据和错误信息
    """
    valid_samples = []
    errors = []

    for i, data in enumerate(samples_data):
        # 检查必需字段
        if not data.get('sample_no'):
            errors.append(f"第{i + 1}条数据缺少样品编号")
            continue
        
        if not data.get('sample_name'):
            errors.append(f"第{i + 1}条数据缺少样品名称")
            continue

        # 检查检测数据
        if not data.get('detection_data'):
            errors.append(f"第{i + 1}条数据缺少检测指标")
            continue

        valid_samples.append(data)

    return valid_samples, errors
