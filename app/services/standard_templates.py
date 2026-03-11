"""
预设环境检测标准模板
包含常用的国家环境质量标准
"""
import json


# 土壤环境质量标准 - GB 15618-2018
# 农用地土壤污染风险管控标准
SOIL_GB15618_2018 = {
    "standard_name": "土壤环境质量 农用地土壤污染风险管控标准",
    "standard_code": "GB 15618-2018",
    "standard_type": "土壤",
    "description": "适用于农用地土壤污染风险筛查和风险评估",
    "limits": [
        {"indicator": "pH", "operator": "between", "min_limit": None, "max_limit": None, "unit": "无量纲"},
        {"indicator": "镉", "operator": "<=", "max_limit": 0.3, "unit": "mg/kg"},
        {"indicator": "汞", "operator": "<=", "max_limit": 3.4, "unit": "mg/kg"},
        {"indicator": "砷", "operator": "<=", "max_limit": 30, "unit": "mg/kg"},
        {"indicator": "铅", "operator": "<=", "max_limit": 70, "unit": "mg/kg"},
        {"indicator": "铬", "operator": "<=", "max_limit": 250, "unit": "mg/kg"},
        {"indicator": "铜", "operator": "<=", "max_limit": 50, "unit": "mg/kg"},
        {"indicator": "镍", "operator": "<=", "max_limit": 60, "unit": "mg/kg"},
        {"indicator": "锌", "operator": "<=", "max_limit": 200, "unit": "mg/kg"},
        {"indicator": "六六六", "operator": "<=", "max_limit": 0.05, "unit": "mg/kg"},
        {"indicator": "滴滴涕", "operator": "<=", "max_limit": 0.05, "unit": "mg/kg"}
    ]
}


# 建设用地土壤污染风险管控标准 - GB 36600-2018
SOIL_GB36600_2018 = {
    "standard_name": "土壤环境质量 建设用地土壤污染风险管控标准",
    "standard_code": "GB 36600-2018",
    "standard_type": "土壤",
    "description": "适用于建设用地土壤污染风险筛查（第一类用地/第二类用地）",
    "limits": [
        {"indicator": "砷", "operator": "<=", "max_limit": 60, "unit": "mg/kg"},
        {"indicator": "镉", "operator": "<=", "max_limit": 65, "unit": "mg/kg"},
        {"indicator": "铬 (六价)", "operator": "<=", "max_limit": 5.7, "unit": "mg/kg"},
        {"indicator": "铜", "operator": "<=", "max_limit": 18000, "unit": "mg/kg"},
        {"indicator": "铅", "operator": "<=", "max_limit": 800, "unit": "mg/kg"},
        {"indicator": "汞", "operator": "<=", "max_limit": 38, "unit": "mg/kg"},
        {"indicator": "镍", "operator": "<=", "max_limit": 900, "unit": "mg/kg"},
        {"indicator": "四氯化碳", "operator": "<=", "max_limit": 2.8, "unit": "mg/kg"},
        {"indicator": "氯仿", "operator": "<=", "max_limit": 0.9, "unit": "mg/kg"},
        {"indicator": "苯", "operator": "<=", "max_limit": 4, "unit": "mg/kg"},
        {"indicator": "苯并 [a] 芘", "operator": "<=", "max_limit": 1.5, "unit": "mg/kg"}
    ]
}


# 地表水环境质量标准 - GB 3838-2002
SURFACE_WATER_GB3838_2002 = {
    "standard_name": "地表水环境质量标准",
    "standard_code": "GB 3838-2002",
    "standard_type": "地表水",
    "description": "适用于全国江河、湖泊、运河、渠道、水库等具有使用功能的地表水水域",
    "limits": [
        {"indicator": "水温", "operator": "between", "min_limit": None, "max_limit": None, "unit": "℃"},
        {"indicator": "pH", "operator": "between", "min_limit": 6, "max_limit": 9, "unit": "无量纲"},
        {"indicator": "溶解氧", "operator": ">=", "min_limit": 5, "unit": "mg/L"},
        {"indicator": "高锰酸盐指数", "operator": "<=", "max_limit": 6, "unit": "mg/L"},
        {"indicator": "COD", "operator": "<=", "max_limit": 20, "unit": "mg/L"},
        {"indicator": "BOD5", "operator": "<=", "max_limit": 4, "unit": "mg/L"},
        {"indicator": "氨氮", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "总磷", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "总氮", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "铜", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "锌", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "氟化物", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "硒", "operator": "<=", "max_limit": 0.01, "unit": "mg/L"},
        {"indicator": "砷", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "汞", "operator": "<=", "max_limit": 0.0001, "unit": "mg/L"},
        {"indicator": "镉", "operator": "<=", "max_limit": 0.005, "unit": "mg/L"},
        {"indicator": "铬 (六价)", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "铅", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "氰化物", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "挥发酚", "operator": "<=", "max_limit": 0.005, "unit": "mg/L"},
        {"indicator": "石油类", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "阴离子表面活性剂", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "硫化物", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "粪大肠菌群", "operator": "<=", "max_limit": 10000, "unit": "个/L"}
    ]
}


