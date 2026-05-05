"""
Titan System - 泰坦与黄金裔
模拟十二泰坦的神权、陨落、火种继承
以及黄金裔的逐火之旅
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import random


@dataclass
class Titan:
    """泰坦 - 神性模拟实体"""
    titan_id: str
    name: str
    title: str
    factor: str
    city: str
    position: Tuple[int, int]

    # 神权状态
    is_alive: bool = True
    is_corrupted: bool = False
    has_fallen: bool = False

    # 神权强度
    divine_power: float = 1.0

    # 火种状态
    spark_intact: bool = True
    spark_holder: Optional[str] = None  # 持有火种的黄金裔

    # 神经网络权重（神权的核心参数）
    neural_weights: Dict = field(default_factory=dict)

    # 历史
    history: List[Dict] = field(default_factory=list)

    def take_damage(self, damage: float, source: str = "unknown"):
        """受到伤害（黑潮/黄金裔攻击）"""
        self.divine_power = max(0.0, self.divine_power - damage)

        if self.divine_power <= 0.3 and self.is_alive:
            self.is_alive = False
            self.has_fallen = True
            self.history.append({
                "event": "fallen",
                "source": source,
                "remaining_power": self.divine_power
            })

    def corrupt(self, intensity: float):
        """被黑潮腐化"""
        self.is_corrupted = True
        self.divine_power *= (1 - intensity * 0.5)
        self.history.append({
            "event": "corrupted",
            "intensity": intensity
        })

    def yield_spark(self) -> Optional[Dict]:
        """献出火种"""
        if self.spark_intact:
            self.spark_intact = False
            return {
                "titan_id": self.titan_id,
                "factor": self.factor,
                "weights": self.neural_weights.copy(),
                "power": self.divine_power
            }
        return None

    def get_state(self) -> Dict:
        return {
            "titan_id": self.titan_id,
            "name": self.name,
            "is_alive": self.is_alive,
            "is_corrupted": self.is_corrupted,
            "has_fallen": self.has_fallen,
            "divine_power": self.divine_power,
            "spark_intact": self.spark_intact,
            "spark_holder": self.spark_holder
        }


@dataclass
class GoldenBlood:
    """黄金裔 - 电信号智能体"""
    agent_id: str
    name: str
    factor_affinity: List[str]
    city_of_origin: str

    # 生命状态
    is_alive: bool = True
    is_demigod: bool = False

    # 金血浓度（毁灭命途标记）
    golden_blood_level: float = 0.0

    # 持有的火种
    held_sparks: List[Dict] = field(default_factory=list)

    # 能力值
    combat_power: float = 0.5
    wisdom: float = 0.5
    faith: float = 0.5

    # 位置
    position: Tuple[int, int] = (50, 50)

    # 逐火之旅进度
    pilgrimage_progress: float = 0.0

    # 预言
    prophecy: Optional[str] = None

    # 历史
    history: List[Dict] = field(default_factory=list)

    def hunt_titan(self, titan: Titan) -> bool:
        """狩猎泰坦"""
        if not titan.is_alive or titan.spark_intact:
            return False

        # 战斗判定
        success_prob = self.combat_power * (1 + self.golden_blood_level)
        if random.random() < success_prob:
            spark = titan.yield_spark()
            if spark:
                self.held_sparks.append(spark)
                self.combat_power += 0.1
                self.history.append({
                    "event": "hunt_success",
                    "titan": titan.titan_id,
                    "sparks_count": len(self.held_sparks)
                })
                return True

        self.history.append({
            "event": "hunt_failed",
            "titan": titan.titan_id
        })
        return False

    def inherit_spark(self, spark: Dict):
        """继承火种成为半神"""
        self.held_sparks.append(spark)
        self.is_demigod = True
        self.golden_blood_level += 0.3
        self.combat_power += 0.3
        self.wisdom += 0.2

        self.history.append({
            "event": "become_demigod",
            "spark_factor": spark.get("factor"),
            "power_after": self.combat_power
        })

    def sacrifice(self) -> List[Dict]:
        """
        自我牺牲（如逐火之旅的终点）
        归还所有火种
        """
        self.is_alive = False
        sparks = self.held_sparks.copy()
        self.held_sparks = []

        self.history.append({
            "event": "sacrifice",
            "sparks_returned": len(sparks)
        })

        return sparks

    def move(self, target: Tuple[int, int], world_size: Tuple[int, int]):
        """移动"""
        x, y = self.position
        tx, ty = target

        # 向目标移动一步
        dx = np.sign(tx - x)
        dy = np.sign(ty - y)

        nx = max(0, min(world_size[0] - 1, x + dx))
        ny = max(0, min(world_size[1] - 1, y + dy))

        self.position = (nx, ny)

    def get_state(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "is_alive": self.is_alive,
            "is_demigod": self.is_demigod,
            "golden_blood_level": self.golden_blood_level,
            "held_sparks": len(self.held_sparks),
            "combat_power": self.combat_power,
            "pilgrimage_progress": self.pilgrimage_progress,
            "position": self.position
        }


class TitanSystem:
    """
    泰坦系统管理器
    管理十二泰坦和黄金裔的交互
    """
    def __init__(self, titan_config: Dict, cities_config: Dict):
        self.titan_config = titan_config
        self.cities_config = cities_config

        # 初始化泰坦
        self.titans: Dict[str, Titan] = {}
        self._init_titans()

        # 黄金裔列表
        self.golden_bloods: Dict[str, GoldenBlood] = {}

        # 逐火之旅状态
        self.pilgrimage_active = False
        self.pilgrimage_step = 0

        # 已收集火种数
        self.collected_sparks = 0

    def _init_titans(self):
        """初始化十二泰坦"""
        city_positions = {
            "okhema": (70, 70),
            "castrum_kremnos": (30, 30),
            "aedyria": (10, 80),
            "janusopolis": (80, 20)
        }

        for titan_id, config in self.titan_config.items():
            city = config.get("city", "okhema")
            pos = city_positions.get(city, (50, 50))

            self.titans[titan_id] = Titan(
                titan_id=titan_id,
                name=config["name"],
                title=config["title"],
                factor=config["factor"],
                city=city,
                position=pos,
                divine_power=1.0
            )

    def spawn_golden_blood(self, city_id: str, 
                          agent_id: str,
                          name: str,
                          factor_affinity: List[str]) -> GoldenBlood:
        """生成黄金裔"""
        city_pos = {
            "okhema": (70, 70),
            "castrum_kremnos": (30, 30),
            "aedyria": (10, 80),
            "janusopolis": (80, 20)
        }.get(city_id, (50, 50))

        agent = GoldenBlood(
            agent_id=agent_id,
            name=name,
            factor_affinity=factor_affinity,
            city_of_origin=city_id,
            position=city_pos,
            golden_blood_level=random.uniform(0.1, 0.3)  # 天生带有金血
        )

        self.golden_bloods[agent_id] = agent
        return agent

    def process_black_tide(self, black_tide_concentration: torch.Tensor,
                          corrupted_titans: List[str]):
        """处理黑潮对泰坦的影响"""
        for titan_id in corrupted_titans:
            if titan_id in self.titans:
                titan = self.titans[titan_id]
                if not titan.is_corrupted:
                    titan.corrupt(0.5)

        # 黑潮也影响黄金裔
        for agent in self.golden_bloods.values():
            if agent.is_alive:
                x, y = agent.position
                if 0 <= x < black_tide_concentration.shape[0] and                    0 <= y < black_tide_concentration.shape[1]:
                    tide_level = black_tide_concentration[x, y].item()
                    if tide_level > 0.5:
                        agent.golden_blood_level += 0.05  # 黑潮增强金血

    def process_pilgrimage(self, max_steps: int = 100) -> Dict:
        """
        执行逐火之旅的一步
        黄金裔狩猎泰坦、收集火种
        """
        self.pilgrimage_active = True
        self.pilgrimage_step += 1

        events = []

        # 每个存活的黄金裔行动
        for agent in list(self.golden_bloods.values()):
            if not agent.is_alive:
                continue

            # 寻找最近的活着的泰坦
            target_titan = None
            min_dist = float('inf')

            for titan in self.titans.values():
                if titan.is_alive and titan.spark_intact:
                    dist = np.sqrt((agent.position[0] - titan.position[0])**2 + 
                                  (agent.position[1] - titan.position[1])**2)
                    if dist < min_dist:
                        min_dist = dist
                        target_titan = titan

            if target_titan and min_dist < 10:
                # 尝试狩猎
                success = agent.hunt_titan(target_titan)
                if success:
                    events.append(f"{agent.name} 成功狩猎 {target_titan.name}")
                    self.collected_sparks += 1
            elif target_titan:
                # 向目标移动
                agent.move(target_titan.position, (100, 100))

        # 检查是否集齐十二火种
        if self.collected_sparks >= 12:
            events.append("十二火种集齐！准备再创世...")

        return {
            "step": self.pilgrimage_step,
            "events": events,
            "collected_sparks": self.collected_sparks,
            "active_agents": sum(1 for a in self.golden_bloods.values() if a.is_alive)
        }

    def get_titan_alive_status(self) -> Dict[str, bool]:
        """获取泰坦存活状态"""
        return {tid: t.is_alive for tid, t in self.titans.items()}

    def get_titan_positions(self) -> Dict[str, Tuple[int, int]]:
        """获取泰坦位置"""
        return {tid: t.position for tid, t in self.titans.items()}

    def get_states(self) -> Dict:
        return {
            "titans": {tid: t.get_state() for tid, t in self.titans.items()},
            "golden_bloods": {aid: a.get_state() for aid, a in self.golden_bloods.items()},
            "pilgrimage_step": self.pilgrimage_step,
            "collected_sparks": self.collected_sparks
        }

    def reset(self):
        """重置（再创世）"""
        self._init_titans()
        self.golden_bloods = {}
        self.pilgrimage_active = False
        self.pilgrimage_step = 0
        self.collected_sparks = 0
