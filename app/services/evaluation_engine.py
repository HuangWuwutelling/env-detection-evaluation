"""
评价引擎 - 核心逻辑
"""
import json
from typing import List, Dict, Optional
from services.soil_limit_matcher import SoilLimitMatcher


class EvaluationEngine:
    """评价引擎类"""

    @staticmethod
    def evaluate_indicator(
        indicator_name: str,
        value: float,
        limit_config: dict
    ) -> dict:
        """
        评价单个指标
        
        Args:
            indicator_name: 指标名称
            value: 实测值
            limit_config: 限值配置，如：
                {
                    "indicator": "pH",
                    "min_limit": 6,
                    "max_limit": 9,
                    "unit": "无量纲",
                    "operator": "between"
                }
        
        Returns:
            评价结果字典
        """
        result = {
            "indicator": indicator_name,
            "value": value,
            "unit": limit_config.get("unit", ""),
            "result": "达标",
            "remark": ""
        }

        # 添加限值信息
        if "min_limit" in limit_config:
            result["min_limit"] = limit_config["min_limit"]
        if "max_limit" in limit_config:
            result["max_limit"] = limit_config["max_limit"]

        operator = limit_config.get("operator", "<=")

        # 根据操作符进行判定
        if operator == "<=":
            # 小于等于限值为达标
            max_limit = limit_config.get("max_limit")
            if max_limit is not None and value > max_limit:
                result["result"] = "超标"
                result["remark"] = f"超标倍数：{(value - max_limit) / max_limit:.2f}"

        elif operator == ">=":
            # 大于等于限值为达标（适用于某些需要达到最低标准的指标）
            min_limit = limit_config.get("min_limit")
            if min_limit is not None and value < min_limit:
                result["result"] = "不达标"
                result["remark"] = f"低于标准值：{min_limit - value}"

        elif operator == "between":
            # 在区间内为达标
            min_limit = limit_config.get("min_limit")
            max_limit = limit_config.get("max_limit")
            if min_limit is not None and max_limit is not None:
                if value < min_limit or value > max_limit:
                    result["result"] = "超标"
                    if value < min_limit:
                        result["remark"] = f"低于下限：{min_limit - value}"
                    else:
                        result["remark"] = f"超出上限：{value - max_limit}"

        return result

    @staticmethod
    def evaluate_sample(
        detection_data: Dict[str, float],
        limits: List[dict],
        land_use_type: str = '',  # 用地类型（农用地/建设用地第一类/建设用地第二类）
        agri_sub_type: str = '',   # 农用地细分（水田/果园/其他）
        ph_range: str = ''         # pH 分段（<5.5, 5.5-6.5, 6.5-7.5, >7.5）
    ) -> tuple:
        """
        评价整个样品
        
        Args:
            detection_data: 检测数据，如 {"pH": 7.2, "COD": 45.5}
            limits: 限值配置列表
            land_use_type: 用地类型（仅土壤需要）
            agri_sub_type: 农用地细分类型（仅农用地需要）
            ph_range: pH 分段（仅农用地需要）
        
        Returns:
            (总体评价结果，评价详情列表)
        """
        details = []
        has_exceedance = False

        for limit_config in limits:
            indicator = limit_config.get("indicator")
            value = detection_data.get(indicator)

            if value is not None:
                # 土壤特殊处理：根据用地类型匹配限值
                if land_use_type in ['农用地', '建设用地第一类', '建设用地第二类']:
                    soil_limit = SoilLimitMatcher.get_soil_limit(
                        indicator, land_use_type, agri_sub_type, ph_range
                    )
                    
                    if soil_limit is not None:
                        # 使用匹配的限值进行评价
                        result = EvaluationEngine.evaluate_indicator(
                            indicator, value,
                            {"indicator": indicator, "operator": "<=", "max_limit": soil_limit, "unit": "mg/kg"}
                        )
                        # 添加额外信息
                        result['land_use_type'] = land_use_type
                        if land_use_type == '农用地':
                            result['agri_sub_type'] = agri_sub_type
                            result['ph_range'] = ph_range
                        
                        details.append(result)
                        if result["result"] != "达标":
                            has_exceedance = True
                        continue
                
                # 非土壤或使用默认限值配置
                result = EvaluationEngine.evaluate_indicator(
                    indicator, value, limit_config
                )
                details.append(result)

                if result["result"] != "达标":
                    has_exceedance = True
            else:
                # 该指标未检测
                details.append({
                    "indicator": indicator,
                    "value": None,
                    "unit": limit_config.get("unit", ""),
                    "result": "未检测",
                    "remark": "该指标未提供检测数据",
                    "min_limit": limit_config.get("min_limit"),
                    "max_limit": limit_config.get("max_limit")
                })

        overall_result = "超标" if has_exceedance else "达标"
        return overall_result, details