# 地下水质量标准 - GB/T 14848-2017
GROUNDWATER_GB14848_2017 = {
    "standard_name": "地下水质量标准",
    "standard_code": "GB/T 14848-2017",
    "standard_type": "地下水",
    "description": "适用于地下水质量分类、监测、评价和管理",
    "limits": [
        {"indicator": "色度", "operator": "<=", "max_limit": 15, "unit": "度"},
        {"indicator": "嗅和味", "operator": "<=", "max_limit": 3, "unit": "级"},
        {"indicator": "浑浊度", "operator": "<=", "max_limit": 3, "unit": "NTU"},
        {"indicator": "肉眼可见物", "operator": "<=", "max_limit": 5, "unit": "级"},
        {"indicator": "pH", "operator": "between", "min_limit": 6.5, "max_limit": 8.5, "unit": "无量纲"},
        {"indicator": "总硬度", "operator": "<=", "max_limit": 450, "unit": "mg/L"},
        {"indicator": "溶解性总固体", "operator": "<=", "max_limit": 1000, "unit": "mg/L"},
        {"indicator": "高锰酸盐指数", "operator": "<=", "max_limit": 3.0, "unit": "mg/L"},
        {"indicator": "氨氮", "operator": "<=", "max_limit": 0.5, "unit": "mg/L"},
        {"indicator": "硝酸盐", "operator": "<=", "max_limit": 20, "unit": "mg/L"},
        {"indicator": "亚硝酸盐", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "挥发性酚类", "operator": "<=", "max_limit": 0.002, "unit": "mg/L"},
        {"indicator": "氰化物", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "氟化物", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "氯化物", "operator": "<=", "max_limit": 250, "unit": "mg/L"},
        {"indicator": "硫酸盐", "operator": "<=", "max_limit": 250, "unit": "mg/L"},
        {"indicator": "铁", "operator": "<=", "max_limit": 0.3, "unit": "mg/L"},
        {"indicator": "锰", "operator": "<=", "max_limit": 0.1, "unit": "mg/L"},
        {"indicator": "铜", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "锌", "operator": "<=", "max_limit": 1.0, "unit": "mg/L"},
        {"indicator": "铝", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "钼", "operator": "<=", "max_limit": 0.07, "unit": "mg/L"},
        {"indicator": "钴", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "砷", "operator": "<=", "max_limit": 0.01, "unit": "mg/L"},
        {"indicator": "硒", "operator": "<=", "max_limit": 0.01, "unit": "mg/L"},
        {"indicator": "汞", "operator": "<=", "max_limit": 0.001, "unit": "mg/L"},
        {"indicator": "镉", "operator": "<=", "max_limit": 0.005, "unit": "mg/L"},
        {"indicator": "铬 (六价)", "operator": "<=", "max_limit": 0.05, "unit": "mg/L"},
        {"indicator": "铅", "operator": "<=", "max_limit": 0.01, "unit": "mg/L"},
        {"indicator": "铍", "operator": "<=", "max_limit": 0.002, "unit": "mg/L"},
        {"indicator": "钡", "operator": "<=", "max_limit": 0.7, "unit": "mg/L"},
        {"indicator": "镍", "operator": "<=", "max_limit": 0.02, "unit": "mg/L"},
        {"indicator": "滴滴涕", "operator": "<=", "max_limit": 0.001, "unit": "mg/L"},
        {"indicator": "六六六", "operator": "<=", "max_limit": 0.005, "unit": "mg/L"},
        {"indicator": "菌落总数", "operator": "<=", "max_limit": 100, "unit": "CFU/mL"},
        {"indicator": "总大肠菌群", "operator": "<=", "max_limit": 3, "unit": "MPN/100mL"}
    ]
}


