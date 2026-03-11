"""
评价标准操作服务
"""
import json
from sqlalchemy.orm import Session
from models.standard import Standard


class StandardService:
    """评价标准服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_standard(self, standard_data: dict) -> Standard:
        """创建评价标准"""
        db_standard = Standard(**standard_data)
        self.db.add(db_standard)
        self.db.commit()
        self.db.refresh(db_standard)
        return db_standard

    def get_standard(self, standard_id: int) -> Standard:
        """获取单个标准"""
        return self.db.query(Standard).filter(Standard.id == standard_id).first()

    def get_standards(self, skip: int = 0, limit: int = 100) -> list:
        """获取标准列表"""
        return self.db.query(Standard).offset(skip).limit(limit).all()

    def update_standard(self, standard_id: int, update_data: dict) -> Standard:
        """更新标准"""
        db_standard = self.get_standard(standard_id)
        if db_standard:
            for key, value in update_data.items():
                setattr(db_standard, key, value)
            self.db.commit()
            self.db.refresh(db_standard)
        return db_standard

    def delete_standard(self, standard_id: int) -> bool:
        """删除标准"""
        db_standard = self.get_standard(standard_id)
        if db_standard:
            self.db.delete(db_standard)
            self.db.commit()
            return True
        return False

    def get_standards_by_type(self, standard_type: str) -> list:
        """根据类型获取标准"""
        return self.db.query(Standard).filter(
            Standard.standard_type == standard_type
        ).all()
