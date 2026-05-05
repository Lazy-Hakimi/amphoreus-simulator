"""
Amphoreus Main Simulator - 翁法罗斯世界模拟器主引擎
整合所有子系统，运行完整的模拟实验
"""

import torch
import numpy as np
import random
import json
import numpy as np
import time

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        if hasattr(obj, 'detach'):
            return obj.detach().cpu().tolist()
        return super().default(obj)
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from core.config import (
    TITAN_CONFIG, CITIES, TWELVE_FACTORS, 
    EXPERIMENT_PHASES, PATHWAYS, SPECIAL_ENTITIES,
    NeuralConfig, SimulationConfig
)
from neural.neural_core import TwelveFactorNetwork, GoldenBloodAgent, FACTOR_TO_IDX
from world.black_tide import BlackTide, BlackTideConfig
from world.world_engine import WorldEngine
from core.recreation_engine import RecreationEngine
from core.titan_system import TitanSystem
from core.pathways import TriplePathway
from core.special_entities import (
    SpecialEntityManager, NeiKos496, PhiLia093, Trailblazer
)


class AmphoreusSimulator:
    """
    翁法罗斯世界模拟器

    核心流程：
    1. 初始化实验环境（帝皇权杖 δ-me13）
    2. 按阶段运行演算（无机→有机→人类→再创世→永劫回归→最终循环）
    3. 每步更新：神经网络 → 世界引擎 → 黑潮 → 泰坦/黄金裔 → 命途 → 特殊实体
    4. 检查再创世触发条件
    5. 记录日志与可视化
    """

    def __init__(self, 
                 neural_config: Optional[NeuralConfig] = None,
                 sim_config: Optional[SimulationConfig] = None,
                 seed: int = 42):

        self.neural_config = neural_config or NeuralConfig()
        self.sim_config = sim_config or SimulationConfig()
        self.seed = seed

        # 设置随机种子
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

        # 初始化各子系统
        self._init_systems()

        # 模拟状态
        self.current_loop = 0
        self.current_phase = "inorganic"
        self.phase_loop_count = 0
        self.total_steps = 0
        self.is_running = False
        self.is_terminal = False

        # 日志
        self.logs = []
        self.step_logs = []

        # 统计
        self.stats = {
            "total_recreations": 0,
            "total_deaths": 0,
            "sparks_collected": 0,
            "destruction_equation_progress": []
        }

    def _init_systems(self):
        """初始化所有子系统"""
        print("[初始化] 正在构建翁法罗斯模拟环境...")

        # 1. 十二因子神经网络
        self.factor_network = TwelveFactorNetwork(
            factor_names=TWELVE_FACTORS,
            dim=64
        ).to(self.neural_config.device)

        # 2. 黑潮系统
        black_tide_cfg = BlackTideConfig(
            spread_rate=0.05,
            erosion_intensity=0.3,
            source_locations=[(0, 0), (50, 50), (99, 99)]
        )
        self.black_tide = BlackTide(
            world_size=self.sim_config.world_size,
            config=black_tide_cfg
        )

        # 3. 世界引擎
        self.world_engine = WorldEngine(
            world_size=self.sim_config.world_size,
            cities_config=CITIES
        )

        # 4. 再创世引擎
        self.recreation_engine = RecreationEngine(
            threshold=self.sim_config.recreation_threshold,
            memory_retention=0.3
        )

        # 5. 泰坦系统
        self.titan_system = TitanSystem(
            titan_config=TITAN_CONFIG,
            cities_config=CITIES
        )

        # 6. 三重命途
        self.pathways = TriplePathway()

        # 7. 特殊实体管理器
        self.entity_manager = SpecialEntityManager()

        # 预注册特殊实体（初始不激活）
        self.entity_manager.register_entity(NeiKos496(position=(50, 50)))
        self.entity_manager.register_entity(PhiLia093(position=(50, 50)))
        self.entity_manager.register_entity(Trailblazer(position=(50, 50)))

        print("[初始化] 所有子系统构建完成")

    def run_simulation(self, max_steps: Optional[int] = None, 
                      verbose: bool = True) -> Dict:
        """
        运行完整模拟

        Args:
            max_steps: 最大步数（None则运行到终止条件）
            verbose: 是否打印详细日志

        Returns:
            模拟结果摘要
        """
        self.is_running = True
        max_steps = max_steps or 100000

        print(f"\n{'='*60}")
        print("  翁法罗斯世界模拟启动")
        print(f"  实验阶段: {self.current_phase}")
        print(f"  目标: 求解毁灭方程，证伪生命第一因")
        print(f"{'='*60}\n")

        start_time = time.time()

        while self.is_running and self.total_steps < max_steps and not self.is_terminal:
            self._step(verbose=(verbose and self.total_steps % self.sim_config.log_interval == 0))

        elapsed = time.time() - start_time

        result = self._generate_final_report(elapsed)

        print(f"\n{'='*60}")
        print("  模拟结束")
        print(f"  总步数: {self.total_steps}")
        print(f"  总耗时: {elapsed:.2f}秒")
        print(f"{'='*60}")

        return result

    def _step(self, verbose: bool = False):
        """单步模拟"""
        self.total_steps += 1
        self.phase_loop_count += 1

        # 获取当前阶段配置
        phase_cfg = EXPERIMENT_PHASES.get(self.current_phase, {})

        # 1. 生成外部输入（模拟环境刺激）
        batch_size = 1
        external_input = torch.randn(batch_size, 12 * 64).to(self.neural_config.device)

        # 2. 计算命途影响力
        destruction_eq = self.factor_network.compute_destruction_equation()
        active_entities = self.entity_manager.get_active_entities()

        pathway_influences = self.pathways.compute_influence(
            world_entropy=self.world_engine.total_entropy,
            loop_count=self.current_loop,
            destruction_equation=destruction_eq,
            special_entities_present=active_entities
        )

        # 3. 神经网络前向传播
        active_factors = [f for f in TWELVE_FACTORS 
                         if f not in self._get_fallen_titan_factors()]

        factor_outputs = self.factor_network(
            external_input=external_input,
            active_factors=active_factors,
            pathway_influence=pathway_influences
        )

        # 4. 黑潮演化
        titan_positions = self.titan_system.get_titan_positions()
        black_tide_report = self.black_tide.step(
            civilization_density=self.world_engine.civilization_density,
            titan_positions=titan_positions,
            loop_count=self.current_loop
        )

        # 5. 世界引擎演化
        titan_alive_status = self.titan_system.get_titan_alive_status()
        world_report = self.world_engine.step(
            black_tide_concentration=black_tide_report["concentration"],
            titan_alive_status=titan_alive_status,
            pathway_influence=pathway_influences
        )

        # 6. 泰坦/黄金裔交互
        self.titan_system.process_black_tide(
            black_tide_concentration=black_tide_report["concentration"],
            corrupted_titans=black_tide_report["corrupted_titans"]
        )

        # 在人类阶段及以后执行逐火之旅
        if phase_cfg.get("has_recreation", False):
            pilgrimage_report = self.titan_system.process_pilgrimage()
        else:
            pilgrimage_report = {"step": 0, "events": []}

        # 7. 应用命途效果
        pathway_effects = self.pathways.apply_pathway_effects(
            factor_network=self.factor_network,
            world_state=world_report,
            influences=pathway_influences
        )

        # 8. 检查特殊实体触发
        self._check_special_entities()

        # 9. 检查再创世
        if self.recreation_engine.check_trigger(
            collapse_degree=world_report["collapse_degree"],
            loop_count=self.phase_loop_count,
            phase_config=phase_cfg
        ):
            self._execute_recreation(world_report)

        # 10. 检查阶段转换
        self._check_phase_transition()

        # 11. 记录日志
        if self.total_steps % self.sim_config.log_interval == 0 or verbose:
            self._log_step(
                step=self.total_steps,
                phase=self.current_phase,
                loop=self.current_loop,
                world_report=world_report,
                black_tide_report=black_tide_report,
                pathway_influences=pathway_influences,
                destruction_eq=destruction_eq,
                pilgrimage_report=pilgrimage_report
            )

        # 12. 检查终止条件
        if phase_cfg.get("is_terminal", False):
            self.is_terminal = True

    def _get_fallen_titan_factors(self) -> List[str]:
        """获取已陨落泰坦对应的因子"""
        fallen = []
        for tid, titan in self.titan_system.titans.items():
            if not titan.is_alive:
                fallen.append(titan.factor)
        return fallen

    def _check_special_entities(self):
        """检查特殊实体触发条件"""
        # 永劫回归阶段激活白厄和昔涟
        if self.current_phase == "eternal_return" and self.phase_loop_count == 1:
            neikos = self.entity_manager.entities.get("NeiKos496")
            philia = self.entity_manager.entities.get("PhiLia093")

            if neikos and not neikos.is_active:
                neikos.activate({"time_pathway_vacant": False})
                print(f"[特殊事件] {neikos.name} 激活！盗火行者现身")

            if philia and not philia.is_active:
                philia.erase()
                print(f"[特殊事件] {philia.name} 的存在被抹除")

        # 最终循环阶段激活开拓者
        if self.current_phase == "final_loop" and self.phase_loop_count == 1:
            trailblazer = self.entity_manager.entities.get("Trailblazer")
            neikos = self.entity_manager.entities.get("NeiKos496")

            if trailblazer:
                trailblazer.activate({"time_pathway_vacant": True})
                print(f"[特殊事件] {trailblazer.name} 介入！天外变量到来")

                if neikos:
                    result = trailblazer.guide_neikos(neikos)
                    print(f"[特殊事件] {result.get('description', '奇点突破')}")

    def _execute_recreation(self, world_report: Dict):
        """执行再创世"""
        print(f"\n[再创世] 文明崩溃度达到阈值，触发世界重置...")

        # 收集当前状态
        factor_states = self.factor_network.get_factor_states()
        agent_states = {aid: a.get_state() for aid, a in self.titan_system.golden_bloods.items()}
        titan_states = {tid: t.get_state() for tid, t in self.titan_system.titans.items()}

        # 执行再创世
        new_gen = self.recreation_engine.execute_recreation(
            world_state=world_report,
            factor_network_state=factor_states,
            agent_states=agent_states,
            titan_states=titan_states,
            phase=self.current_phase
        )

        # 重置子系统
        self.world_engine.reset()
        self.black_tide = BlackTide(
            world_size=self.sim_config.world_size,
            config=BlackTideConfig()
        )
        self.titan_system.reset()

        # 应用继承的火种
        for spark_key, spark_data in new_gen.get("inherited_sparks", {}).items():
            print(f"  [火种继承] {spark_key} -> 保留率 {spark_data['retention']:.0%}")

        self.current_loop += 1
        self.phase_loop_count = 0
        self.stats["total_recreations"] += 1

        print(f"[再创世] 第 {self.current_loop} 次再创世完成")
        print(f"  毁灭方程进展: {new_gen['destruction_equation_progress']:.4f}")

    def _check_phase_transition(self):
        """检查阶段转换"""
        phase_cfg = EXPERIMENT_PHASES.get(self.current_phase, {})
        max_loops = phase_cfg.get("max_loops", float('inf'))

        if self.phase_loop_count >= max_loops:
            transitions = {
                "inorganic": "organic",
                "organic": "human",
                "human": "recreation",
                "recreation": "eternal_return",
                "eternal_return": "final_loop",
                "final_loop": "conclusion"
            }

            next_phase = transitions.get(self.current_phase)
            if next_phase:
                print(f"\n[阶段转换] {self.current_phase} -> {next_phase}")
                self.current_phase = next_phase
                self.phase_loop_count = 0

    def _log_step(self, step: int, phase: str, loop: int,
                  world_report: Dict, black_tide_report: Dict,
                  pathway_influences: Dict, destruction_eq: float,
                  pilgrimage_report: Dict):
        """记录单步日志"""
        log_entry = {
            "step": step,
            "phase": phase,
            "loop": loop,
            "world_age": world_report["world_age"],
            "total_population": world_report["total_population"],
            "total_entropy": world_report["total_entropy"],
            "collapse_degree": world_report["collapse_degree"],
            "black_tide_max": black_tide_report["concentration"].max().item(),
            "pathway_dominant": max(pathway_influences, key=pathway_influences.get),
            "destruction_equation": destruction_eq,
            "fallen_cities": world_report["fallen_cities"],
            "pilgrimage_events": pilgrimage_report.get("events", [])
        }

        self.step_logs.append(log_entry)

        # 打印摘要
        print(f"[Step {step:6d}] Phase:{phase:12s} Loop:{loop:3d} | "
              f"Entropy:{world_report['total_entropy']:.3f} | "
              f"Collapse:{world_report['collapse_degree']:.3f} | "
              f"Tide:{black_tide_report['concentration'].max().item():.3f} | "
              f"Pathway:{max(pathway_influences, key=pathway_influences.get):12s} | "
              f"DestEq:{destruction_eq:.4f}")

    def _generate_final_report(self, elapsed: float) -> Dict:
        """生成最终报告"""
        recreation_stats = self.recreation_engine.get_recreation_stats()

        report = {
            "simulation_summary": {
                "total_steps": self.total_steps,
                "total_loops": self.current_loop,
                "final_phase": self.current_phase,
                "elapsed_seconds": elapsed,
                "is_terminal": self.is_terminal
            },
            "recreation_stats": recreation_stats,
            "pathway_balance": self.pathways.get_pathway_balance(),
            "final_world_state": {
                "total_population": sum(c.population for c in self.world_engine.cities.values()),
                "total_entropy": self.world_engine.total_entropy,
                "collapse_degree": self._compute_final_collapse(),
                "fallen_cities": [cid for cid, c in self.world_engine.cities.items() if c.is_fallen]
            },
            "titan_states": {tid: t.get_state() for tid, t in self.titan_system.titans.items()},
            "special_entities": self.entity_manager.get_entity_states(),
            "factor_states": self.factor_network.get_factor_states(),
            "destruction_equation_final": self.factor_network.compute_destruction_equation(),
            "step_logs_count": len(self.step_logs)
        }

        return report

    def _compute_final_collapse(self) -> float:
        """计算最终崩溃度"""
        if not self.world_engine.cities:
            return 1.0
        fallen = sum(1 for c in self.world_engine.cities.values() if c.is_fallen)
        return fallen / len(self.world_engine.cities)

    def save_logs(self, filepath: str = "logs/simulation_log.json"):
        """保存日志到文件"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.step_logs, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
        print(f"[日志] 已保存到 {filepath}")

    def save_report(self, filepath: str = "logs/final_report.json"):
        """保存最终报告"""
        report = self._generate_final_report(0)
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)
        print(f"[报告] 已保存到 {filepath}")
