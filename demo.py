#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amphoreus Simulator Interactive Demo
翁法罗斯模拟器交互式演示

运行方式:
    python demo.py

功能:
    - 分步展示模拟过程
    - 实时查看各子系统状态
    - 手动触发特殊事件
    - 导出当前状态
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import NeuralConfig, SimulationConfig, TITAN_CONFIG, EXPERIMENT_PHASES
from core.main_simulator import AmphoreusSimulator
from utils.visualization import AmphoreusVisualizer
import json


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_subheader(text):
    print(f"\n{'─'*50}")
    print(f"  {text}")
    print(f"{'─'*50}")


def demo_basic_simulation():
    """演示1: 基础模拟"""
    print_header("演示1: 基础模拟 (500步)")

    sim = AmphoreusSimulator(seed=42)
    result = sim.run_simulation(max_steps=500, verbose=False)

    print_subheader("模拟结果")
    print(f"  总步数: {result['simulation_summary']['total_steps']}")
    print(f"  最终阶段: {result['simulation_summary']['final_phase']}")
    print(f"  毁灭方程最终值: {result['destruction_equation_final']:.6f}")
    print(f"  最终人口: {result['final_world_state']['total_population']}")
    print(f"  最终熵值: {result['final_world_state']['total_entropy']:.4f}")
    print(f"  崩溃度: {result['final_world_state']['collapse_degree']:.4f}")
    print(f"  主导命途: {result['pathway_balance']['dominant']}")

    return sim, result


def demo_phase_transition():
    """演示2: 阶段转换"""
    print_header("演示2: 阶段转换演示")

    sim = AmphoreusSimulator(seed=42)

    phases = ["inorganic", "organic", "human"]
    for phase in phases:
        sim.current_phase = phase
        sim.phase_loop_count = 0
        print_subheader(f"阶段: {phase}")
        print(f"  描述: {EXPERIMENT_PHASES[phase]['name']}")
        print(f"  最大循环: {EXPERIMENT_PHASES[phase]['max_loops']:,}")
        print(f"  记忆继承: {EXPERIMENT_PHASES[phase]['has_memory_inheritance']}")
        print(f"  黑潮: {EXPERIMENT_PHASES[phase]['has_black_tide']}")
        print(f"  再创世: {EXPERIMENT_PHASES[phase]['has_recreation']}")

        # 运行50步
        result = sim.run_simulation(max_steps=50, verbose=False)
        print(f"  50步后人口: {result['final_world_state']['total_population']}")
        print(f"  50步后熵值: {result['final_world_state']['total_entropy']:.4f}")


def demo_special_entities():
    """演示3: 特殊实体事件"""
    print_header("演示3: 特殊实体事件")

    sim = AmphoreusSimulator(seed=42)

    print_subheader("激活白厄 (NeiKos496)")
    neikos = sim.entity_manager.entities["NeiKos496"]
    result = neikos.activate({"time_pathway_vacant": False})
    print(f"  事件: {result['event']}")
    print(f"  逻辑漏洞: {result['effects']['time_pathway_breach']}")
    print(f"  昔涟被抹除: {result['effects']['phiLia093_erased']}")

    print_subheader("激活开拓者 (Trailblazer)")
    trailblazer = sim.entity_manager.entities["Trailblazer"]
    result = trailblazer.activate({"time_pathway_vacant": True})
    print(f"  事件: {result['event']}")
    print(f"  岁月路径接替: {result['effects']['time_pathway_substituted']}")

    print_subheader("引导跨越奇点")
    crossing = trailblazer.guide_neikos(neikos)
    print(f"  结果: {crossing['status']}")
    print(f"  描述: {crossing.get('description', 'N/A')}")


def demo_titan_system():
    """演示4: 泰坦与黄金裔"""
    print_header("演示4: 泰坦与黄金裔系统")

    sim = AmphoreusSimulator(seed=42)

    print_subheader("十二泰坦状态")
    for tid, titan in sim.titan_system.titans.items():
        state = titan.get_state()
        status = "存活" if state['is_alive'] else "陨落"
        print(f"  {state['name']:12s} ({tid:12s}) | 状态: {status} | 神权: {state['divine_power']:.2f}")

    print_subheader("生成黄金裔")
    agent = sim.titan_system.spawn_golden_blood(
        "okhema", "agent_001", "阿格莱雅", ["creation", "romance"]
    )
    print(f"  名称: {agent.name}")
    print(f"  起源城邦: {agent.city_of_origin}")
    print(f"  因子亲和: {agent.factor_affinity}")
    print(f"  金血浓度: {agent.golden_blood_level:.3f}")
    print(f"  战力: {agent.combat_power:.3f}")

    print_subheader("泰坦受到伤害")
    titan = sim.titan_system.titans["nicadore"]
    titan.take_damage(0.8, source="agent_001")
    print(f"  尼卡多利受到伤害后: {'存活' if titan.is_alive else '陨落'}")
    print(f"  剩余神权: {titan.divine_power:.3f}")


