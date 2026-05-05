"""
World Engine - 翁法罗斯世界演算
模拟文明迭代、城邦兴衰、人口演化
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import random


@dataclass
class CityState:
    """城邦状态"""
    name: str
    city_id: str
    titan_patron: str
    position: Tuple[int, int]
    population: int = 10000
    defense: float = 0.5
    faith: float = 0.5
    prosperity: float = 0.5
    corruption: float = 0.0
    is_fallen: bool = False
    history: List[Dict] = field(default_factory=list)

    def update(self, black_tide_level: float, 
               titan_alive: bool,
               pathway_influence: Dict[str, float]):
        destruction = pathway_influence.get("nihility", 0.0)
        erudition = pathway_influence.get("erudition", 0.0)
        remembrance = pathway_influence.get("remembrance", 0.0)

        self.corruption = min(1.0, self.corruption + black_tide_level * 0.1 * (1 + destruction))

        if self.is_fallen:
            self.population = int(self.population * 0.9)
        else:
            growth_rate = 0.02 * (1 + erudition) * (1 + self.prosperity)
            decline = 0.05 * self.corruption * (1 + destruction)
            self.population = max(0, int(self.population * (1 + growth_rate - decline)))

        if titan_alive:
            self.prosperity = min(1.0, self.prosperity + 0.01 * erudition)
        else:
            self.prosperity = max(0.0, self.prosperity - 0.02)

        if self.corruption > 0.5:
            self.faith = max(0.0, self.faith - 0.05)
        else:
            self.faith = min(1.0, self.faith + 0.01 * remembrance)

        if not titan_alive:
            self.defense = max(0.1, self.defense - 0.03)

        if self.corruption > 0.9 or self.population < 100:
            self.is_fallen = True

        self.history.append({
            "population": self.population,
            "prosperity": self.prosperity,
            "faith": self.faith,
            "corruption": self.corruption,
            "is_fallen": self.is_fallen
        })

        if len(self.history) > 1000:
            self.history.pop(0)

    def get_state(self) -> Dict:
        return {
            "name": self.name,
            "population": self.population,
            "defense": self.defense,
            "faith": self.faith,
            "prosperity": self.prosperity,
            "corruption": self.corruption,
            "is_fallen": self.is_fallen,
            "titan_patron": self.titan_patron
        }


class WorldEngine:
    """世界演算引擎"""
    def __init__(self, world_size: Tuple[int, int], cities_config: Dict):
        self.world_size = world_size
        self.cities_config = cities_config
        self.civilization_density = torch.zeros(world_size)
        self.terrain = self._generate_terrain()
        self.cities: Dict[str, CityState] = {}
        self._init_cities()
        self.world_age = 0
        self.total_entropy = 0.0

    def _generate_terrain(self) -> torch.Tensor:
        h, w = self.world_size
        x = torch.linspace(0, 2*np.pi, w)
        y = torch.linspace(0, 2*np.pi, h)
        X, Y = torch.meshgrid(x, y, indexing='xy')
        terrain = (torch.sin(X) * torch.cos(Y) + 1) / 2
        return terrain.T

    def _init_cities(self):
        positions = {
            "okhema": (min(70, self.world_size[0]-1), min(70, self.world_size[1]-1)),
            "castrum_kremnos": (min(30, self.world_size[0]-1), min(30, self.world_size[1]-1)),
            "aedyria": (min(10, self.world_size[0]-1), min(80, self.world_size[1]-1)),
            "janusopolis": (min(80, self.world_size[0]-1), min(20, self.world_size[1]-1))
        }

        for city_id, config in self.cities_config.items():
            pos = positions.get(city_id, (self.world_size[0]//2, self.world_size[1]//2))
            self.cities[city_id] = CityState(
                name=config["name"],
                city_id=city_id,
                titan_patron=config["titan"],
                position=pos,
                population=config.get("population_base", 10000),
                defense=config.get("defense", 0.5),
                faith=config.get("faith", 0.5),
                is_fallen=config.get("fallen", False)
            )
            x, y = pos
            if 0 <= x < self.world_size[0] and 0 <= y < self.world_size[1]:
                self.civilization_density[x, y] = 1.0

    def step(self, black_tide_concentration: torch.Tensor,
             titan_alive_status: Dict[str, bool],
             pathway_influence: Dict[str, float]) -> Dict:
        self.world_age += 1
        self._update_civilization_density()

        fallen_cities = []
        for city_id, city in self.cities.items():
            x, y = city.position
            tide_level = 0.0
            if 0 <= x < self.world_size[0] and 0 <= y < self.world_size[1]:
                tide_level = black_tide_concentration[x, y].item()

            titan_alive = titan_alive_status.get(city.titan_patron, True)
            city.update(tide_level, titan_alive, pathway_influence)

            if city.is_fallen and len(city.history) > 1 and not city.history[-2]["is_fallen"]:
                fallen_cities.append(city_id)

        self.total_entropy = self._compute_world_entropy()
        collapse_degree = self._compute_collapse_degree()

        return {
            "world_age": self.world_age,
            "total_entropy": self.total_entropy,
            "collapse_degree": collapse_degree,
            "fallen_cities": fallen_cities,
            "total_population": sum(c.population for c in self.cities.values()),
            "city_states": {cid: c.get_state() for cid, c in self.cities.items()}
        }

    def _update_civilization_density(self):
        """向量化更新文明密度场"""
        density = torch.zeros(self.world_size)
        for city in self.cities.values():
            if city.is_fallen or city.population <= 0:
                continue
            cx, cy = city.position
            radius = max(1, int(np.sqrt(max(1, city.population)) / 100))

            # 创建坐标网格
            h, w = self.world_size
            y_coords = torch.arange(h).unsqueeze(1).expand(h, w)
            x_coords = torch.arange(w).unsqueeze(0).expand(h, w)

            dist = torch.sqrt((x_coords - cy).float()**2 + (y_coords - cx).float()**2)
            mask = dist <= radius
            influence = city.prosperity * (1 - dist / radius).clamp(0, 1)
            density += influence * mask.float()

        self.civilization_density = torch.clamp(density, 0, 1)

    def _compute_world_entropy(self) -> float:
        entropies = []
        for city in self.cities.values():
            city_entropy = city.corruption + (1 - city.prosperity) + (1 - city.faith)
            entropies.append(city_entropy / 3)
        return np.mean(entropies) if entropies else 0.0

    def _compute_collapse_degree(self) -> float:
        if not self.cities:
            return 1.0
        fallen_ratio = sum(1 for c in self.cities.values() if c.is_fallen) / len(self.cities)
        base_pops = [c.history[0]["population"] if c.history else 10000 for c in self.cities.values()]
        total_base = sum(base_pops) if base_pops else 1
        total_current = sum(c.population for c in self.cities.values())
        population_decline = 1 - (total_current / total_base) if total_base > 0 else 0
        return min(1.0, (fallen_ratio + population_decline) / 2)

    def get_city_positions(self) -> Dict[str, Tuple[int, int]]:
        return {cid: c.position for cid, c in self.cities.items()}

    def get_titan_positions(self) -> Dict[str, Tuple[int, int]]:
        return {c.titan_patron: c.position for c in self.cities.values()}

    def reset(self):
        self.world_age = 0
        self.civilization_density = torch.zeros(self.world_size)
        self.total_entropy = 0.0
        self._init_cities()
