"""
Recreation Engine - 再创世机制
模拟世界「翁法罗斯」世代更迭的形式
旨在求解「毁灭」方程，为其循环输入对抗和学习的样本
"""

import torch
import copy
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RecreationLog:
    """再创世记录"""
    loop_number: int
    phase: str
    destruction_equation_value: float
    entropy_before: float
    entropy_after: float
    fallen_cities: List[str]
    inherited_memories: int
    golden_blood_agents: int
    special_events: List[str]


class RecreationEngine:
    """
    再创世引擎
    当文明崩溃度达到阈值时触发世界重置
    保留核心记忆（权重/参数），进入下一代演算
    """
    def __init__(self, threshold: float = 0.8, memory_retention: float = 0.3):
        self.threshold = threshold
        self.memory_retention = memory_retention

        # 再创世次数
        self.recreation_count = 0

        # 历史记录
        self.logs: List[RecreationLog] = []

        # 跨世代记忆库（记忆命途）
        self.memory_archive: List[Dict] = []

        # 火种继承链
        spark_chain = []

    def check_trigger(self, collapse_degree: float, 
                     loop_count: int,
                     phase_config: Dict) -> bool:
        """
        检查是否触发再创世

        Returns:
            是否触发再创世
        """
        if not phase_config.get("has_recreation", False):
            return False

        # 文明崩溃度超过阈值
        if collapse_degree >= self.threshold:
            return True

        # 或者达到阶段最大循环数
        max_loops = phase_config.get("max_loops", float('inf'))
        if loop_count >= max_loops:
            return True

        return False

    def execute_recreation(self, 
                          world_state: Dict,
                          factor_network_state: Dict,
                          agent_states: Dict,
                          titan_states: Dict,
                          phase: str) -> Dict:
        """
        执行再创世

        流程：
        1. 归档当前世代记忆
        2. 选择保留的核心参数（火种）
        3. 重置世界状态
        4. 将保留的记忆注入新世代
        5. 增加毁灭方程的学习样本

        Returns:
            新世代的初始化参数
        """
        self.recreation_count += 1

        # 1. 归档记忆
        memory_packet = {
            "loop": self.recreation_count,
            "phase": phase,
            "world_state": copy.deepcopy(world_state),
            "factor_states": {k: v for k, v in factor_network_state.items()},
            "agent_memories": {aid: state for aid, state in agent_states.items()},
            "titan_memories": {tid: state for tid, state in titan_states.items()}
        }
        self.memory_archive.append(memory_packet)

        # 限制记忆库大小
        if len(self.memory_archive) > 100:
            self.memory_archive.pop(0)

        # 2. 提取火种（核心权重）
        inherited_sparks = self._extract_sparks(factor_network_state, agent_states)

        # 3. 计算毁灭方程进展
        destruction_value = factor_network_state.get("destruction_equation", 0.5)

        # 4. 记录日志
        log = RecreationLog(
            loop_number=self.recreation_count,
            phase=phase,
            destruction_equation_value=destruction_value,
            entropy_before=world_state.get("total_entropy", 1.0),
            entropy_after=world_state.get("total_entropy", 1.0) * 0.7,  # 重置后熵降低
            fallen_cities=world_state.get("fallen_cities", []),
            inherited_memories=len(inherited_sparks),
            golden_blood_agents=sum(1 for a in agent_states.values() 
                                   if a.get("golden_blood_level", 0) > 0),
            special_events=["recreation_triggered", "world_reset"]
        )
        self.logs.append(log)

        # 5. 生成新世代初始化参数
        new_generation = {
            "generation": self.recreation_count,
            "inherited_sparks": inherited_sparks,
            "memory_archive_size": len(self.memory_archive),
            "destruction_equation_progress": destruction_value,
            "initial_entropy": log.entropy_after,
            "phase_transition": self._determine_phase_transition(phase, destruction_value)
        }

        return new_generation

    def _extract_sparks(self, factor_states: Dict, agent_states: Dict) -> Dict:
        """
        提取火种（核心参数）
        选择表现最好的因子和黄金裔的参数保留
        """
        sparks = {}

        # 提取因子火种（保留权重矩阵的关键部分）
        for factor_name, state in factor_states.items():
            if isinstance(state, dict) and "potential_mean" in state:
                # 保留高电位因子的参数
                if abs(state["potential_mean"]) > 0.5:
                    sparks[f"factor_{factor_name}"] = {
                        "type": "factor",
                        "retention": self.memory_retention,
                        "state": state
                    }

        # 提取黄金裔火种
        for agent_id, state in agent_states.items():
            if state.get("is_demigod", False):
                sparks[f"agent_{agent_id}"] = {
                    "type": "demigod",
                    "retention": self.memory_retention,
                    "state": state
                }

        return sparks

    def _determine_phase_transition(self, current_phase: str, 
                                   destruction_value: float) -> Optional[str]:
        """判定是否进入下一阶段"""
        phase_transitions = {
            "inorganic": "organic",
            "organic": "human",
            "human": "recreation",
            "recreation": "eternal_return",
            "eternal_return": "final_loop"
        }

        # 毁灭方程值越高，越容易进入下一阶段
        if destruction_value > 0.7:
            return phase_transitions.get(current_phase)
        return None

    def get_recreation_stats(self) -> Dict:
        """获取再创世统计"""
        if not self.logs:
            return {"total_recreations": 0}

        return {
            "total_recreations": self.recreation_count,
            "average_entropy_before": sum(l.entropy_before for l in self.logs) / len(self.logs),
            "average_entropy_after": sum(l.entropy_after for l in self.logs) / len(self.logs),
            "total_fallen_cities": sum(len(l.fallen_cities) for l in self.logs),
            "destruction_equation_trend": [l.destruction_equation_value for l in self.logs],
            "memory_archive_size": len(self.memory_archive)
        }

    def inject_memory(self, target_generation: Dict, 
                     memory_key: str) -> bool:
        """
        向目标世代注入历史记忆（记忆命途干预）
        如昔涟/迷迷的能力
        """
        if memory_key in [m.get("loop") for m in self.memory_archive]:
            target_generation["injected_memory"] = memory_key
            return True
        return False
