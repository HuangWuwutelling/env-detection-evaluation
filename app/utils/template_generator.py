"""
数据导入模板生成工具
统一的 Excel 导入模板，支持所有环境检测类型
"""
import pandas as pd
import io
from typing import List, Dict


def get_template_columns(standard_type: str = None) -> Dict:
    """
    返回统一的模板列配置
    
    Args:
        standard_type: 标准类型（可选，用于兼容旧代码）
    
    Returns:
        包含固定列和动态指标列的配置字典
    """
    # 统一模板的固定列（所有类型都需要）
    fixed_columns = {
        '样品编号': str,
        '样品名称': str,
        '样品类型': str,  # 土壤、地表水、地下水、灌溉水、空气等
        '样品来源': str,
        '采样日期': str,
        '评价标准': str,  # GB 15618-2018、GB 3838-2002 等
        '用地类型': str,  # 农用地/建设用地第一类/建设用地第二类（土壤专用）
        '农用地细分': str,  # 水田/果园/其他（仅农用地需要）
        'pH 分段': str,  # <5.5, 5.5-6.5, 6.5-7.5, >7.5（土壤专用）
        '水质类别': str,  # I 类、II 类、III 类、IV 类、V 类（水环境专用）
        '备注': str
    }
    
    # 不同标准的检测指标列（所有可能用到的指标）
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
    
    # 如果指定了标准类型，只返回该类型的指标；否则返回所有指标
    if standard_type:
        indicators = indicator_columns.get(standard_type, {})
    else:
        # 统一模板：合并所有类型的指标
        all_indicators = {}
        for indicators in indicator_columns.values():
            all_indicators.update(indicators)
        indicators = all_indicators
    
    # 返回时合并所有列（不再区分 special_columns）
    return {
        'fixed_columns': fixed_columns,
        'indicator_columns': indicators
    }


def create_template_excel(standard_type: str = None, sample_count: int = 10) -> bytes:
    """
    创建统一的 Excel 模板（支持所有类型）
    
    Args:
        standard_type: 标准类型（可选，用于过滤指标列）
        sample_count: 示例数据行数
    
    Returns:
        Excel 文件的二进制数据
    """
    config = get_template_columns(standard_type)
    
    # 合并所有列：固定列 + 指标列
    all_columns = list(config['fixed_columns'].keys()) + list(config['indicator_columns'].keys())
    
    # 创建 DataFrame
    df = pd.DataFrame(columns=all_columns)
    
    # 添加示例数据（前几行）- 展示不同类型的样品
    example_data = []
    
    # 定义不同类型样品的示例配置
    sample_configs = [
        {'样品类型': '土壤', '用地类型': '农用地', '农用地细分': '水田', 'pH 分段': '6.5-7.5'},
        {'样品类型': '土壤', '用地类型': '农用地', '农用地细分': '果园', 'pH 分段': '5.5-6.5'},
        {'样品类型': '土壤', '用地类型': '建设用地第一类', '农用地细分': '', 'pH 分段': ''},
        {'样品类型': '地表水', '水质类别': 'III 类'},
        {'样品类型': '地下水', '水质类别': 'II 类'},
        {'样品类型': '灌溉水', '水质类别': 'I 类'}
    ]
    
    for i in range(min(sample_count, len(sample_configs))):
        row = {}
        config = sample_configs[i]
        
        # 填充固定列
        row['样品编号'] = f'S{pd.Timestamp.now().strftime("%Y%m%d")}{str(i+1).zfill(3)}'
        row['样品名称'] = f'{config["样品类型"]}样品{i+1}'
        row['样品类型'] = config['样品类型']
        row['样品来源'] = f'采样点{i+1}'
        row['采样日期'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        row['评价标准'] = get_standard_code(row['样品类型'])
        row['用地类型'] = config.get('用地类型', '')
        row['农用地细分'] = config.get('农用地细分', '')
        row['pH 分段'] = config.get('pH 分段', '')
        row['水质类别'] = config.get('水质类别', '')
        row['备注'] = ''
        
        # 填充示例检测数据（模拟合理值）- 根据样品类型选择对应的指标
        sample_type_indicators = {
            '土壤': ['pH', '镉', '汞', '砷', '铅', '铬', '铜', '镍', '锌'],
            '地表水': ['水温', 'pH', '溶解氧', '高锰酸盐指数', 'COD', '氨氮'],
            '地下水': ['pH', '总硬度', '溶解性总固体', '氨氮', '硝酸盐'],
            '灌溉水': ['pH', '悬浮物', 'COD', 'BOD5', '氨氮']
        }
        
        indicators_for_type = sample_type_indicators.get(row['样品类型'], [])
        all_indicators = config.get('indicator_columns', {})
        for indicator in indicators_for_type:
            if indicator in all_indicators:
                row[indicator] = get_example_value(indicator, row['样品类型'])
        
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
            # 使用列索引而不是字母来设置宽度
            col_letter = worksheet.cell(row=1, column=i+1).column_letter
            worksheet.column_dimensions[col_letter].width = column_width
        
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
    templates = create_all_templates()
    
    # 或者生成统一模板（包含所有指标）
    unified_template = create_template_excel(None)
    print("\n✅ 已生成统一模板（包含所有环境检测类型）")
    
    # 保存到本地测试
    with open('统一环境检测模板.xlsx', 'wb') as f:
        f.write(unified_template)
    print("模板已保存为：统一环境检测模板.xlsx")


def get_standard_code(sample_type: str) -> str:
    """
    根据样品类型返回对应的国家标准代码
    
    Args:
        sample_type: 样品类型
    
    Returns:
        国家标准代码
    """
    standard_map = {
        '土壤': 'GB 15618-2018',
        '地表水': 'GB 3838-2002',
        '地下水': 'GB/T 14848-2017',
        '灌溉水': 'GB 5084-2021',
        '空气': 'GB 3095-2012'
    }
    return standard_map.get(sample_type, '')
