"""
数据库迁移脚本 - 添加新字段到 samples 表
"""
import sys
sys.path.insert(0, 'app')

from models.database import engine
from sqlalchemy import text

def migrate_database():
    """执行数据库迁移"""
    print("=" * 60)
    print("开始数据库迁移...")
    print("=" * 60)
    
    # 需要添加的新字段
    new_columns = [
        ('standard_code', 'VARCHAR(100)', '评价标准（GB 编号）'),
        ('land_use_type', 'VARCHAR(100)', '用地类型（土壤专用）'),
        ('agri_sub_type', 'VARCHAR(100)', '农用地细分（水田/果园/其他）'),
        ('ph_range', 'VARCHAR(50)', 'pH 分段（土壤专用）'),
        ('water_class', 'VARCHAR(50)', '水质类别（I 类/II 类/III 类/IV 类/V 类）')
    ]
    
    with engine.connect() as conn:
        for column_name, column_type, comment in new_columns:
            try:
                # 检查列是否已存在
                result = conn.execute(text(f"PRAGMA table_info(samples)"))
                existing_columns = [row[1] for row in result.fetchall()]
                
                if column_name in existing_columns:
                    print(f"✓ 列 '{column_name}' 已存在，跳过")
                    continue
                
                # 添加新列
                sql = f"ALTER TABLE samples ADD COLUMN {column_name} {column_type}"
                conn.execute(text(sql))
                print(f"✓ 成功添加列：{column_name} ({column_type})")
                
            except Exception as e:
                print(f"✗ 添加列 {column_name} 失败：{e}")
        
        conn.commit()
    
    print("=" * 60)
    print("数据库迁移完成！")
    print("=" * 60)
    print("\n新增字段：")
    for column_name, column_type, comment in new_columns:
        print(f"  - {column_name}: {column_type} - {comment}")
    print("\n请重启 Streamlit 应用以使用新功能。")

if __name__ == "__main__":
    migrate_database()
