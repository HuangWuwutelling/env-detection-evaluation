"""
评价标准数据模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime
from .database import Base


class Standard(Base):
    """评价标准表"""
    __tablename__ = 'standards'

    id = Column(Integer, primary_key=True, index=True)
    standard_name = Column(String(100), nullable=False, comment='标准名称')
    standard_code = Column(String(50), unique=True, comment='标准编号（如GB/T 12345-2020）')
    standard_type = Column(String(50), comment='标准类型（如地表水、大气、土壤等）')
    
    # 评价指标限值（JSON格式存储）
    # 格式：[
    #   {"indicator": "pH", "min_limit": 6, "max_limit": 9, "unit": "无量纲", "operator": "between"},
    #   {"indicator": "COD", "max_limit": 20, "unit": "mg/L", "operator": "<="},
    #   {"indicator": "氨氮", "max_limit": 1.0, "unit": "mg/L", "operator": "<="}
    # ]
    limits = Column(Text, nullable=False, comment='指标限值配置')
    
    description = Column(String(500), comment='标准描述')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f"<Standard(standard_name='{self.standard_name}')>"
