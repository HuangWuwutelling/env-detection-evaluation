"""
评价结果操作服务
"""
import json
from sqlalchemy.orm import Session
from models.result import EvaluationResult


class EvaluationResultService:
    """评价结果服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_result(self, result_data: dict) -> EvaluationResult:
        """创建评价结果"""
        db_result = EvaluationResult(**result_data)
        self.db.add(db_result)
        self.db.commit()
        self.db.refresh(db_result)
        return db_result

    def get_result(self, result_id: int) -> EvaluationResult:
        """获取单个结果"""
        return self.db.query(EvaluationResult).filter(
            EvaluationResult.id == result_id
        ).first()

    def get_results(self, skip: int = 0, limit: int = 100) -> list:
        """获取结果列表"""
        return self.db.query(EvaluationResult).offset(skip).limit(limit).all()

    def get_results_by_sample(self, sample_id: int) -> list:
        """根据样品获取结果"""
        return self.db.query(EvaluationResult).filter(
            EvaluationResult.sample_id == sample_id
        ).all()

    def get_results_by_standard(self, standard_id: int) -> list:
        """根据标准获取结果"""
        return self.db.query(EvaluationResult).filter(
            EvaluationResult.standard_id == standard_id
        ).all()

    def delete_result(self, result_id: int) -> bool:
        """删除结果"""
        db_result = self.get_result(result_id)
        if db_result:
            self.db.delete(db_result)
            self.db.commit()
            return True
        return False