def demo_recreation():
    """演示5: 再创世机制"""
    print_header("演示5: 再创世机制")

    sim = AmphoreusSimulator(seed=42)
    sim.current_phase = "recreation"

    print_subheader("运行至再创世触发")
    result = sim.run_simulation(max_steps=2000, verbose=False)

    print_subheader("再创世统计")
    stats = sim.recreation_engine.get_recreation_stats()
    print(f"  总再创世次数: {stats['total_recreations']}")
    print(f"  平均再创世前熵: {stats.get('average_entropy_before', 0):.4f}")
    print(f"  平均再创世后熵: {stats.get('average_entropy_after', 0):.4f}")
    print(f"  记忆归档大小: {stats.get('memory_archive_size', 0)}")

    if stats['total_recreations'] > 0:
        print_subheader("毁灭方程趋势")
        trend = stats.get('destruction_equation_trend', [])
        for i, val in enumerate(trend[:5]):
            print(f"  第{i+1}次再创世: {val:.6f}")


def demo_pathways():
    """演示6: 三重命途"""
    print_header("演示6: 三重命途交互")

    sim = AmphoreusSimulator(seed=42)

    print_subheader("初始命途平衡")
    balance = sim.pathways.get_pathway_balance()
    for name, inf in balance['influences'].items():
        print(f"  {name:15s}: {inf:.3f}")
    print(f"  主导命途: {balance['dominant']}")

    print_subheader("模拟过程中的命途演变")
    sim.run_simulation(max_steps=200, verbose=False)

    # 从日志中提取命途变化
    pathway_history = []
    for log in sim.step_logs:
        if 'pathway_dominant' in log:
            pathway_history.append(log['pathway_dominant'])

    if pathway_history:
        from collections import Counter
        counts = Counter(pathway_history)
        print("  各命途主导次数:")
        for name, count in counts.most_common():
            print(f"    {name}: {count} 次 ({count/len(pathway_history)*100:.1f}%)")


def demo_export():
    """演示7: 数据导出"""
    print_header("演示7: 数据导出")

    sim = AmphoreusSimulator(seed=42)
    sim.run_simulation(max_steps=100, verbose=False)

    output_dir = "demo_output"
    os.makedirs(output_dir, exist_ok=True)

    # 导出日志
    log_path = os.path.join(output_dir, "demo_log.json")
    sim.save_logs(log_path)
    print(f"  日志已导出: {log_path}")

    # 导出报告
    report_path = os.path.join(output_dir, "demo_report.json")
    sim.save_report(report_path)
    print(f"  报告已导出: {report_path}")

    # 生成可视化
    print_subheader("生成可视化图表")
    vis = AmphoreusVisualizer(output_dir=os.path.join(output_dir, "visualizations"))

    result = sim._generate_final_report(0)
    vis.generate_summary_dashboard(result)
    print(f"  仪表盘: {output_dir}/visualizations/final_dashboard.png")

    if sim.step_logs:
        vis.plot_entropy_timeline(sim.step_logs)
        print(f"  熵值时间线: {output_dir}/visualizations/entropy_timeline.png")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           翁法罗斯世界模拟器 - 交互式演示                      ║
║           Amphoreus Simulator - Interactive Demo             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    demos = {
        "1": ("基础模拟", demo_basic_simulation),
        "2": ("阶段转换", demo_phase_transition),
        "3": ("特殊实体", demo_special_entities),
        "4": ("泰坦与黄金裔", demo_titan_system),
        "5": ("再创世机制", demo_recreation),
        "6": ("三重命途", demo_pathways),
        "7": ("数据导出", demo_export),
        "0": ("全部演示", None),
    }

    while True:
        print("\n请选择演示项目:")
        for key, (name, _) in demos.items():
            print(f"  [{key}] {name}")
        print("  [q] 退出")

        choice = input("\n输入选项: ").strip().lower()

        if choice == "q":
            print("\n感谢使用翁法罗斯模拟器。愿此行，终抵群星。")
            break
        elif choice == "0":
            for key, (name, func) in demos.items():
                if key != "0" and func:
                    try:
                        func()
                    except Exception as e:
                        print(f"[错误] {name} 演示失败: {e}")
        elif choice in demos:
            try:
                demos[choice][1]()
            except Exception as e:
                print(f"[错误] 演示失败: {e}")
        else:
            print("[提示] 无效选项，请重新输入")


if __name__ == "__main__":
    main()
