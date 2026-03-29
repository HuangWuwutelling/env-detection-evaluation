"""
土壤污染风险管控标准限值匹配器
根据 GB 15618-2018 和 GB 36600-2018 自动匹配不同用地类型的限值
"""
from typing import Dict, Optional


class SoilLimitMatcher:
    """土壤限值匹配器"""
    
    # GB 15618-2018 农用地土壤污染风险管控标准
    # 单位：mg/kg (pH 无量纲)
    AGRICULTURAL_LIMITS = {
        '水田': {
            '<5.5': {
                '镉': 0.3, '汞': 3.4, '砷': 30, '铅': 70, '铬': 250,
                '铜': 50, '镍': 60, '锌': 200, '六六六': 0.05, '滴滴涕': 0.05
            },
            '5.5-6.5': {
                '镉': 0.4, '汞': 4.0, '砷': 30, '铅': 90, '铬': 250,
                '铜': 50, '镍': 70, '锌': 250, '六六六': 0.05, '滴滴涕': 0.05
            },
            '6.5-7.5': {
                '镉': 0.5, '汞': 5.0, '砷': 25, '铅': 120, '铬': 250,
                '铜': 100, '镍': 100, '锌': 300, '六六六': 0.05, '滴滴涕': 0.05
            },
            '>7.5': {
                '镉': 0.6, '汞': 6.0, '砷': 20, '铅': 170, '铬': 250,
                '铜': 100, '镍': 100, '锌': 350, '六六六': 0.05, '滴滴涕': 0.05
            }
        },
        '旱地': {
            '<5.5': {
                '镉': 0.3, '汞': 1.3, '砷': 40, '铅': 70, '铬': 250,
                '铜': 50, '镍': 60, '锌': 200, '六六六': 0.05, '滴滴涕': 0.05
            },
            '5.5-6.5': {
                '镉': 0.3, '汞': 1.8, '砷': 40, '铅': 90, '铬': 250,
                '铜': 50, '镍': 70, '锌': 250, '六六六': 0.05, '滴滴涕': 0.05
            },
            '6.5-7.5': {
                '镉': 0.3, '汞': 2.4, '砷': 30, '铅': 120, '铬': 250,
                '铜': 100, '镍': 100, '锌': 300, '六六六': 0.05, '滴滴涕': 0.05
            },
            '>7.5': {
                '镉': 0.6, '汞': 3.4, '砷': 25, '铅': 170, '铬': 250,
                '铜': 100, '镍': 100, '锌': 350, '六六六': 0.05, '滴滴涕': 0.05
            }
        },
        '果园': {
            '<5.5': {
                '镉': 0.3, '汞': 1.3, '砷': 40, '铅': 70, '铬': 250,
                '铜': 50, '镍': 60, '锌': 200, '六六六': 0.05, '滴滴涕': 0.05
            },
            '5.5-6.5': {
                '镉': 0.3, '汞': 1.8, '砷': 40, '铅': 90, '铬': 250,
                '铜': 50, '镍': 70, '锌': 250, '六六六': 0.05, '滴滴涕': 0.05
            },
            '6.5-7.5': {
                '镉': 0.3, '汞': 2.4, '砷': 30, '铅': 120, '铬': 250,
                '铜': 100, '镍': 100, '锌': 300, '六六六': 0.05, '滴滴涕': 0.05
            },
            '>7.5': {
                '镉': 0.6, '汞': 3.4, '砷': 25, '铅': 170, '铬': 250,
                '铜': 100, '镍': 100, '锌': 350, '六六六': 0.05, '滴滴涕': 0.05
            }
        },
        '其他': {
            # 其他类型暂时使用旱地的限值
            '<5.5': {
                '镉': 0.3, '汞': 1.3, '砷': 40, '铅': 70, '铬': 250,
                '铜': 50, '镍': 60, '锌': 200, '六六六': 0.05, '滴滴涕': 0.05
            },
            '5.5-6.5': {
                '镉': 0.3, '汞': 1.8, '砷': 40, '铅': 90, '铬': 250,
                '铜': 50, '镍': 70, '锌': 250, '六六六': 0.05, '滴滴涕': 0.05
            },
            '6.5-7.5': {
                '镉': 0.3, '汞': 2.4, '砷': 30, '铅': 120, '铬': 250,
                '铜': 100, '镍': 100, '锌': 300, '六六六': 0.05, '滴滴涕': 0.05
            },
            '>7.5': {
                '镉': 0.6, '汞': 3.4, '砷': 25, '铅': 170, '铬': 250,
                '铜': 100, '镍': 100, '锌': 350, '六六六': 0.05, '滴滴涕': 0.05
            }
        }
    }
    
    # GB 36600-2018 建设用地土壤污染风险管控标准
    # 第一类用地：居住用地、公共管理与公共服务用地等
    CONSTRUCTION_TYPE1_LIMITS = {
        '砷': 60, '镉': 65, '铬 (六价)': 5.7, '铜': 18000, '铅': 800,
        '汞': 38, '镍': 900, '四氯化碳': 2.8, '氯仿': 0.9, '苯': 4,
        '苯并 [a] 芘': 1.5
    }
    
    # 第二类用地：工业用地、商业服务业设施用地等
    CONSTRUCTION_TYPE2_LIMITS = {
        '砷': 140, '镉': 65, '铬 (六价)': 5.7, '铜': 18000, '铅': 800,
        '汞': 38, '镍': 900, '四氯化碳': 2.8, '氯仿': 0.9, '苯': 4,
        '苯并 [a] 芘': 1.5
    }
    
    @staticmethod
    def get_agricultural_limit(indicator: str, agri_type: str, ph_range: str) -> Optional[float]:
        """
        获取农用地污染物限值
        
        Args:
            indicator: 污染物指标名称
            agri_type: 农用地类型（水田/旱地/果园/其他）
            ph_range: pH 分段（<5.5, 5.5-6.5, 6.5-7.5, >7.5）
        
        Returns:
            限值（mg/kg），如果找不到则返回 None
        """
        if agri_type not in SoilLimitMatcher.AGRICULTURAL_LIMITS:
            return None
            
        if ph_range not in SoilLimitMatcher.AGRICULTURAL_LIMITS[agri_type]:
            return None
            
        limits = SoilLimitMatcher.AGRICULTURAL_LIMITS[agri_type][ph_range]
        return limits.get(indicator)
    
    @staticmethod
    def get_construction_limit(indicator: str, land_type: str) -> Optional[float]:
        """
        获取建设用地污染物限值
        
        Args:
            indicator: 污染物指标名称
            land_type: 用地类型（建设用地第一类/建设用地第二类）
        
        Returns:
            限值（mg/kg），如果找不到则返回 None
        """
        if land_type == '建设用地第一类':
            return SoilLimitMatcher.CONSTRUCTION_TYPE1_LIMITS.get(indicator)
        elif land_type == '建设用地第二类':
            return SoilLimitMatcher.CONSTRUCTION_TYPE2_LIMITS.get(indicator)
        return None
    
    @staticmethod
    def get_soil_limit(indicator: str, land_use_type: str, 
                      agri_sub_type: str = '', ph_range: str = '') -> Optional[float]:
        """
        获取土壤污染物限值（统一接口）
        
        Args:
            indicator: 污染物指标名称
            land_use_type: 用地类型（农用地/建设用地第一类/建设用地第二类）
            agri_sub_type: 农用地细分类型（水田/果园/其他），仅农用地需要
            ph_range: pH 分段（<5.5, 5.5-6.5, 6.5-7.5, >7.5），仅农用地需要
        
        Returns:
            限值（mg/kg），如果找不到则返回 None
        """
        if land_use_type == '农用地':
            return SoilLimitMatcher.get_agricultural_limit(indicator, agri_sub_type, ph_range)
        elif land_use_type in ['建设用地第一类', '建设用地第二类']:
            return SoilLimitMatcher.get_construction_limit(indicator, land_use_type)
        return None


# 测试
if __name__ == "__main__":
    print("土壤限值匹配器测试")
    print("=" * 50)
    
    # 测试农用地 - 水田
    limit = SoilLimitMatcher.get_soil_limit('镉', '农用地', '水田', '<5.5')
    print(f"水田，pH<5.5, 镉的限值：{limit} mg/kg")
    
    # 测试农用地 - 果园
    limit = SoilLimitMatcher.get_soil_limit('汞', '农用地', '果园', '6.5-7.5')
    print(f"果园，pH6.5-7.5, 汞的限值：{limit} mg/kg")
    
    # 测试建设用地第一类
    limit = SoilLimitMatcher.get_soil_limit('砷', '建设用地第一类')
    print(f"建设用地第一类，砷的限值：{limit} mg/kg")
    
    # 测试建设用地第二类
    limit = SoilLimitMatcher.get_soil_limit('砷', '建设用地第二类')
    print(f"建设用地第二类，砷的限值：{limit} mg/kg")
