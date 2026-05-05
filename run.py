#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amphoreus Simulator Launcher
翁法罗斯世界模拟器启动脚本

使用方法:
    python run.py [options]

示例:
    python run.py --steps 5000 --seed 42 --verbose
    python run.py --quick-test
    python run.py --full-simulation
"""

import argparse
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import NeuralConfig, SimulationConfig
from core.main_simulator import AmphoreusSimulator
from utils.visualization import AmphoreusVisualizer
import json


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="翁法罗斯世界模拟器 - 基于《崩坏：星穹铁道》世界观",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
实验阶段说明:
  inorganic      - 无机阶段: 50121次循环，无机变量
  organic        - 有机阶段: 176199次循环，有机变量
  human          - 人类阶段: 28371273次循环，加入记忆继承
  recreation     - 再创世阶段: 黑潮推动世界更迭
  eternal_return - 永劫回归: 死循环，NeiKos496与PhiLia093
  final_loop     - 最终循环: 外来变量介入
  conclusion     - 结论: 求解毁灭方程

示例:
  python run.py --quick-test                    # 快速测试（500步）
  python run.py --full-simulation               # 完整模拟
  python run.py --steps 10000 --seed 123        # 自定义步数
  python run.py --phase human --steps 5000      # 从指定阶段开始
        """
    )

    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=5000,
        help="最大模拟步数 (默认: 5000)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="随机种子 (默认: 42)"
    )

    parser.add_argument(
        "--phase",
        type=str,
        default="inorganic",
        choices=["inorganic", "organic", "human", "recreation", 
                "eternal_return", "final_loop", "conclusion"],
        help="起始实验阶段 (默认: inorganic)"
    )

    parser.add_argument(
        "--world-size",
        type=int,
        nargs=2,
        default=[100, 100],
        metavar=("H", "W"),
        help="世界网格大小 (默认: 100 100)"
    )

    parser.add_argument(
        "--recreation-threshold",
        type=float,
        default=0.8,
        help="再创世触发阈值 (默认: 0.8)"
    )

    parser.add_argument(
        "--log-interval",
        type=int,
        default=100,
        help="日志打印间隔 (默认: 100步)"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="计算设备 (默认: cpu)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="启用详细日志输出"
    )

    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="快速测试模式 (500步)"
    )

    parser.add_argument(
        "--full-simulation",
        action="store_true",
        help="完整模拟模式 (尝试运行全部阶段)"
    )

    parser.add_argument(
        "--save-logs",
        action="store_true",
        default=True,
        help="保存模拟日志"
    )

    parser.add_argument(
        "--save-report",
        action="store_true",
        default=True,
        help="保存最终报告"
    )

    parser.add_argument(
        "--visualize",
        action="store_true",
        help="生成可视化图表"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="logs",
        help="输出目录 (默认: logs)"
    )

    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    # 处理快捷模式
    if args.quick_test:
        args.steps = 500
        args.log_interval = 50
        print("[模式] 快速测试模式")

    if args.full_simulation:
        args.steps = 1000000
        args.log_interval = 1000
        print("[模式] 完整模拟模式")

    # 构建配置
    neural_config = NeuralConfig(
        device=args.device
    )

    sim_config = SimulationConfig(
        world_size=tuple(args.world_size),
        recreation_threshold=args.recreation_threshold,
        log_interval=args.log_interval,
        seed=args.seed
    )

    print(f"\n{'='*60}")
    print("  翁法罗斯世界模拟器 v1.0")
    print(f"{'='*60}")
    print(f"  配置参数:")
    print(f"    - 最大步数: {args.steps}")
    print(f"    - 随机种子: {args.seed}")
    print(f"    - 起始阶段: {args.phase}")
    print(f"    - 世界大小: {args.world_size}")
    print(f"    - 再创世阈值: {args.recreation_threshold}")
    print(f"    - 日志间隔: {args.log_interval}")
    print(f"    - 计算设备: {args.device}")
    print(f"{'='*60}\n")

    # 创建并运行模拟器
    simulator = AmphoreusSimulator(
        neural_config=neural_config,
        sim_config=sim_config,
        seed=args.seed
    )

    # 设置起始阶段
    simulator.current_phase = args.phase

    try:
        # 运行模拟
        result = simulator.run_simulation(
            max_steps=args.steps,
            verbose=args.verbose
        )

        # 保存日志
        if args.save_logs:
            log_path = os.path.join(args.output_dir, "simulation_log.json")
            simulator.save_logs(filepath=log_path)

        # 保存报告
        if args.save_report:
            report_path = os.path.join(args.output_dir, "final_report.json")
            simulator.save_report(filepath=report_path)

        # 生成可视化
        if args.visualize:
            print("\n[可视化] 正在生成图表...")
            visualizer = AmphoreusVisualizer(
                output_dir=os.path.join(args.output_dir, "visualizations")
            )

            # 生成摘要仪表盘
            visualizer.generate_summary_dashboard(result)

            # 生成熵值时间线
            if simulator.step_logs:
                visualizer.plot_entropy_timeline(simulator.step_logs)

            # 生成再创世统计
            if simulator.recreation_engine.logs:
                visualizer.plot_recreation_stats(
                    [log.__dict__ for log in simulator.recreation_engine.logs]
                )

            print("[可视化] 图表生成完成")

        # 打印最终结果摘要
        print(f"\n{'='*60}")
        print("  模拟结果摘要")
        print(f"{'='*60}")
        summary = result.get("simulation_summary", {})
        print(f"  总步数: {summary.get('total_steps', 0)}")
        print(f"  总循环: {summary.get('total_loops', 0)}")
        print(f"  最终阶段: {summary.get('final_phase', 'unknown')}")
        print(f"  毁灭方程最终值: {result.get('destruction_equation_final', 0):.6f}")

        world = result.get("final_world_state", {})
        print(f"  最终人口: {world.get('total_population', 0)}")
        print(f"  最终熵值: {world.get('total_entropy', 0):.4f}")
        print(f"  崩溃度: {world.get('collapse_degree', 0):.4f}")

        pathway = result.get("pathway_balance", {})
        print(f"  主导命途: {pathway.get('dominant', 'unknown')}")
        print(f"{'='*60}")

    except KeyboardInterrupt:
        print("\n[中断] 模拟被用户中断")

        # 保存中断时的状态
        if args.save_report:
            report_path = os.path.join(args.output_dir, "interrupted_report.json")
            simulator.save_report(filepath=report_path)

    except Exception as e:
        print(f"\n[错误] 模拟运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
