"""
Triple Pathway System - 三重命途交互
智识（Erudition）、记忆（Remembrance）、毁灭（Nihility）
"""

import torch
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PathwayState:
    """命途状态"""
    name: str
    influence: float = 0.33  # 影响力（三命途初始均衡）
    entropy_effect: float = 0.0  # 对熵的影响


class TriplePathway:
    """
    三重命途系统
    管理智识、记忆、毁灭三种命途的交互与平衡
    """
    def __init__(self):
        self.pathways = {
            "erudition": PathwayState("智识", influence=0.4, entropy_effect=-0.05),  # 熵减
            "remembrance": PathwayState("记忆", influence=0.3, entropy_effect=0.0),   # 稳定
            "nihility": PathwayState("毁灭", influence=0.3, entropy_effect=0.05)      # 熵增
        }

        # 命途冲突历史
        self.conflict_history = []

        # 当前主导命途
        self.dominant_pathway = "erudition"

    def compute_influence(self, 
                         world_entropy: float,
                         loop_count: int,
                         destruction_equation: float,
                         special_entities_present: List[str] = None) -> Dict[str, float]:
        """
        计算各命途的当前影响力

        规则：
        - 智识：主导算法演算，熵越高影响力越低
        - 毁灭：随循环次数和毁灭方程值增长
        - 记忆：在永劫回归阶段增强
        """
        if special_entities_present is None:
            special_entities_present = []

        # 智识影响力：与熵负相关
        erudition_inf = max(0.1, 0.5 - world_entropy * 0.3)

        # 毁灭影响力：与循环次数和毁灭方程正相关
        loop_factor = min(loop_count / 1000000, 0.3)
        destruction_inf = 0.3 + loop_factor + destruction_equation * 0.2
        destruction_inf = min(0.6, destruction_inf)

        # 记忆影响力：基础值 + 特殊实体加成
        remembrance_inf = 0.3
        if "PhiLia093" in special_entities_present:
            remembrance_inf += 0.2  # 昔涟增强记忆命途
        if "Trailblazer" in special_entities_present:
            remembrance_inf += 0.1  # 开拓者带来外部记忆

        # 归一化
        total = erudition_inf + destruction_inf + remembrance_inf

        influences = {
            "erudition": erudition_inf / total,
            "nihility": destruction_inf / total,
            "remembrance": remembrance_inf / total
        }

        # 更新状态
        for key, val in influences.items():
            self.pathways[key].influence = val

        # 确定主导命途
        self.dominant_pathway = max(influences, key=influences.get)

        return influences

    def apply_pathway_effects(self, 
                             factor_network,
                             world_state: Dict,
                             influences: Dict[str, float]) -> Dict:
        """
        应用命途效果

        Returns:
            效果报告
        """
        effects = {}

        # 智识效果：算法优化，降低系统熵
        if "erudition" in influences:
            erudition_power = influences["erudition"]
            effects["erudition"] = {
                "entropy_reduction": erudition_power * 0.02,
                "algorithm_refinement": True,
                "description": "博识尊的算法优化了演算效率"
            }

        # 毁灭效果：增加金血、加速熵增
        if "nihility" in influences:
            destruction_power = influences["nihility"]
            effects["nihility"] = {
                "entropy_boost": destruction_power * 0.03,
                "golden_blood_spread": destruction_power * 0.1,
                "description": "纳努克的瞥视加速了世界的毁灭"
            }

        # 记忆效果：数据持久化、历史继承
        if "remembrance" in influences:
            remembrance_power = influences["remembrance"]
            effects["remembrance"] = {
                "memory_persistence": remembrance_power,
                "history_retention": remembrance_power * 0.5,
                "description": "浮黎的记忆保存了文明的痕迹"
            }

        # 记录冲突
        self.conflict_history.append({
            "dominant": self.dominant_pathway,
            "influences": influences.copy(),
            "effects": effects
        })

        return effects

    def check_pathway_resonance(self, 
                               agent_factors: List[str],
                               titan_factors: List[str]) -> Optional[str]:
        """
        检查命途共鸣
        当黄金裔与泰坦的因子匹配时触发共鸣
        """
        # 简单匹配检查
        matches = set(agent_factors) & set(titan_factors)
        if len(matches) >= 2:
            return "strong_resonance"
        elif len(matches) == 1:
            return "weak_resonance"
        return None

    def get_pathway_balance(self) -> Dict:
        """获取命途平衡状态"""
        return {
            "dominant": self.dominant_pathway,
            "influences": {k: v.influence for k, v in self.pathways.items()},
            "conflict_count": len(self.conflict_history),
            "is_balanced": all(0.2 < v.influence < 0.5 for v in self.pathways.values())
        }

    def external_intervention(self, pathway: str, strength: float):
        """
        外部干预（如星穹列车的介入）
        暂时改变命途平衡
        """
        if pathway in self.pathways:
            self.pathways[pathway].influence += strength

            # 重新归一化
            total = sum(p.influence for p in self.pathways.values())
            for p in self.pathways.values():
                p.influence /= total
