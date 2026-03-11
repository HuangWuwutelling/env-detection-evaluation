"""
数据导入模板生成工具
为不同评价标准生成对应的 Excel 导入模板
"""
import pandas as pd
import io
from typing import List, Dict


def get_template_columns(standard_type: str) -> Dict:
    """
    根据标准类型返回模板列配置
    
    Args:
        standard_type: 标准类型（土壤、地表水、地下水、灌溉水）
    
    Returns:
        包含固定列和动态指标列的配置字典
    """
    # 所有模板都需要的固定列
    fixed_columns = {
        '样品编号': str,
        '样品名称': str,
        '样品类型': str,
        '样品来源': str,
        '采样日期': str,
        '备注': str
    }
    
    # 不同标准的检测指标列
    indicator_columns = {
        '土壤': {
            'pH': float,
            '镉': float,
            '汞': float,
            '砷': float,
            '铅': float,
            '铬': float,
            '铜': float,
            '镍': float,
            '锌': float,
            '六六六': float,
            '滴滴涕': float,
            '四氯化碳': float,
            '氯仿': float,
            '苯': float,
            '苯并 [a] 芘': float,
            '铬 (六价)': float
        },
        '地表水': {
            '水温': float,
            'pH': float,
            '溶解氧': float,
            '高锰酸盐指数': float,
            'COD': float,
            'BOD5': float,
            '氨氮': float,
            '总磷': float,
            '总氮': float,
            '铜': float,
            '锌': float,
            '氟化物': float,
            '硒': float,
            '砷': float,
            '汞': float,
            '镉': float,
            '铬 (六价)': float,
            '铅': float,
            '氰化物': float,
            '挥发酚': float,
            '石油类': float,
            '阴离子表面活性剂': float,
            '硫化物': float,
            '粪大肠菌群': float
        },
        '地下水': {
            '色度': float,
            '嗅和味': float,
            '浑浊度': float,
            '肉眼可见物': float,
            'pH': float,
            '总硬度': float,
            '溶解性总固体': float,
            '高锰酸盐指数': float,
            '氨氮': float,
            '硝酸盐': float,
            '亚硝酸盐': float,
            '挥发性酚类': float,
            '氰化物': float,
            '氟化物': float,
            '氯化物': float,
            '硫酸盐': float,
            '铁': float,
            '锰': float,
            '铜': float,
            '锌': float,
            '铝': float,
            '钼': float,
            '钴': float,
            '砷': float,
            '硒': float,
            '汞': float,
            '镉': float,
            '铬 (六价)': float,
            '铅': float,
            '铍': float,
            '钡': float,
            '镍': float,
            '滴滴涕': float,
            '六六六': float,
            '菌落总数': float,
            '总大肠菌群': float
        },
        '灌溉水': {
            'pH': float,
            '悬浮物': float,
            'COD': float,
            'BOD5': float,
            '氨氮': float,
            '总磷': float,
            '总氮': float,
            '石油类': float,
            '挥发酚': float,
            '氰化物': float,
            '氟化物': float,
            '硫化物': float,
            '铜': float,
            '锌': float,
            '硒': float,
            '砷': float,
            '汞': float,
            '镉': float,
            '铬 (六价)': float,
            '铅': float,
            '粪大肠菌群': float,
            '蛔虫卵数': float
        }
    }
    
    return {
        'fixed_columns': fixed_columns,
        'indicator_columns': indicator_columns.get(standard_type, {})
    }


