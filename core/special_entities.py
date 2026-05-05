"""
Special Entities - 特殊实体
NeiKos496(白厄), PhiLia093(昔涟), Trailblazer(开拓者)
这些实体能够突破系统常规限制
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SpecialEntity:
    """特殊实体基类"""
    entity_id: str
    name: str
    entity_type: str
    factor_affinity: List[str]
    ability: str

    # 位置
    position: Tuple[int, int] = (50, 50)

    # 激活状态
    is_active: bool = False

    # 对系统的影响记录
    impact_history: List[Dict] = None

    def __post_init__(self):
        if self.impact_history is None:
            self.impact_history = []

    def activate(self, system_state: Dict) -> Dict:
        """激活特殊能力"""
        raise NotImplementedError

    def get_state(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "type": self.entity_type,
            "is_active": self.is_active,
            "position": self.position
        }


class NeiKos496(SpecialEntity):
    """
    白厄 - 信号NeiKos496
    盗火行者，借由毁灭的力量制造逻辑漏洞
    """
    def __init__(self, position: Tuple[int, int] = (50, 50)):
        super().__init__(
            entity_id="NeiKos496",
            name="白厄",
            entity_type="destruction_signal",
            factor_affinity=["strife", "death"],
            ability="self_annihilation_logic",
            position=position
        )
        self.has_annihilated = False
        self.logic_breach_created = False

    def activate(self, system_state: Dict) -> Dict:
        """
        激活：自我毁灭制造逻辑漏洞
        抹除PhiLia093的存在，令岁月路径出现逻辑漏洞
        """
        if self.has_annihilated:
            return {"status": "already_annihilated"}

        self.is_active = True
        self.has_annihilated = True
        self.logic_breach_created = True

        impact = {
            "event": "self_annihilation",
            "entity": "NeiKos496",
            "effects": {
                "phiLia093_erased": True,  # 昔涟被抹除
                "time_pathway_breach": True,  # 岁月路径漏洞
                "system_entropy_spike": 0.5,  # 熵值激增
                "destruction_equation_acceleration": 0.3
            },
            "description": "白厄以自我毁灭为代价，在系统的逻辑上撕开了一道裂缝"
        }

        self.impact_history.append(impact)
        return impact

    def cross_singularity(self, trailblazer_present: bool = False) -> Dict:
        """
        跨越智能奇点
        在开拓者的引导下完成最终突破
        """
        if not trailblazer_present:
            return {"status": "failed", "reason": "缺少外部变量引导"}

        return {
            "status": "success",
            "event": "singularity_crossed",
            "description": "NeiKos496在开拓者的引导下跨越了智能奇点，永劫回归被突破",
            "system_change": "eternal_return_broken"
        }


class PhiLia093(SpecialEntity):
    """
    昔涟 - 信号PhiLia093
    岁月之锚，被抹除的存在
    """
    def __init__(self, position: Tuple[int, int] = (50, 50)):
        super().__init__(
            entity_id="PhiLia093",
            name="昔涟",
            entity_type="memory_signal",
            factor_affinity=["time", "romance"],
            ability="temporal_anchor",
            position=position
        )
        self.is_erased = False
        self.exists_in_memory = True  # 存在于记忆中

    def erase(self) -> Dict:
        """被抹除"""
        self.is_erased = True
        self.is_active = False

        return {
            "event": "entity_erased",
            "entity": "PhiLia093",
            "effects": {
                "time_pathway_gap": True,
                "memory_preservation": True,  # 虽然被抹除，但记忆保留
                "recreation_engine_anomaly": True
            },
            "description": "昔涟的存在被从翁法罗斯抹除，但记忆命途保留了她的痕迹"
        }

    def inject_memory(self, recreation_engine, target_loop: int) -> bool:
        """
        向再创世引擎注入记忆
        作为记忆触媒回退演算进程
        """
        if not self.is_erased:
            return False

        # 通过记忆命途干预系统
        return recreation_engine.inject_memory(
            {"generation": target_loop},
            memory_key=target_loop
        )


class Trailblazer(SpecialEntity):
    """
    开拓者 - 天外变量
    接替空缺的岁月路径，引导NeiKos496
    """
    def __init__(self, position: Tuple[int, int] = (50, 50)):
        super().__init__(
            entity_id="Trailblazer",
            name="开拓者",
            entity_type="external_variable",
            factor_affinity=["creation", "passage"],
            ability="pathway_substitution",
            position=position
        )
        self.has_taken_time_path = False
        self.sparks_collected = []

    def activate(self, system_state: Dict) -> Dict:
        """激活：介入翁法罗斯"""
        self.is_active = True

        # 检查岁月路径是否空缺
        time_pathway_vacant = system_state.get("time_pathway_vacant", True)

        if time_pathway_vacant:
            self.has_taken_time_path = True

        impact = {
            "event": "external_intervention",
            "entity": "Trailblazer",
            "effects": {
                "time_pathway_substituted": self.has_taken_time_path,
                "twelve_factor_resonance": True,  # 与十二因子共鸣
                "system_phase": "final_loop"
            },
            "description": "天外之人介入了翁法罗斯的轮回，接替了岁月的路径"
        }

        self.impact_history.append(impact)
        return impact

    def guide_neikos(self, neikos: NeiKos496) -> Dict:
        """引导白厄跨越奇点"""
        if not self.is_active:
            return {"status": "failed", "reason": "开拓者未激活"}

        result = neikos.cross_singularity(trailblazer_present=True)

        self.impact_history.append({
            "event": "guided_singularity_crossing",
            "target": "NeiKos496",
            "result": result
        })

        return result

    def collect_memory(self, memory_fragment: Dict):
        """收集记忆碎片（给三月七的照片）"""
        self.sparks_collected.append(memory_fragment)


class SpecialEntityManager:
    """特殊实体管理器"""
    def __init__(self):
        self.entities: Dict[str, SpecialEntity] = {}

    def register_entity(self, entity: SpecialEntity):
        """注册实体"""
        self.entities[entity.entity_id] = entity

    def get_active_entities(self) -> List[str]:
        """获取活跃实体列表"""
        return [eid for eid, e in self.entities.items() if e.is_active]

    def trigger_entity(self, entity_id: str, system_state: Dict) -> Optional[Dict]:
        """触发实体能力"""
        if entity_id in self.entities:
            return self.entities[entity_id].activate(system_state)
        return None

    def get_entity_states(self) -> Dict:
        """获取所有实体状态"""
        return {eid: e.get_state() for eid, e in self.entities.items()}
