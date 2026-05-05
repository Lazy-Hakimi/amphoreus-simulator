"""
Black Tide System - 黑潮模拟
黑潮并非实体，而是循环期间模拟空无法承载方程运行所产生的视觉乱码
"""

import torch
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random


@dataclass
class BlackTideConfig:
    """黑潮配置"""
    spread_rate: float = 0.05
    erosion_intensity: float = 0.3
    render_glitch_prob: float = 0.1
    titan_corruption_threshold: float = 0.7
    entropy_boost: float = 0.2
    source_locations: List[Tuple[int, int]] = None

    def __post_init__(self):
        if self.source_locations is None:
            self.source_locations = [(0, 0), (50, 50)]


class BlackTide:
    """黑潮 - 渎神的侵蚀之力"""
    def __init__(self, world_size: Tuple[int, int], config: BlackTideConfig):
        self.world_size = world_size
        self.config = config
        self.concentration = torch.zeros(world_size)
        self.render_glitches = {}
        self.corrupted_entities = set()
        self.tide_history = []

        # 扩散卷积核
        self.kernel = torch.tensor([
            [0.05, 0.1, 0.05],
            [0.1, 0.4, 0.1],
            [0.05, 0.1, 0.05]
        ]).unsqueeze(0).unsqueeze(0)

        for loc in config.source_locations:
            x, y = loc
            if 0 <= x < world_size[0] and 0 <= y < world_size[1]:
                self.concentration[x, y] = 1.0

    def step(self, civilization_density: torch.Tensor,
             titan_positions: Dict[str, Tuple[int, int]],
             loop_count: int) -> Dict:
        """黑潮演化一步（向量化实现）"""
        # 使用卷积进行扩散
        conc = self.concentration.unsqueeze(0).unsqueeze(0)
        kernel = self.kernel.to(conc.dtype)

        # 边界填充后卷积
        padded = F.pad(conc, (1, 1, 1, 1), mode='replicate')
        diffused = F.conv2d(padded, kernel)
        new_concentration = diffused.squeeze()

        # 文明密度吸引
        new_concentration += civilization_density * 0.01

        # 循环次数影响
        loop_factor = min(loop_count / 10000, 1.0)
        new_concentration *= (1 + loop_factor * 0.1)

        self.concentration = torch.clamp(new_concentration, 0, 1)

        # 生成渲染错误
        glitches = self._generate_render_glitches()

        # 检测泰坦腐化
        corrupted_titans = self._check_titan_corruption(titan_positions)

        self.tide_history.append({
            "max_concentration": self.concentration.max().item(),
            "mean_concentration": self.concentration.mean().item(),
            "glitches_count": len(glitches),
            "corrupted_titans": corrupted_titans
        })

        return {
            "concentration": self.concentration,
            "glitches": glitches,
            "corrupted_titans": corrupted_titans,
            "entropy_increase": self.config.entropy_boost * self.concentration.mean().item()
        }

    def _generate_render_glitches(self) -> List[Dict]:
        glitches = []
        high_tide_mask = self.concentration > 0.5
        if high_tide_mask.any():
            glitch_positions = torch.nonzero(high_tide_mask, as_tuple=False)
            num_glitches = min(len(glitch_positions), 10)
            indices = torch.randperm(len(glitch_positions))[:num_glitches]

            for idx in indices:
                x, y = glitch_positions[idx].tolist()
                glitch = {
                    "position": (x, y),
                    "type": random.choice(["pixelation", "color_inversion", 
                                          "geometry_distortion", "temporal_artifact"]),
                    "intensity": self.concentration[x, y].item(),
                    "description": self._generate_glitch_description()
                }
                glitches.append(glitch)
                self.render_glitches[(x, y)] = glitch

        return glitches

    def _generate_glitch_description(self) -> str:
        descriptions = [
            "空间结构出现不可名状的扭曲",
            "时间流在此断裂，呈现递归残影",
            "物质渲染失败，露出底层代码",
            "色彩通道溢出，呈现渎神之紫",
            "几何体失去维度约束，向虚空坍缩",
            "记忆数据损坏，出现未知实体残像"
        ]
        return random.choice(descriptions)

    def _check_titan_corruption(self, titan_positions: Dict[str, Tuple[int, int]]) -> List[str]:
        corrupted = []
        for titan_name, (x, y) in titan_positions.items():
            if 0 <= x < self.world_size[0] and 0 <= y < self.world_size[1]:
                if self.concentration[x, y] > self.config.titan_corruption_threshold:
                    corrupted.append(titan_name)
                    self.corrupted_entities.add(titan_name)
        return corrupted

    def get_corruption_level(self, position: Tuple[int, int]) -> float:
        x, y = position
        if 0 <= x < self.world_size[0] and 0 <= y < self.world_size[1]:
            return self.concentration[x, y].item()
        return 0.0

    def purify(self, position: Tuple[int, int], radius: int = 5, strength: float = 0.5):
        x, y = position
        h, w = self.world_size
        y_coords = torch.arange(h).unsqueeze(1).expand(h, w)
        x_coords = torch.arange(w).unsqueeze(0).expand(h, w)
        dist = torch.sqrt((x_coords - y).float()**2 + (y_coords - x).float()**2)
        mask = dist <= radius
        decay = (1 - strength * (1 - dist / radius).clamp(0, 1)) * mask.float() + (~mask).float()
        self.concentration *= decay
        self.concentration = torch.clamp(self.concentration, 0, 1)

    def get_state(self) -> Dict:
        return {
            "max_concentration": self.concentration.max().item(),
            "mean_concentration": self.concentration.mean().item(),
            "corrupted_entities": list(self.corrupted_entities),
            "total_glitches": len(self.render_glitches),
            "history_length": len(self.tide_history)
        }