def create_template_excel(standard_type: str, sample_count: int = 10) -> bytes:
    """
    创建指定标准类型的 Excel 模板
    
    Args:
        standard_type: 标准类型
        sample_count: 示例数据行数
    
    Returns:
        Excel 文件的二进制数据
    """
    config = get_template_columns(standard_type)
    
    # 合并所有列
    all_columns = list(config['fixed_columns'].keys()) + \
                  list(config['indicator_columns'].keys())
    
    # 创建 DataFrame
    df = pd.DataFrame(columns=all_columns)
    
    # 添加示例数据（前几行）
    example_data = []
    for i in range(min(sample_count, 5)):
        row = {}
        
        # 填充固定列
        row['样品编号'] = f'S{pd.Timestamp.now().strftime("%Y%m%d")}{str(i+1).zfill(3)}'
        row['样品名称'] = f'{standard_type}样品{i+1}'
        row['样品类型'] = standard_type
        row['样品来源'] = f'采样点{i+1}'
        row['采样日期'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        row['备注'] = ''
        
        # 填充示例检测数据（模拟合理值）
        for indicator in config['indicator_columns'].keys():
            row[indicator] = get_example_value(indicator, standard_type)
        
        example_data.append(row)
    
    # 将示例数据添加到 DataFrame
    if example_data:
        example_df = pd.DataFrame(example_data)
        df = pd.concat([example_df, df], ignore_index=True)
    
    # 写入 Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='样品数据')
        
        # 调整列宽
        worksheet = writer.sheets['样品数据']
        for i, col in enumerate(all_columns):
            # 根据列名长度和内容设置合适的列宽
            max_length = max(len(str(col)), 12)
            if col in ['样品编号', '样品名称']:
                max_length = 20
            elif col in ['备注']:
                max_length = 30
            
            column_width = min(max_length, 25)
            worksheet.column_dimensions[chr(65 + i)].width = column_width
        
        # 冻结首行
        worksheet.freeze_panes = "A2"
    
    return buffer.getvalue()


def get_example_value(indicator: str, standard_type: str) -> float:
    """
    获取指标的示例值（模拟合理的检测数据范围）
    
    Args:
        indicator: 指标名称
        standard_type: 标准类型
    
    Returns:
        示例数值
    """
    # 常见指标的典型值范围
    value_ranges = {
        'pH': (6.5, 8.5),
        'COD': (10, 50),
        'BOD5': (2, 10),
        '氨氮': (0.1, 2.0),
        '总磷': (0.05, 0.5),
        '总氮': (0.5, 3.0),
        '溶解氧': (5, 9),
        '高锰酸盐指数': (2, 8),
        '悬浮物': (10, 100),
        '水温': (15, 25),
        '总硬度': (100, 400),
        '溶解性总固体': (300, 1000),
        '硝酸盐': (5, 20),
        '亚硝酸盐': (0.01, 0.5),
        '石油类': (0.01, 0.5),
        '挥发酚': (0.001, 0.01),
        '氰化物': (0.001, 0.05),
        '氟化物': (0.5, 1.5),
        '硫化物': (0.01, 0.2),
        '粪大肠菌群': (100, 5000),
        
        # 重金属（mg/kg 或 mg/L）
        '铜': (0.01, 1.0),
        '锌': (0.05, 1.5),
        '砷': (0.001, 0.05),
        '汞': (0.0001, 0.001),
        '镉': (0.001, 0.01),
        '铬 (六价)': (0.001, 0.05),
        '铅': (0.001, 0.05),
        '镍': (0.01, 0.5),
        '铁': (0.1, 1.0),
        '锰': (0.05, 0.5),
        
        # 土壤特有
        '六六六': (0.01, 0.1),
        '滴滴涕': (0.01, 0.1),
        '四氯化碳': (0.001, 0.01),
        '氯仿': (0.001, 0.01),
        '苯': (0.01, 0.5),
        '苯并 [a] 芘': (0.1, 1.0),
    }
    
    # 获取范围并生成随机值
    if indicator in value_ranges:
        min_val, max_val = value_ranges[indicator]
        import random
        return round(random.uniform(min_val, max_val), 3)
    else:
        # 其他指标默认值
        return 0.0


def create_all_templates() -> Dict[str, bytes]:
    """
    创建所有标准类型的模板
    
    Returns:
        字典：{标准类型：Excel 文件二进制数据}
    """
    templates = {}
    
    standard_types = ['土壤', '地表水', '地下水', '灌溉水']
    
    for std_type in standard_types:
        try:
            templates[std_type] = create_template_excel(std_type)
            print(f"✅ 已生成 {std_type} 模板")
        except Exception as e:
            print(f"❌ 生成 {std_type} 模板失败：{e}")
    
    return templates


# 使用示例
if __name__ == "__main__":
    # 生成单个模板
    excel_data = create_template_excel('地表水')
    print(f"模板大小：{len(excel_data)} bytes")
    
    # 保存到本地测试
    with open('地表水样品导入模板.xlsx', 'wb') as f:
        f.write(excel_data)
    print("模板已保存为：地表水样品导入模板.xlsx")
