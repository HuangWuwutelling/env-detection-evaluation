"""
评价结果数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from .database import Base


class EvaluationResult(Base):
    """评价结果表"""
    __tablename__ = 'evaluation_results'

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey('samples.id'), nullable=False, comment='样品ID')
    sample_no = Column(String(50), nullable=False, comment='样品编号')
    standard_id = Column(Integer, ForeignKey('standards.id'), nullable=False, comment='标准ID')
    standard_name = Column(String(100), nullable=False, comment='评价标准名称')
    
    # 各指标评价详情（JSON格式存储）
    # 格式：[
    #   {
    #     "indicator": "pH",
    #     "value": 7.2,
    #     "min_limit": 6,
    #     "max_limit": 9,
    #     "unit": "无量纲",
    #     "result": "达标",
    #     "remark": ""
    #   },
    #   {
    #     "indicator": "COD",
    #     "value": 45.5,
    #     "max_limit": 20,
    #     "unit": "mg/L",
    #     "result": "超标",
    #     "remark": "超标倍数：1.28"
    #   }
    # ]
    evaluation_details = Column(Text, nullable=False, comment='评价详情')
    
    # 总体评价结论
    overall_result = Column(String(20), nullable=False, comment='总体评价结果（达标/超标）')
    conclusion = Column(String(500), comment='评价结论')
    
    evaluated_at = Column(DateTime, default=datetime.now, comment='评价时间')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')

    def __repr__(self):
        return f"<EvaluationResult(sample_no='{self.sample_no}', result='{self.overall_result}')>"
