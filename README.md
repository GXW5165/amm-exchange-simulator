# AMM Exchange Simulator

## 📌 项目简介

本项目是一个基于 **Python** 实现的 **AMM（Automated Market Maker）交易所仿真系统**，用于模拟恒定乘积模型（x · y = k）下的交易机制、流动性管理过程以及相关风险指标。

系统采用 **离散事件驱动仿真（Discrete Event Simulation）** 的方式，支持交易、流动性添加与移除、手续费分配等行为，并输出滑点、无常损失、LP收益等关键分析指标。

本项目为课程设计项目，重点在于：

* AMM数学模型的工程实现
* 软件工程结构设计（分层架构）
* 仿真系统构建与实验分析

📖 设计依据：概要设计说明书 

---

## 🎯 项目目标

* 实现恒定乘积 AMM 核心逻辑
* 构建离散事件仿真引擎
* 支持多场景仿真（基础 / 冲击 / 对比）
* 输出关键指标（滑点 / 无常损失 / 收益）
* 提供 CLI 交互与可视化分析能力

---

## 🚀 核心功能

### ✅ P0（必须实现）

* 恒定乘积模型交易（x · y = k）
* Token A / Token B 双向兑换
* 手续费计算与累计分配
* 流动性添加与移除（LP机制）
* 滑点计算
* 无常损失（Impermanent Loss）计算
* 离散事件驱动仿真
* CLI命令行交互系统
* 仿真日志记录（CSV）

---

### ⚡ P1（增强功能）

* 数据可视化（价格 / 滑点 / 收益曲线）
* 多用户仿真
* 极端场景模拟（大额冲击）
* 多参数对比实验
* 单元测试支持（pytest）

---

### 🌟 P2（扩展功能）

* Web界面（Streamlit / React）
* 套利行为模拟
* 历史数据回测
* 多AMM模型对比

---

## 🧠 系统架构设计

系统采用 **分层架构（Layered Architecture）**：

```
UI Layer (CLI / Web)
        ↓
Simulation Layer (事件调度)
        ↓
Core Business Layer (AMM逻辑)
        ↓
Support Layer (数据 / 日志 / 可视化)
```

### 📦 模块划分

* **核心业务层**

  * AMMEngine（交易逻辑）
  * Pool（资金池状态）
  * LiquidityManager（流动性管理）

* **仿真控制层**

  * Simulator（仿真流程）
  * Event（事件模型）

* **指标计算层**

  * 滑点计算
  * 无常损失计算
  * 收益统计

* **支撑层**

  * 数据管理（日志 / 配置 / 导出）
  * 可视化（图表生成）

* **界面层**

  * CLI交互
  * Web扩展（可选）

---

## 📂 项目结构（推荐）

```
amm-exchange-simulator/
│
├── src/
│   ├── core/                 # 核心业务逻辑
│   │   ├── pool.py
│   │   ├── amm_engine.py
│   │   └── liquidity.py
│   │
│   ├── simulation/           # 仿真引擎
│   │   ├── simulator.py
│   │   ├── event.py
│   │   └── scheduler.py
│   │
│   ├── metrics/              # 指标计算
│   │   ├── slippage.py
│   │   └── impermanent_loss.py
│   │
│   ├── data/                 # 数据管理
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── exporter.py
│   │
│   ├── visualization/        # 可视化模块
│   │   └── plotter.py
│   │
│   ├── cli/                  # 命令行接口
│   │   └── main.py
│
├── config/                   # 配置文件
│   └── default.yaml
│
├── data/                     # 输出数据
│   ├── logs/
│   └── results/
│
├── tests/                    # 单元测试
│
├── requirements.txt
├── main.py                   # 程序入口
└── README.md
```

---

## ⚙️ 环境要求

* Python ≥ 3.10

---

## 📦 依赖安装

```bash
pip install -r requirements.txt
```

推荐依赖：

* numpy
* pandas
* matplotlib / plotly
* pyyaml
* pytest

---

## ▶️ 运行方式

### 方式1：直接运行

```bash
python main.py
```

---

### 方式2：指定配置文件

```bash
python main.py --config config/default.yaml
```

---

## 📊 输出内容

运行后系统将生成：

* 📄 CSV日志文件（交易 / LP操作）
* 📈 统计指标（滑点 / 收益 / IL）
* 📉 可视化图表（价格曲线等）

---

## 🧪 示例功能

* 单次交易模拟
* 批量事件仿真
* 极端市场冲击测试
* 参数对比实验

---

## 📐 核心数学模型

### 恒定乘积模型

```
x · y = k
```

---

### 交易公式

```
dx' = dx(1 - f)
dy = y - k / (x + dx')
```

---

### 滑点

```
slippage = (P_theory - P_actual) / P_theory
```

---

### 无常损失

```
IL(r) = 2√r / (1 + r) - 1
```

---

## 📜 设计原则

* 高内聚、低耦合
* 模块化设计
* 分层架构
* 信息隐藏
* 可扩展性与可维护性优先

---

## 🧩 后续扩展方向

* 多池系统（Multi Pool）
* 套利机制模拟
* Web前端交互
* 实盘数据回测
* 不同AMM模型对比（如恒定均值）

---

## 👥 项目成员

* 黄誉萱
* 关翔文
* 柏昕云
* 戴铭隽

---

## 📚 项目用途

本项目仅用于：

* 课程设计
* AMM机制学习
* 仿真实验分析

不用于任何实际金融交易或商业用途。

---

## 📄 License

MIT License（或课程要求指定License）
