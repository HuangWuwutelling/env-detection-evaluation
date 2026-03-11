"""
样品数据模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .database import Base


class Sample(Base):
    """样品表"""
    __tablename__ = 'samples'

    id = Column(Integer, primary_key=True, index=True)
    sample_no = Column(String(50), unique=True, index=True, nullable=False, comment='样品编号')
    sample_name = Column(String(100), nullable=False, comment='样品名称')
    sample_type = Column(String(50), comment='样品类型')
    source = Column(String(200), comment='样品来源')
    collection_date = Column(DateTime, comment='采样日期')
    detection_date = Column(DateTime, default=datetime.now, comment='检测日期')
    
    # 检测指标数据（JSON格式存储）
    # 格式：{"pH": 7.2, "COD": 45.5, "氨氮": 0.8}
    detection_data = Column(Text, comment='检测指标数据')
    
    remark = Column(String(500), comment='备注')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f"<Sample(sample_no='{self.sample_no}', sample_name='{self.sample_name}')>"
