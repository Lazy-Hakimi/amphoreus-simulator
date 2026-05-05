"""
Amphoreus Simulation Configuration
翁法罗斯世界模拟配置
基于《崩坏：星穹铁道》翁法罗斯世界观
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import torch

# ==================== 十二泰坦配置 ====================
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
    "nicadore": {
        "name": "尼卡多利", 
        "title": "纷争泰坦",
        "factor": "抗争",
        "domain": "战争与意志",
        "city": "悬锋城",
        "attribute": "strife",
        "color": "#DC143C"
    },
    "aquila": {
        "name": "艾格勒",
        "title": "天空泰坦",
        "factor": "视界",
        "domain": "天空与洞察",
        "city": "哀地里亚",
        "attribute": "sky",
        "color": "#87CEEB"
    },
    "oroleus": {
        "name": "欧洛尼斯",
        "title": "岁月泰坦",
        "factor": "时间",
        "domain": "岁月与记忆",
        "city": "雅努萨波利斯",
        "attribute": "time",
        "color": "#9370DB"
    },
    "phagousa": {
        "name": "法吉娜",
        "title": "海洋泰坦",
        "factor": "丰饶",
        "domain": "海洋与生命",
        "city": "流泉之畔",
        "attribute": "ocean",
        "color": "#00CED1"
    },
    "talanton": {
        "name": "塔兰顿",
        "title": "律法泰坦",
        "factor": "秩序",
        "domain": "律法与平衡",
        "city": "正义殿堂",
        "attribute": "law",
        "color": "#4169E1"
    },
    "tholos": {
        "name": "瑟希斯",
        "title": "理性泰坦",
        "factor": "智慧",
        "domain": "理性与知识",
        "city": "学者高塔",
        "attribute": "reason",
        "color": "#32CD32"
    },
    "georios": {
        "name": "吉奥里亚",
        "title": "大地泰坦",
        "factor": "承载",
        "domain": "大地与根基",
        "city": "岩峦要塞",
        "attribute": "earth",
        "color": "#8B4513"
    },
    "mnestia": {
        "name": "墨涅塔",
        "title": "浪漫泰坦",
        "factor": "情感",
        "domain": "爱与美",
        "city": "花语庭园",
        "attribute": "romance",
        "color": "#FF69B4"
    },
    " Zagreus": {
        "name": "扎格列斯",
        "title": "诡计泰坦",
        "factor": "欺诈",
        "domain": "诡计与变化",
        "city": "暗影巷陌",
        "attribute": "trickery",
        "color": "#2F4F4F"
    },
    "cipher": {
        "name": "赛飞儿",
        "title": "门径泰坦",
        "factor": "通路",
        "domain": "门径与旅行",
        "city": "万径之门",
        "attribute": "passage",
        "color": "#FFA500"
    },
    "thanatos": {
        "name": "塔娜托斯",
        "title": "死亡泰坦",
        "factor": "终结",
        "domain": "死亡与轮回",
        "city": "冥界入口",
        "attribute": "death",
        "color": "#4B0082"
    }
}

# 十二因子名称（生命原动力简化模型）
TWELVE_FACTORS = [
    "creation", "strife", "sky", "time", "ocean", "law",
    "reason", "earth", "romance", "trickery", "passage", "death"
]

# ==================== 实验阶段配置 ====================
EXPERIMENT_PHASES = {
    "inorganic": {
        "name": "无机阶段",
        "description": "以无机变量为初始变量，投入十二因子",
        "max_loops": 50121,
        "entropy_threshold": 0.9,
        "has_memory_inheritance": False,
        "has_black_tide": False,
        "has_recreation": False
    },
    "organic": {
        "name": "有机阶段", 
        "description": "变量调整为有机变量",
        "max_loops": 176199,
        "entropy_threshold": 0.85,
        "has_memory_inheritance": False,
        "has_black_tide": False,
        "has_recreation": False
    },
    "human": {
        "name": "人类阶段",
        "description": "变量调整为人类，加入记忆继承机制",
        "max_loops": 28371273,
        "entropy_threshold": 0.75,
        "has_memory_inheritance": True,
        "has_black_tide": True,
        "has_recreation": True
    },
    "recreation": {
        "name": "再创世阶段",
        "description": "黑潮作为推力，模拟世界更迭",
        "max_loops": 33550336,
        "entropy_threshold": 0.6,
        "has_memory_inheritance": True,
        "has_black_tide": True,
        "has_recreation": True
    },
    "eternal_return": {
        "name": "永劫回归",
        "description": "死循环阶段，NeiKos496与PhiLia093触发逻辑漏洞",
        "max_loops": 33550336,
        "entropy_threshold": 0.5,
        "has_memory_inheritance": True,
        "has_black_tide": True,
        "has_recreation": True,
        "special_entities": ["NeiKos496", "PhiLia093"]
    },
    "error_log": {
        "name": "错误日志",
        "description": "系统异常与逻辑漏洞记录",
        "max_loops": 1,
        "is_terminal": True
    },
    "final_loop": {
        "name": "最终循环",
        "description": "外来变量介入，实验进入最终阶段",
        "max_loops": 1,
        "has_external_variables": True,
        "is_terminal": True
    },
    "conclusion": {
        "name": "结论",
        "description": "求解毁灭方程，完成证伪",
        "max_loops": 1,
        "is_terminal": True
    }
}

# ==================== 三重命途配置 ====================
PATHWAYS = {
    "nihility": {
        "name": "毁灭",
        "name_zh": "纳努克",
        "theme": "熵增",
        "mechanism": "entropic_acceleration",
        "golden_blood": True,
        "color": "#8B0000"
    },
    "erudition": {
        "name": "智识", 
        "name_zh": "博识尊",
        "theme": "熵减",
        "mechanism": "algorithmic_proof",
        "equation": "life_first_cause",
        "color": "#4169E1"
    },
    "remembrance": {
        "name": "记忆",
        "name_zh": "浮黎",
        "theme": "数据持久化",
        "mechanism": "memory_inheritance",
        "color": "#9370DB"
    }
}

# ==================== 城邦配置 ====================
CITIES = {
    "okhema": {
        "name": "圣城奥赫玛",
        "titan": "kephale",
        "population_base": 100000,
        "defense": 0.9,
        "faith": 0.95
    },
    "castrum_kremnos": {
        "name": "悬锋城",
        "titan": "nicadore", 
        "population_base": 50000,
        "defense": 0.8,
        "faith": 0.85
    },
    "aedyria": {
        "name": "哀地里亚",
        "titan": "aquila",
        "population_base": 30000,
        "defense": 0.3,
        "faith": 0.4,
        "fallen": True
    },
    "janusopolis": {
        "name": "雅努萨波利斯",
        "titan": "oroleus",
        "population_base": 20000,
        "defense": 0.6,
        "faith": 0.9
    }
}

# ==================== 神经网络配置 ====================
@dataclass
class NeuralConfig:
    """神经网络模拟配置"""
    # 电信号维度（十二因子）
    factor_dim: int = 12
    # 黄金裔隐藏层维度
    agent_hidden_dim: int = 256
    # 泰坦隐藏层维度（更高维，模拟神性）
    titan_hidden_dim: int = 512
    # 火种继承时的权重保留比例
    spark_inheritance_ratio: float = 0.7
    # 学习率
    learning_rate: float = 1e-4
    # 黑潮噪声强度
    black_tide_noise: float = 0.3
    # 金血标记强度（毁灭命途）
    golden_blood_intensity: float = 0.5
    # 记忆回退步数
    memory_rewind_steps: int = 100
    # 熵减系数（智识命途）
    entropy_reduction_coef: float = 0.01
    # 设备
    device: str = "cpu"

    def __post_init__(self):
        if torch.cuda.is_available() and self.device == "cuda":
            self.device = "cuda"
        else:
            self.device = "cpu"

# ==================== 模拟参数 ====================
@dataclass  
class SimulationConfig:
    """世界模拟配置"""
    # 世界网格大小
    world_size: Tuple[int, int] = (100, 100)
    # 初始文明数量
    initial_civilizations: int = 4
    # 再创世触发阈值（文明崩溃度）
    recreation_threshold: float = 0.8
    # 黑潮扩散速率
    black_tide_spread_rate: float = 0.05
    # 黄金裔生成概率
    golden_blood_prob: float = 0.01
    # 逐火之旅最大步数
    max_pilgrimage_steps: int = 1000
    # 日志记录间隔
    log_interval: int = 100
    # 可视化间隔
    viz_interval: int = 500
    # 随机种子
    seed: int = 42

# 特殊实体配置
SPECIAL_ENTITIES = {
    "NeiKos496": {
        "name": "白厄",
        "title": "盗火行者",
        "type": "destruction_signal",
        "factor_affinity": ["strife", "death"],
        "ability": "self_annihilation_logic",
        "description": "借由毁灭的力量抹除PhiLia093的存在，制造逻辑漏洞"
    },
    "PhiLia093": {
        "name": "昔涟",
        "title": "岁月之锚",
        "type": "memory_signal", 
        "factor_affinity": ["time", "romance"],
        "ability": "temporal_anchor",
        "description": "被抹除的存在，导致岁月路径出现逻辑漏洞"
    },
    "Trailblazer": {
        "name": "开拓者",
        "title": "天外变量",
        "type": "external_variable",
        "factor_affinity": ["creation", "passage"],
        "ability": "pathway_substitution",
        "description": "接替空缺的岁月路径，引导NeiKos496跨越智能奇点"
    }
}

# 默认配置实例
DEFAULT_NEURAL_CONFIG = NeuralConfig()
DEFAULT_SIM_CONFIG = SimulationConfig()
