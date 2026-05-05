"""
Amphoreus Simulator Test Suite
翁法罗斯模拟器测试套件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import torch
import numpy as np

from core.config import NeuralConfig, SimulationConfig, TITAN_CONFIG, CITIES, TWELVE_FACTORS
from neural.neural_core import FactorNeuron, TwelveFactorNetwork, GoldenBloodAgent
from world.black_tide import BlackTide, BlackTideConfig
from world.world_engine import WorldEngine, CityState
from core.titan_system import TitanSystem, Titan, GoldenBlood
from core.pathways import TriplePathway
from core.special_entities import NeiKos496, PhiLia093, Trailblazer
from core.recreation_engine import RecreationEngine
from core.main_simulator import AmphoreusSimulator


class TestFactorNeuron(unittest.TestCase):
    """测试因子神经元"""

    def test_initialization(self):
        neuron = FactorNeuron("creation", dim=64)
        self.assertEqual(neuron.factor_name, "creation")
        self.assertEqual(neuron.dim, 64)
        self.assertEqual(neuron.activation_history, [])

    def test_forward(self):
        neuron = FactorNeuron("creation", dim=64)
        stimulus = torch.randn(2, 64)
        spike, potential = neuron(stimulus)
        self.assertEqual(spike.shape, (2, 64))
        self.assertEqual(potential.shape, (2, 64))

    def test_golden_blood(self):
        neuron = FactorNeuron("creation", dim=64)
        neuron.infuse_golden_blood(0.5)
        self.assertGreater(neuron.golden_blood.item(), 0)

    def test_reset(self):
        neuron = FactorNeuron("creation", dim=64)
        neuron.activation_history = [1.0, 2.0]
        neuron.reset_potential()
        self.assertEqual(neuron.activation_history, [])


class TestTwelveFactorNetwork(unittest.TestCase):
    """测试十二因子网络"""

    def test_initialization(self):
        net = TwelveFactorNetwork(TWELVE_FACTORS, dim=64)
        self.assertEqual(len(net.factors), 12)
        self.assertEqual(net.num_factors, 12)

    def test_forward(self):
        net = TwelveFactorNetwork(TWELVE_FACTORS, dim=64)
        input_tensor = torch.randn(1, 12 * 64)
        outputs = net(input_tensor)
        self.assertIn("creation", outputs)

    def test_destruction_equation(self):
        net = TwelveFactorNetwork(TWELVE_FACTORS, dim=64)
        value = net.compute_destruction_equation()
        self.assertIsInstance(value, float)
        self.assertGreaterEqual(value, 0)

    def test_factor_states(self):
        net = TwelveFactorNetwork(TWELVE_FACTORS, dim=64)
        states = net.get_factor_states()
        self.assertEqual(len(states), 12)
        self.assertIn("creation", states)


class TestBlackTide(unittest.TestCase):
    """测试黑潮系统"""

    def test_initialization(self):
        bt = BlackTide((50, 50), BlackTideConfig())
        self.assertEqual(bt.concentration.shape, (50, 50))

    def test_step(self):
        bt = BlackTide((50, 50), BlackTideConfig())
        civ_density = torch.zeros(50, 50)
        titan_pos = {"kephale": (25, 25)}
        report = bt.step(civ_density, titan_pos, loop_count=0)
        self.assertIn("concentration", report)
        self.assertIn("glitches", report)

    def test_purify(self):
        bt = BlackTide((50, 50), BlackTideConfig())
        bt.concentration[25, 25] = 1.0
        bt.purify((25, 25), radius=5)
        self.assertLess(bt.concentration[25, 25].item(), 1.0)

    def test_get_state(self):
        bt = BlackTide((50, 50), BlackTideConfig())
        state = bt.get_state()
        self.assertIn("max_concentration", state)
        self.assertIn("mean_concentration", state)


class TestWorldEngine(unittest.TestCase):
    """测试世界引擎"""

    def test_initialization(self):
        we = WorldEngine((50, 50), CITIES)
        self.assertEqual(len(we.cities), 4)
        self.assertEqual(we.world_age, 0)

    def test_step(self):
        we = WorldEngine((50, 50), CITIES)
        tide = torch.zeros(50, 50)
        titan_alive = {t: True for t in TITAN_CONFIG.keys()}
        pathway = {"erudition": 0.4, "nihility": 0.3, "remembrance": 0.3}
        report = we.step(tide, titan_alive, pathway)
        self.assertIn("total_population", report)
        self.assertIn("collapse_degree", report)
        self.assertEqual(we.world_age, 1)

    def test_reset(self):
        we = WorldEngine((50, 50), CITIES)
        we.world_age = 100
        we.reset()
        self.assertEqual(we.world_age, 0)


class TestTitanSystem(unittest.TestCase):
    """测试泰坦系统"""

    def test_initialization(self):
        ts = TitanSystem(TITAN_CONFIG, CITIES)
        self.assertEqual(len(ts.titans), 12)

    def test_titan_damage(self):
        ts = TitanSystem(TITAN_CONFIG, CITIES)
        titan = ts.titans["kephale"]
        titan.take_damage(0.8)
        self.assertFalse(titan.is_alive)

    def test_spawn_golden_blood(self):
        ts = TitanSystem(TITAN_CONFIG, CITIES)
        agent = ts.spawn_golden_blood("okhema", "test_1", "测试者", ["creation"])
        self.assertIn("test_1", ts.golden_bloods)
        self.assertGreater(agent.golden_blood_level, 0)

    def test_reset(self):
        ts = TitanSystem(TITAN_CONFIG, CITIES)
        ts.spawn_golden_blood("okhema", "test_1", "测试者", ["creation"])
        ts.reset()
        self.assertEqual(len(ts.golden_bloods), 0)


class TestPathways(unittest.TestCase):
    """测试三重命途"""

    def test_initialization(self):
        tp = TriplePathway()
        self.assertEqual(len(tp.pathways), 3)

    def test_compute_influence(self):
        tp = TriplePathway()
        influences = tp.compute_influence(0.5, 100, 0.3)
        self.assertEqual(len(influences), 3)
        self.assertAlmostEqual(sum(influences.values()), 1.0, places=5)

    def test_apply_effects(self):
        tp = TriplePathway()
        from neural.neural_core import TwelveFactorNetwork
        net = TwelveFactorNetwork(TWELVE_FACTORS, dim=32)
        influences = tp.compute_influence(0.5, 100, 0.3)
        effects = tp.apply_pathway_effects(net, {}, influences)
        self.assertGreater(len(effects), 0)


class TestSpecialEntities(unittest.TestCase):
    """测试特殊实体"""

    def test_neikos_activation(self):
        neikos = NeiKos496()
        result = neikos.activate({})
        self.assertTrue(neikos.has_annihilated)
        self.assertTrue(neikos.logic_breach_created)

    def test_philia_erase(self):
        philia = PhiLia093()
        result = philia.erase()
        self.assertTrue(philia.is_erased)

    def test_trailblazer_activation(self):
        tb = Trailblazer()
        result = tb.activate({"time_pathway_vacant": True})
        self.assertTrue(tb.is_active)
        self.assertTrue(tb.has_taken_time_path)


class TestRecreationEngine(unittest.TestCase):
    """测试再创世引擎"""

    def test_check_trigger(self):
        re = RecreationEngine(threshold=0.8)
        self.assertTrue(re.check_trigger(0.9, 100, {"has_recreation": True}))
        self.assertFalse(re.check_trigger(0.5, 100, {"has_recreation": True}))
        self.assertFalse(re.check_trigger(0.9, 100, {"has_recreation": False}))

    def test_execute_recreation(self):
        re = RecreationEngine(threshold=0.8)
        result = re.execute_recreation(
            world_state={"total_entropy": 0.5},
            factor_network_state={"creation": {"potential_mean": 0.6}},
            agent_states={},
            titan_states={},
            phase="human"
        )
        self.assertEqual(re.recreation_count, 1)
        self.assertIn("generation", result)

    def test_get_stats(self):
        re = RecreationEngine(threshold=0.8)
        stats = re.get_recreation_stats()
        self.assertEqual(stats["total_recreations"], 0)


class TestSimulator(unittest.TestCase):
    """测试主模拟器"""

    def test_initialization(self):
        sim = AmphoreusSimulator(seed=42)
        self.assertEqual(sim.current_phase, "inorganic")
        self.assertEqual(sim.total_steps, 0)

    def test_run_short(self):
        sim = AmphoreusSimulator(seed=42)
        result = sim.run_simulation(max_steps=50, verbose=False)
        self.assertEqual(result["simulation_summary"]["total_steps"], 50)
        self.assertIn("destruction_equation_final", result)

    def test_save_logs(self):
        import tempfile
        sim = AmphoreusSimulator(seed=42)
        sim.run_simulation(max_steps=10, verbose=False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_log.json")
            sim.save_logs(path)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
