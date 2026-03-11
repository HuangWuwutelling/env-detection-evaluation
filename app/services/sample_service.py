"""
样品数据操作服务
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from models.sample import Sample


class SampleService:
    """样品服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_sample(self, sample_data: dict) -> Sample:
        """创建样品"""
        db_sample = Sample(**sample_data)
        self.db.add(db_sample)
        self.db.commit()
        self.db.refresh(db_sample)
        return db_sample

    def get_sample(self, sample_id: int) -> Sample:
        """获取单个样品"""
        return self.db.query(Sample).filter(Sample.id == sample_id).first()

    def get_sample_by_no(self, sample_no: str) -> Sample:
        """根据编号获取样品"""
        return self.db.query(Sample).filter(Sample.sample_no == sample_no).first()

    def get_samples(self, skip: int = 0, limit: int = 100) -> list:
        """获取样品列表"""
        return self.db.query(Sample).offset(skip).limit(limit).all()

    def update_sample(self, sample_id: int, update_data: dict) -> Sample:
        """更新样品"""
        db_sample = self.get_sample(sample_id)
        if db_sample:
            for key, value in update_data.items():
                setattr(db_sample, key, value)
            self.db.commit()
            self.db.refresh(db_sample)
        return db_sample

    def delete_sample(self, sample_id: int) -> bool:
        """删除样品"""
        db_sample = self.get_sample(sample_id)
        if db_sample:
            self.db.delete(db_sample)
            self.db.commit()
            return True
        return False

    def batch_create_samples(self, samples_data: list) -> list:
        """批量创建样品"""
        created_samples = []
        for data in samples_data:
            try:
                sample = self.create_sample(data)
                created_samples.append(sample)
            except Exception as e:
                print(f"创建样品失败：{data.get('sample_no')}, 错误：{e}")
        return created_samples

    def search_samples(self, keyword: str) -> list:
        """搜索样品"""
        return self.db.query(Sample).filter(
            (Sample.sample_no.contains(keyword)) | 
            (Sample.sample_name.contains(keyword))
        ).all()
