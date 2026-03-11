# 环境检测数据评价系统

一个基于 Streamlit 的环境检测数据自动化评价系统，支持样品数据管理、评价标准配置、自动评价和结果导出功能。

## 功能特性

✅ **样品管理**
- 手动录入样品信息
- Excel/CSV 批量导入样品数据
- 样品列表查看和搜索

✅ **评价标准管理**
- 自定义评价标准和限值
- 支持多种判定规则（≤、≥、区间）
- 预设常用环境检测标准模板

✅ **数据评价**
- 根据选定标准自动评价
- 单指标和多指标综合评价
- 实时显示评价结果

✅ **评价结果**
- 历史评价记录查询
- 详细评价结果展示
- 导出 Excel 报告

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（可选）
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 2. 运行系统

```bash
cd app
streamlit run main.py
```

系统将在 http://localhost:8501 启动

### 3. 使用流程

1. **配置评价标准** - 在「评价标准」模块添加评价指标和限值
2. **录入样品数据** - 在「样品管理」模块手动录入或批量导入
3. **执行评价** - 在「数据评价」模块选择样品和标准进行评价
4. **查看结果** - 在「评价结果」模块查看和导出评价报告

## 项目结构

```
env-detection-evaluation/
├── app/
│   ├── main.py                    # 主入口
│   ├── models/                    # 数据模型
│   │   ├── database.py           # 数据库配置
│   │   ├── sample.py             # 样品模型
│   │   ├── standard.py           # 标准模型
│   │   └── result.py             # 结果模型
│   ├── services/                  # 业务逻辑层
│   │   ├── sample_service.py     # 样品服务
│   │   ├── standard_service.py   # 标准服务
│   │   ├── result_service.py     # 结果服务
│   │   └── evaluation_engine.py  # 评价引擎
│   ├── pages/                     # 页面模块
│   │   ├── sample_management.py  # 样品管理
│   │   ├── standard_management.py # 标准管理
│   │   ├── evaluation.py         # 数据评价
│   │   └── results.py            # 结果展示
│   └── utils/                     # 工具函数
│       └── file_import.py        # 文件导入工具
├── data/                          # 数据存储目录
├── requirements.txt               # Python 依赖
└── README.md                      # 项目说明
```

## 数据导入模板

批量导入样品时，Excel/CSV 文件应包含以下列：

| 列名 | 必需 | 说明 |
|------|------|------|
| 样品编号 | ✅ | 样品的唯一标识 |
| 样品名称 | ✅ | 样品名称 |
| 样品类型 | ❌ | 如：地表水、废水、大气 |
| 样品来源 | ❌ | 采样地点或来源 |
| 采样日期 | ❌ | 格式：YYYY-MM-DD |
| 检测指标列 | ❌ | 如 pH、COD、氨氮等 |
| 备注 | ❌ | 其他说明信息 |

## 技术栈

- **Python 3.10+**
- **Streamlit** - Web 应用框架
- **SQLAlchemy** - ORM 框架
- **SQLite** - 本地数据库
- **Pandas** - 数据处理
- **Openpyxl** - Excel 文件处理

## 开发日志

- 2026-03-11: 完成系统基础框架和所有核心功能开发
- 持续更新中...

## License

MIT