# 农田灌溉水质标准 - GB 5084-2021
IRRIGATION_WATER_GB5084_2021 = {
    "standard_name": "农田灌溉水质标准",
    "standard_code": "GB 5084-2021",
    "standard_type": "灌溉水",
    "description": "适用于以地表水、地下水和处理后的养殖业废水及以农产品为原料加工的工业废水作为水源的农田灌溉用水",
    "limits": [
        {"indicator": "pH", "operator": "between", "min_limit": 5.5, "max_limit": 8.5, "unit": "无量纲"},
        {"indicator": "悬浮物", "operator": "<=", "max_limit": 100, "unit": "mg/L"},
        {"indicator": "COD", "operator": "<=", "max_limit": 200, "unit": "mg/L"},
        {"indicator": "BOD5", "operator": "<=", "max_limit": 100, "unit": "mg/L"},
        {"indicator": "氨氮", "operator": "<=", "max_limit": 40, "unit": "mg/L"},
        {"indicator": "总磷", "operator": "<=", "max_limit": 10, "unit": "mg/L"},
        {"indicator": "总氮", "operator": "<=", "max_limit": 40, "unit": "mg/L"},
        {"indicator": "石油类", "operator": "<=", "max_limit": 10, "unit": "mg/L"},
        {"indicator": "挥发酚", "operator": "<=", "max_limit": 1, "unit": "mg/L"},
        {"indicator": "氰化物", "operator": "<=", "max_limit": 0.5, "unit": "mg/L"},
        {"indicator": "氟化物", "operator": "<=", "max_limit": 3, "unit": "mg/L"},
        {"indicator": "硫化物", "operator": "<=", "max_limit": 1, "unit": "mg/L"},
        {"indicator": "铜", "operator": "<=", "max_limit": 1, "unit": "mg/L"},
        {"indicator": "锌", "operator": "<=", "max_limit": 5, "unit": "mg/L"},
        {"indicator": "硒", "operator": "<=", "max_limit": 0.02, "unit": "mg/L"},
        {"indicator": "砷", "operator": "<=", "max_limit": 0.1, "unit": "mg/L"},
        {"indicator": "汞", "operator": "<=", "max_limit": 0.001, "unit": "mg/L"},
        {"indicator": "镉", "operator": "<=", "max_limit": 0.01, "unit": "mg/L"},
        {"indicator": "铬 (六价)", "operator": "<=", "max_limit": 0.1, "unit": "mg/L"},
        {"indicator": "铅", "operator": "<=", "max_limit": 0.2, "unit": "mg/L"},
        {"indicator": "粪大肠菌群", "operator": "<=", "max_limit": 40000, "unit": "个/L"},
        {"indicator": "蛔虫卵数", "operator": "<=", "max_limit": 2, "unit": "个/L"}
    ]
}


# 所有标准模板列表
STANDARD_TEMPLATES = [
    SOIL_GB15618_2018,
    SOIL_GB36600_2018,
    SURFACE_WATER_GB3838_2002,
    GROUNDWATER_GB14848_2017,
    IRRIGATION_WATER_GB5084_2021
]


def get_template_by_code(standard_code: str) -> dict | None:
    """根据标准编号获取模板"""
    for template in STANDARD_TEMPLATES:
        if template["standard_code"] == standard_code:
            return template
    return None


def get_templates_by_type(standard_type: str) -> list:
    """根据类型获取所有模板"""
    return [t for t in STANDARD_TEMPLATES if t["standard_type"] == standard_type]


def load_template_to_db(template: dict, db_session):
    """
    将标准模板加载到数据库
    
    Args:
        template: 标准模板字典
        db_session: 数据库会话
    """
    from services.standard_service import StandardService
    
    service = StandardService(db_session)
    
    # 检查是否已存在
    existing = service.get_standards()
    for std in existing:
        if std.standard_code == template["standard_code"]:
            return std  # 已存在则返回
    
    # 创建新标准
    standard_data = {
        "standard_name": template["standard_name"],
        "standard_code": template["standard_code"],
        "standard_type": template["standard_type"],
        "limits": json.dumps(template["limits"], ensure_ascii=False),
        "description": template.get("description", "")
    }
    
    return service.create_standard(standard_data)


def initialize_all_templates(db_session):
    """初始化所有标准模板到数据库"""
    created_templates = []
    for template in STANDARD_TEMPLATES:
        try:
            std = load_template_to_db(template, db_session)
            created_templates.append(std)
            print(f"已加载标准模板：{template['standard_name']} ({template['standard_code']})")
        except Exception as e:
            print(f"加载模板失败 {template['standard_code']}: {str(e)}")
    
    return created_templates
