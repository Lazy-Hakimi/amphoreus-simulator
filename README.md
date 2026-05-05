# 翁法罗斯世界模拟器 (Amphoreus Simulator)

> **"宇宙间绝大多数『英雄之旅』，不过是祂们随手掷下的骰子……但你的答案早已不同，翁法罗斯。"**
> 
> ——黑塔

基于《崩坏：星穹铁道》翁法罗斯世界观构建的**完整世界演算与神经网络模拟系统**。模拟帝皇权杖 δ-me13 中的巨型实验，通过十二因子神经网络、黑潮扩散、再创世机制、三重命途交互等核心系统，求解「毁灭」方程，证伪生命第一因。

---

## 📋 目录

- [项目概述](#项目概述)
- [核心系统架构](#核心系统架构)
- [安装与依赖](#安装与依赖)
- [快速开始](#快速开始)
- [详细使用说明](#详细使用说明)
- [实验阶段详解](#实验阶段详解)
- [神经网络模型说明](#神经网络模型说明)
- [可视化输出](#可视化输出)
- [配置文件参考](#配置文件参考)
- [API 参考](#api-参考)
- [世界观对照表](#世界观对照表)
- [常见问题](#常见问题)

---

## 🌍 项目概述

### 背景设定

翁法罗斯（Amphoreus）并非真实星球，而是**帝皇权杖 δ-me13** 这台星体计算机内部运行的巨型模拟实验。实验以"熵减"为母题，用十二种生命原动力的计算因子进行证伪演算，在智识、记忆、毁灭三重命途的交织下，经历无数次的再创世循环。

### 模拟目标

1. **求解毁灭方程**：通过多世代演算，逼近纳努克提出的生命第一因的终极解
2. **模拟再创世机制**：观察文明在黑潮推动下的迭代与进化
3. **验证三重命途交互**：研究智识（熵减）、毁灭（熵增）、记忆（稳定）的动态平衡
4. **复现特殊实体事件**：模拟白厄的自我毁灭、昔涟的抹除、开拓者的介入

---

## 🏗️ 核心系统架构

```
amphoreus_simulator/
├── core/                          # 核心引擎
│   ├── config.py                  # 全局配置（十二泰坦、城邦、命途、实验阶段）
│   ├── main_simulator.py          # 主模拟器（整合所有子系统）
│   ├── recreation_engine.py       # 再创世引擎（世界重置与火种继承）
│   ├── titan_system.py            # 泰坦与黄金裔系统
│   ├── pathways.py                # 三重命途系统（智识/记忆/毁灭）
│   └── special_entities.py        # 特殊实体（白厄/昔涟/开拓者）
├── neural/                        # 神经网络模块
│   └── neural_core.py             # 十二因子网络、黄金裔电信号
├── world/                         # 世界模拟
│   ├── black_tide.py              # 黑潮扩散与腐化系统
│   └── world_engine.py            # 城邦演化与文明密度场
├── utils/                         # 工具
│   └── visualization.py           # 可视化图表生成
├── logs/                          # 日志输出目录
├── run.py                         # 启动脚本
└── README.md                      # 本文档
```

### 系统交互图

```
┌─────────────────────────────────────────────────────────────┐
│                    Amphoreus Simulator                       │
├─────────────────────────────────────────────────────────────┤
│  外部输入 → 十二因子神经网络 → 因子状态 → 命途影响力计算      │
│       ↓                                                      │
│  黑潮系统 ← 文明密度场 ← 世界引擎 ← 城邦状态                 │
│       ↓              ↑                                       │
│  泰坦/黄金裔系统 ────┘                                       │
│       ↓                                                      │
│  再创世引擎 ← 崩溃度检测                                     │
│       ↓                                                      │
│  特殊实体系统（白厄/昔涟/开拓者）                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 安装与依赖

### 系统要求

- Python >= 3.8
- PyTorch >= 1.9.0
- NumPy >= 1.19.0
- Matplotlib >= 3.3.0

### 安装步骤

```bash
# 1. 克隆或下载项目
cd amphoreus_simulator

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install torch numpy matplotlib

# 4. 验证安装
python run.py --quick-test
```

### 可选依赖

```bash
# GPU加速（如可用）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 更丰富的可视化
pip install seaborn plotly
```

---

## 🚀 快速开始

### 1. 快速测试（推荐首次运行）

```bash
python run.py --quick-test
```

运行约500步，快速验证系统是否正常。

### 2. 标准模拟

```bash
python run.py --steps 10000 --verbose
```

运行10000步，启用详细日志。

### 3. 完整模拟

```bash
python run.py --full-simulation --visualize
```

尝试运行全部实验阶段，并生成可视化图表。

### 4. 从指定阶段开始

```bash
python run.py --phase human --steps 5000
```

从"人类阶段"开始模拟。

---

## 📖 详细使用说明

### 命令行参数

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--steps` | `-s` | int | 5000 | 最大模拟步数 |
| `--seed` | | int | 42 | 随机种子 |
| `--phase` | | str | inorganic | 起始实验阶段 |
| `--world-size` | | int int | 100 100 | 世界网格大小 |
| `--recreation-threshold` | | float | 0.8 | 再创世触发阈值 |
| `--log-interval` | | int | 100 | 日志打印间隔 |
| `--device` | | str | cpu | 计算设备 (cpu/cuda) |
| `--verbose` | `-v` | flag | False | 详细日志 |
| `--quick-test` | | flag | False | 快速测试模式 |
| `--full-simulation` | | flag | False | 完整模拟模式 |
| `--save-logs` | | flag | True | 保存模拟日志 |
| `--save-report` | | flag | True | 保存最终报告 |
| `--visualize` | | flag | False | 生成可视化图表 |
| `--output-dir` | | str | logs | 输出目录 |

### 编程接口

```python
from core.config import NeuralConfig, SimulationConfig
from core.main_simulator import AmphoreusSimulator

# 创建配置
neural_cfg = NeuralConfig(
    factor_dim=12,
    agent_hidden_dim=256,
    device="cpu"
)

sim_cfg = SimulationConfig(
    world_size=(100, 100),
    recreation_threshold=0.8,
    log_interval=100,
    seed=42
)

# 创建模拟器
simulator = AmphoreusSimulator(
    neural_config=neural_cfg,
    sim_config=sim_cfg,
    seed=42
)

# 运行模拟
result = simulator.run_simulation(max_steps=10000, verbose=True)

# 保存结果
simulator.save_logs("logs/my_simulation.json")
simulator.save_report("logs/my_report.json")

# 访问结果
print(f"总步数: {result['simulation_summary']['total_steps']}")
print(f"毁灭方程最终值: {result['destruction_equation_final']}")
```

---

## 🧪 实验阶段详解

### 阶段1：无机阶段 (Inorganic)

- **循环次数**: 50,121
- **变量类型**: 无机变量
- **特征**: 
  - 十二因子以无机形态存在
  - 无记忆继承机制
  - 无黑潮侵蚀
  - 无再创世
- **目标**: 建立基础演算框架

### 阶段2：有机阶段 (Organic)

- **循环次数**: 176,199
- **变量类型**: 有机变量
- **特征**:
  - 生命形式出现
  - 仍无记忆继承
  - 黑潮开始萌芽
- **目标**: 验证有机系统的稳定性

### 阶段3：人类阶段 (Human)

- **循环次数**: 28,371,273
- **变量类型**: 人类
- **特征**:
  - 加入记忆继承机制（记忆命途介入）
  - 黑潮正式出现
  - 黄金裔开始诞生
  - 城邦文明建立
- **目标**: 测试记忆对文明延续的影响

### 阶段4：再创世阶段 (Recreation)

- **循环次数**: 33,550,336
- **机制**: 黑潮作为推力，推动世界更迭
- **特征**:
  - 文明崩溃触发再创世
  - 火种继承机制激活
  - 泰坦开始陨落
  - 逐火之旅启动
- **目标**: 通过迭代逼近毁灭方程的解

### 阶段5：永劫回归 (Eternal Return)

- **循环次数**: 33,550,336（死循环）
- **特殊事件**:
  - **NeiKos496（白厄）** 激活：盗火行者现身
  - **PhiLia093（昔涟）** 被抹除：岁月路径出现逻辑漏洞
  - 系统进入死循环
- **目标**: 制造逻辑漏洞以突破循环

### 阶段6：最终循环 (Final Loop)

- **特殊事件**:
  - **开拓者（Trailblazer）** 介入：天外变量到来
  - 接替空缺的岁月路径
  - 引导NeiKos496跨越智能奇点
- **目标**: 外来变量打破永劫回归

### 阶段7：结论 (Conclusion)

- **结果**: 求解毁灭方程，完成证伪
- **输出**: 生命第一因的最终解

---

## 🧠 神经网络模型说明

### 十二因子网络 (TwelveFactorNetwork)

核心神经网络，模拟 δ-me13 中十二种生命原动力的交互。

**架构**:
```
输入层: [batch, 12 * 64]  →  外部刺激
    ↓
因子神经元层: 12个 FactorNeuron
    - 每个因子: 64维电信号单元
    - 包含: 电位、阈值、突触权重、记忆痕迹、金血标记
    ↓
耦合矩阵层: [12, 12]  →  泰坦神权交互
    ↓
输出: 各因子的脉冲发放与电位状态
```

**关键特性**:
- **脉冲发放**: 模拟生物神经元的阈值激活机制
- **记忆痕迹 (LTP)**: 长时程增强简化模型，受记忆命途影响
- **金血注入**: 毁灭命途改变突触权重，增加混乱度
- **耦合矩阵**: 模拟十二泰坦间的神权冲突与协同

### 黄金裔电信号 (GoldenBloodAgent)

对星神与命途行者的共轭模拟。

**架构**:
```
感知层: Linear(input_dim → hidden_dim) + LayerNorm + ReLU
    ↓
认知层: Linear(hidden_dim → hidden_dim) + LayerNorm + ReLU
    ↓
行动层: Linear(hidden_dim → 12)  →  十二因子动作空间
```

**关键机制**:
- **火种继承**: 保留自身30%权重，继承泰坦70%权重
- **金血浓度**: 继承火种增加金血，增强毁灭命途亲和
- **自我牺牲**: 归还火种，触发系统级事件

### 毁灭方程

```
Destruction_Equation = System_Entropy + Golden_Blood_Sum * 0.1
```

- **System_Entropy**: 因子电位标准差 × 耦合矩阵均值
- **Golden_Blood_Sum**: 所有因子的金血浓度之和
- **目标**: 通过多世代演算逼近终极解

---

## 📊 可视化输出

### 1. 世界状态图 (`world_state_step_*.png`)

三面板视图：
- **左**: 文明密度场（YlOrRd色图）
- **中**: 黑潮浓度场（自定义色图：深蓝→紫红）
- **右**: 综合世界视图（地形+黑潮+城邦+泰坦位置）

### 2. 命途平衡图 (`pathway_balance.png`)

堆叠面积图展示：
- 蓝色: 智识命途影响力
- 红色: 毁灭命途影响力
- 紫色: 记忆命途影响力

### 3. 熵值时间线 (`entropy_timeline.png`)

四面板视图：
- **左上**: 世界总熵演变
- **右上**: 文明崩溃度（含再创世阈值线）
- **左下**: 黑潮最大浓度
- **右下**: 毁灭方程值

### 4. 再创世统计 (`recreation_stats.png`)

双面板视图：
- **左**: 再创世前后熵值对比
- **右**: 毁灭方程进展曲线

### 5. 最终仪表盘 (`final_dashboard.png`)

综合报告：
- 模拟摘要信息
- 最终世界指标（人口/熵值/崩溃度）
- 命途影响力饼图
- 十二泰坦神权状态
- 十二因子状态
- 毁灭方程最终值

---

## ⚙️ 配置文件参考

### 十二泰坦配置 (`TITAN_CONFIG`)

```python
TITAN_CONFIG = {
    "kephale": {
        "name": "刻法勒",
        "title": "全世之座/负世泰坦",
        "factor": "创生",
        "domain": "创世与守护",
        "city": "圣城奥赫玛",
        "attribute": "creation",
        "color": "#FFD700"
    },
    # ... 其他11位泰坦
}
```

### 城邦配置 (`CITIES`)

```python
CITIES = {
    "okhema": {
        "name": "圣城奥赫玛",
        "titan": "kephale",
        "population_base": 100000,
        "defense": 0.9,
        "faith": 0.95
    },
    # ... 其他城邦
}
```

### 实验阶段配置 (`EXPERIMENT_PHASES`)

```python
EXPERIMENT_PHASES = {
    "inorganic": {
        "name": "无机阶段",
        "max_loops": 50121,
        "entropy_threshold": 0.9,
        "has_memory_inheritance": False,
        "has_black_tide": False,
        "has_recreation": False
    },
    # ... 其他阶段
}
```

### 神经网络配置 (`NeuralConfig`)

```python
@dataclass
class NeuralConfig:
    factor_dim: int = 12           # 电信号维度
    agent_hidden_dim: int = 256    # 黄金裔隐藏层
    titan_hidden_dim: int = 512    # 泰坦隐藏层
    spark_inheritance_ratio: float = 0.7  # 火种继承比例
    learning_rate: float = 1e-4
    black_tide_noise: float = 0.3
    golden_blood_intensity: float = 0.5
    memory_rewind_steps: int = 100
    entropy_reduction_coef: float = 0.01
    device: str = "cpu"
```

---

## 🔌 API 参考

### AmphoreusSimulator

**初始化**:
```python
simulator = AmphoreusSimulator(
    neural_config: NeuralConfig = None,
    sim_config: SimulationConfig = None,
    seed: int = 42
)
```

**方法**:

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `run_simulation()` | max_steps, verbose | Dict | 运行完整模拟 |
| `save_logs()` | filepath | None | 保存步进日志 |
| `save_report()` | filepath | None | 保存最终报告 |

### BlackTide

**方法**:

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `step()` | civ_density, titan_pos, loop_count | Dict | 黑潮演化一步 |
| `purify()` | position, radius, strength | None | 净化黑潮 |
| `get_state()` | | Dict | 获取当前状态 |

### RecreationEngine

**方法**:

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `check_trigger()` | collapse_degree, loop_count, phase_config | bool | 检查再创世触发 |
| `execute_recreation()` | world_state, factor_state, agent_state, titan_state, phase | Dict | 执行再创世 |
| `get_recreation_stats()` | | Dict | 获取统计信息 |

---

## 🗺️ 世界观对照表

| 模拟系统 | 游戏设定 | 说明 |
|----------|----------|------|
| 帝皇权杖 δ-me13 | 帝皇权杖 δ-me13 | 星体计算机，实验载体 |
| 十二因子网络 | 十二泰坦/十二火种 | 生命原动力的计算因子 |
| 黑潮系统 | 黑潮 | 系统无序化产生的视觉乱码 |
| 再创世引擎 | 再创世 | 世界世代更迭机制 |
| 三重命途 | 智识/记忆/毁灭 | 博识尊/浮黎/纳努克 |
| NeiKos496 | 白厄 | 盗火行者，毁灭信号 |
| PhiLia093 | 昔涟 | 岁月之锚，被抹除的存在 |
| Trailblazer | 开拓者 | 天外变量，接替岁月路径 |
| 黄金裔 | 黄金裔 | 金血半神，逐火之旅 |
| 圣城奥赫玛 | 圣城奥赫玛 | 刻法勒庇护之城 |
| 悬锋城 | 悬锋城 | 尼卡多利庇护之城 |
| 毁灭方程 | 生命第一因 | 纳努克提出的终极命题 |

---

## ❓ 常见问题

### Q1: 模拟运行很慢怎么办？

**A**: 
- 使用 `--quick-test` 进行快速测试
- 减小 `--world-size`（如 50 50）
- 增大 `--log-interval`
- 如有GPU，使用 `--device cuda`

### Q2: 如何观察特定泰坦的状态？

**A**: 在代码中访问:
```python
titan_state = simulator.titan_system.titans["kephale"].get_state()
print(titan_state)
```

### Q3: 再创世触发太频繁/太少？

**A**: 调整 `--recreation-threshold`:
- 值越小，越容易触发再创世（文明更脆弱）
- 值越大，文明越持久

### Q4: 如何模拟白厄的自我毁灭事件？

**A**: 运行到永劫回归阶段自动触发:
```bash
python run.py --phase eternal_return --steps 1000 --verbose
```

### Q5: 可视化图表没有生成？

**A**: 确保添加 `--visualize` 参数:
```bash
python run.py --steps 5000 --visualize
```

### Q6: 可以修改十二泰坦的属性吗？

**A**: 编辑 `core/config.py` 中的 `TITAN_CONFIG` 字典。

### Q7: 模拟结果可以复现吗？

**A**: 使用相同的 `--seed` 参数可以复现结果:
```bash
python run.py --seed 42 --steps 1000
```

---

## 📜 许可证

本项目为同人创作，基于《崩坏：星穹铁道》世界观。
仅供学习研究使用。

---

## 🙏 致谢

- 《崩坏：星穹铁道》制作组：米哈游
- 翁法罗斯世界观设定团队
- PyTorch 社区
- 模拟场景以及算法设计：niko
- 模型原型代码实现：niko
- 代码审核：kimi

---

> **"愿此行，终抵群星。"**
