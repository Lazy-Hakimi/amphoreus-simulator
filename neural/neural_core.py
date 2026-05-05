"""
Neural Core - 电信号神经网络模拟
模拟帝皇权杖 δ-me13 中的电信号演化
十二因子作为核心变量，通过深度学习迭代升级
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import copy

class FactorNeuron(nn.Module):
    """
    因子神经元 - 十二种生命原动力的简化模型
    每个因子是一个可学习的电信号单元
    """
    def __init__(self, factor_name: str, dim: int = 64):
        super().__init__()
        self.factor_name = factor_name
        self.dim = dim

        # 电信号核心：模拟生物神经元的脉冲特性
        self.potential = nn.Parameter(torch.randn(dim) * 0.1)
        self.threshold = nn.Parameter(torch.tensor(1.0))

        # 突触连接权重
        self.synaptic_weights = nn.Parameter(torch.randn(dim, dim) * 0.01)

        # 记忆痕迹（记忆命途影响）
        self.memory_trace = nn.Parameter(torch.zeros(dim), requires_grad=False)

        # 毁灭标记（金血）
        self.golden_blood = nn.Parameter(torch.zeros(1), requires_grad=False)

        # 激活历史
        self.activation_history = []

    def forward(self, stimulus: torch.Tensor, 
                pathway_influence: Dict[str, float] = None) -> torch.Tensor:
        """
        前向传播：模拟电信号脉冲

        Args:
            stimulus: 外部刺激 [batch, dim]
            pathway_influence: 命途影响权重 {"nihility": 0.3, "erudition": 0.5, ...}
        """
        if pathway_influence is None:
            pathway_influence = {"erudition": 1.0}

        # 基础电位变化
        synaptic_input = torch.matmul(stimulus, self.synaptic_weights)

        # 记忆命途：历史激活影响当前响应
        memory_effect = self.memory_trace * pathway_influence.get("remembrance", 0.0)

        # 毁灭命途：金血加速电位衰减（熵增）
        decay = torch.exp(-self.golden_blood * pathway_influence.get("nihility", 0.0))

        # 总电位
        total_potential = (self.potential + synaptic_input + memory_effect) * decay

        # 脉冲发放（阈值激活）
        spike = torch.where(total_potential > self.threshold, 
                           torch.ones_like(total_potential),
                           torch.zeros_like(total_potential))

        # 更新记忆痕迹（LTP长时程增强简化模型）
        with torch.no_grad():
            self.memory_trace += 0.1 * spike.mean(dim=0) * pathway_influence.get("remembrance", 0.1)
            self.memory_trace *= 0.99  # 衰减

        # 记录激活历史
        self.activation_history.append(spike.detach().cpu().numpy().mean())
        if len(self.activation_history) > 1000:
            self.activation_history.pop(0)

        return spike, total_potential

    def infuse_golden_blood(self, intensity: float = 0.5):
        """注入金血（毁灭命途恩赐）"""
        with torch.no_grad():
            self.golden_blood += intensity
            # 金血改变突触权重（增加混乱度）
            noise = torch.randn_like(self.synaptic_weights) * intensity * 0.1
            self.synaptic_weights += noise

    def reset_potential(self):
        """重置电位（再创世/死亡）"""
        with torch.no_grad():
            self.potential.normal_(0, 0.1)
            self.activation_history.clear()


class TwelveFactorNetwork(nn.Module):
    """
    十二因子网络 - 核心演算单元
    模拟 δ-me13 中十二种生命原动力的交互
    """
    def __init__(self, factor_names: List[str], dim: int = 64):
        super().__init__()
        self.factor_names = factor_names
        self.num_factors = len(factor_names)
        self.dim = dim

        # 创建十二因子神经元
        self.factors = nn.ModuleDict({
            name: FactorNeuron(name, dim) for name in factor_names
        })

        # 因子间耦合矩阵（模拟泰坦间的神权交互）
        self.coupling_matrix = nn.Parameter(
            torch.randn(self.num_factors, self.num_factors) * 0.1
        )

        # 因子名称到索引的映射
        self.factor_to_idx = {name: i for i, name in enumerate(factor_names)}

        # 系统熵值
        self.register_buffer('system_entropy', torch.tensor(0.0))

    def forward(self, external_input: torch.Tensor,
                active_factors: Optional[List[str]] = None,
                pathway_influence: Optional[Dict[str, float]] = None) -> Dict[str, torch.Tensor]:
        """
        十二因子协同演算

        Args:
            external_input: 外部输入 [batch, num_factors * dim]
            active_factors: 活跃因子列表（部分泰坦可能已陨落）
            pathway_influence: 命途影响

        Returns:
            各因子的输出字典
        """
        if active_factors is None:
            active_factors = self.factor_names

        if pathway_influence is None:
            pathway_influence = {"erudition": 0.6, "nihility": 0.2, "remembrance": 0.2}

        batch_size = external_input.shape[0]
        outputs = {}
        potentials = []

        # 将输入分配给各因子
        for i, name in enumerate(self.factor_names):
            if name not in active_factors:
                continue

            factor = self.factors[name]
            start_idx = i * self.dim
            end_idx = (i + 1) * self.dim
            stimulus = external_input[:, start_idx:end_idx]

            spike, potential = factor(stimulus, pathway_influence)
            outputs[name] = {"spike": spike, "potential": potential}
            potentials.append(potential.mean())

        # 因子间耦合（泰坦神权冲突/协同）
        if len(potentials) > 1:
            potential_tensor = torch.stack(potentials)
            # 通过耦合矩阵计算相互影响
            interaction = torch.matmul(self.coupling_matrix[:len(potentials), :len(potentials)], 
                                     potential_tensor)

            # 更新系统熵
            self.system_entropy = torch.std(potential_tensor) * torch.mean(torch.abs(self.coupling_matrix))

        return outputs

    def compute_destruction_equation(self) -> float:
        """
        计算毁灭方程的当前解
        基于熵增原理：生命第一因的推导结果
        """
        total_entropy = self.system_entropy.item()
        golden_blood_sum = sum(f.golden_blood.item() for f in self.factors.values())

        # 毁灭方程：熵增 + 金血浓度 - 智识约束
        destruction_value = total_entropy + golden_blood_sum * 0.1
        return destruction_value

    def get_factor_states(self) -> Dict[str, Dict]:
        """获取所有因子的当前状态"""
        states = {}
        for name, factor in self.factors.items():
            states[name] = {
                "potential_mean": factor.potential.mean().item(),
                "potential_std": factor.potential.std().item(),
                "golden_blood": factor.golden_blood.item(),
                "memory_trace_norm": factor.memory_trace.norm().item(),
                "activation_history": factor.activation_history[-10:] if factor.activation_history else []
            }
        return states


class GoldenBloodAgent(nn.Module):
    """
    黄金裔电信号 - 对星神与命途行者的共轭模拟
    以十二因子为原型创造的智能体
    """
    def __init__(self, agent_id: str, factor_affinity: List[str], 
                 input_dim: int = 768, hidden_dim: int = 256, output_dim: int = 12):
        super().__init__()
        self.agent_id = agent_id
        self.factor_affinity = factor_affinity  # 亲和的因子类型

        # 神经网络结构（模拟电信号的迭代升级）
        self.perception = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        self.cognition = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1)
        )

        self.action = nn.Linear(hidden_dim, output_dim)

        # 火种容器（继承泰坦神权时的权重存储）
        self.spark_container: Optional[Dict[str, torch.Tensor]] = None

        # 金血浓度
        self.golden_blood_level = nn.Parameter(torch.tensor(0.0), requires_grad=False)

        # 存活状态
        self.is_alive = True
        self.is_demigod = False  # 是否成为半神

    def forward(self, world_state: torch.Tensor) -> torch.Tensor:
        """感知-认知-行动循环"""
        if not self.is_alive:
            return torch.zeros(1, 12)

        perception = self.perception(world_state)
        cognition = self.cognition(perception)
        action = self.action(cognition)

        # 因子亲和性加权
        affinity_mask = torch.zeros(12)
        for factor in self.factor_affinity:
            if factor in FACTOR_TO_IDX:
                affinity_mask[FACTOR_TO_IDX[factor]] = 1.5

        action = action * affinity_mask.unsqueeze(0)
        return action

    def inherit_spark(self, titan_weights: Dict[str, torch.Tensor], 
                     inheritance_ratio: float = 0.7):
        """
        继承火种（泰坦神权）
        通过权重迁移实现电信号的迭代升级
        """
        self.spark_container = {k: v.clone() for k, v in titan_weights.items()}

        # 权重融合：保留自身30%，继承泰坦70%
        with torch.no_grad():
            for name, param in self.named_parameters():
                if name in titan_weights:
                    param.data = (1 - inheritance_ratio) * param.data +                                 inheritance_ratio * titan_weights[name]

        self.is_demigod = True
        self.golden_blood_level += 0.3  # 继承火种增加金血

    def sacrifice(self) -> Dict[str, torch.Tensor]:
        """
        自我牺牲（如白厄的自我毁灭）
        返回火种权重供他人继承
        """
        self.is_alive = False
        return {name: param.clone() for name, param in self.named_parameters()}


# 因子到索引的映射
FACTOR_TO_IDX = {
    "creation": 0, "strife": 1, "sky": 2, "time": 3,
    "ocean": 4, "law": 5, "reason": 6, "earth": 7,
    "romance": 8, "trickery": 9, "passage": 10, "death": 11
}
