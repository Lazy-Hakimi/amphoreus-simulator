"""
Visualization Tools - 翁法罗斯模拟可视化
提供世界状态、黑潮扩散、命途平衡等可视化
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.colors import LinearSegmentedColormap
import json
from typing import Dict, List, Optional
from pathlib import Path

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False



class AmphoreusVisualizer:
    """
    翁法罗斯模拟可视化器
    """
    def __init__(self, output_dir: str = "logs/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 自定义颜色映射
        self.tide_cmap = LinearSegmentedColormap.from_list(
            "black_tide", ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#ff6b6b"]
        )

        # 泰坦颜色映射
        self.titan_colors = {
            "kephale": "#FFD700", "nicadore": "#DC143C", "aquila": "#87CEEB",
            "oroleus": "#9370DB", "phagousa": "#00CED1", "talanton": "#4169E1",
            "tholos": "#32CD32", "georios": "#8B4513", "mnestia": "#FF69B4",
            "Zagreus": "#2F4F4F", "cipher": "#FFA500", "thanatos": "#4B0082"
        }

    def plot_world_state(self, world_data: Dict, step: int, 
                        black_tide_concentration: np.ndarray,
                        titan_positions: Dict,
                        save: bool = True) -> plt.Figure:
        """
        绘制世界状态图

        包含：
        - 地形/文明密度
        - 黑潮扩散
        - 城邦位置
        - 泰坦位置
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # 1. 文明密度
        ax1 = axes[0]
        civ_density = world_data.get("civilization_density", np.zeros((100, 100)))
        im1 = ax1.imshow(civ_density, cmap="YlOrRd", vmin=0, vmax=1)
        ax1.set_title("文明密度场", fontsize=14, fontweight='bold')
        plt.colorbar(im1, ax=ax1, fraction=0.046)

        # 2. 黑潮浓度
        ax2 = axes[1]
        im2 = ax2.imshow(black_tide_concentration, cmap=self.tide_cmap, vmin=0, vmax=1)
        ax2.set_title("黑潮浓度场", fontsize=14, fontweight='bold')
        plt.colorbar(im2, ax=ax2, fraction=0.046)

        # 3. 综合视图
        ax3 = axes[2]
        # 背景：地形
        terrain = np.zeros((100, 100))
        for i in range(100):
            for j in range(100):
                terrain[i, j] = (np.sin(i * 0.1) * np.cos(j * 0.1) + 1) / 2
        ax3.imshow(terrain, cmap="terrain", alpha=0.3)

        # 叠加黑潮
        ax3.imshow(black_tide_concentration, cmap=self.tide_cmap, alpha=0.6)

        # 标记城邦
        cities = world_data.get("cities", {})
        for cid, city in cities.items():
            pos = city.get("position", (50, 50))
            color = "red" if city.get("is_fallen", False) else "green"
            marker = "x" if city.get("is_fallen", False) else "o"
            ax3.plot(pos[1], pos[0], marker=marker, color=color, markersize=12, 
                    markeredgecolor='black', markeredgewidth=2)
            ax3.annotate(city.get("name", cid), (pos[1], pos[0]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)

        # 标记泰坦
        for tid, pos in titan_positions.items():
            color = self.titan_colors.get(tid, "white")
            circle = Circle((pos[1], pos[0]), 3, color=color, alpha=0.8, 
                          ec='black', linewidth=2)
            ax3.add_patch(circle)

        ax3.set_title("综合世界视图", fontsize=14, fontweight='bold')
        ax3.set_xlim(0, 100)
        ax3.set_ylim(100, 0)

        plt.suptitle(f"翁法罗斯世界状态 - Step {step}", fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save:
            filepath = self.output_dir / f"world_state_step_{step:06d}.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

        return fig

    def plot_pathway_balance(self, pathway_history: List[Dict], 
                            save: bool = True) -> plt.Figure:
        """
        绘制命途平衡历史
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        steps = [h["step"] for h in pathway_history]
        erudition = [h["influences"]["erudition"] for h in pathway_history]
        nihility = [h["influences"]["nihility"] for h in pathway_history]
        remembrance = [h["influences"]["remembrance"] for h in pathway_history]

        ax.fill_between(steps, 0, erudition, alpha=0.7, label="智识 (Erudition)", color="#4169E1")
        ax.fill_between(steps, erudition, np.array(erudition) + np.array(nihility), 
                       alpha=0.7, label="毁灭 (Nihility)", color="#8B0000")
        ax.fill_between(steps, np.array(erudition) + np.array(nihility), 1, 
                       alpha=0.7, label="记忆 (Remembrance)", color="#9370DB")

        ax.set_xlabel("模拟步数", fontsize=12)
        ax.set_ylabel("命途影响力", fontsize=12)
        ax.set_title("三重命途影响力演变", fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)

        if save:
            filepath = self.output_dir / "pathway_balance.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

        return fig

    def plot_entropy_timeline(self, step_logs: List[Dict], 
                             save: bool = True) -> plt.Figure:
        """
        绘制熵值时间线
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        steps = [log["step"] for log in step_logs]

        # 1. 总熵
        ax1 = axes[0, 0]
        entropy = [log["total_entropy"] for log in step_logs]
        ax1.plot(steps, entropy, color='red', linewidth=1.5)
        ax1.set_title("世界总熵", fontsize=12, fontweight='bold')
        ax1.set_xlabel("步数")
        ax1.set_ylabel("熵值")
        ax1.grid(True, alpha=0.3)

        # 2. 崩溃度
        ax2 = axes[0, 1]
        collapse = [log["collapse_degree"] for log in step_logs]
        ax2.plot(steps, collapse, color='orange', linewidth=1.5)
        ax2.axhline(y=0.8, color='r', linestyle='--', label='再创世阈值')
        ax2.set_title("文明崩溃度", fontsize=12, fontweight='bold')
        ax2.set_xlabel("步数")
        ax2.set_ylabel("崩溃度")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. 黑潮最大值
        ax3 = axes[1, 0]
        tide_max = [log["black_tide_max"] for log in step_logs]
        ax3.plot(steps, tide_max, color='purple', linewidth=1.5)
        ax3.set_title("黑潮最大浓度", fontsize=12, fontweight='bold')
        ax3.set_xlabel("步数")
        ax3.set_ylabel("浓度")
        ax3.grid(True, alpha=0.3)

        # 4. 毁灭方程
        ax4 = axes[1, 1]
        dest_eq = [log["destruction_equation"] for log in step_logs]
        ax4.plot(steps, dest_eq, color='darkred', linewidth=1.5)
        ax4.set_title("毁灭方程值", fontsize=12, fontweight='bold')
        ax4.set_xlabel("步数")
        ax4.set_ylabel("方程值")
        ax4.grid(True, alpha=0.3)

        plt.suptitle("翁法罗斯核心指标时间线", fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save:
            filepath = self.output_dir / "entropy_timeline.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

        return fig

    def plot_recreation_stats(self, recreation_logs: List[Dict],
                             save: bool = True) -> plt.Figure:
        """
        绘制再创世统计
        """
        if not recreation_logs:
            return None

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        loops = [log["loop_number"] for log in recreation_logs]

        # 1. 熵变化
        ax1 = axes[0]
        entropy_before = [log["entropy_before"] for log in recreation_logs]
        entropy_after = [log["entropy_after"] for log in recreation_logs]

        ax1.plot(loops, entropy_before, 'o-', label="再创世前", color='red')
        ax1.plot(loops, entropy_after, 's-', label="再创世后", color='green')
        ax1.set_title("再创世前后熵值对比", fontsize=12, fontweight='bold')
        ax1.set_xlabel("再创世次数")
        ax1.set_ylabel("熵值")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 毁灭方程进展
        ax2 = axes[1]
        dest_eq = [log["destruction_equation_value"] for log in recreation_logs]
        ax2.plot(loops, dest_eq, 'D-', color='darkred', linewidth=2)
        ax2.set_title("毁灭方程进展", fontsize=12, fontweight='bold')
        ax2.set_xlabel("再创世次数")
        ax2.set_ylabel("方程值")
        ax2.grid(True, alpha=0.3)

        plt.suptitle("再创世统计分析", fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save:
            filepath = self.output_dir / "recreation_stats.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

        return fig

    def generate_summary_dashboard(self, final_report: Dict,
                                   save: bool = True) -> plt.Figure:
        """
        生成最终摘要仪表盘
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 标题
        fig.suptitle("翁法罗斯模拟实验最终报告", fontsize=20, fontweight='bold', y=0.98)

        # 1. 基本信息
        ax_info = fig.add_subplot(gs[0, 0])
        ax_info.axis('off')
        summary = final_report.get("simulation_summary", {})
        info_text = f"""
        模拟摘要
        ─────────────
        总步数: {summary.get('total_steps', 0)}
        总循环: {summary.get('total_loops', 0)}
        最终阶段: {summary.get('final_phase', 'unknown')}
        运行时间: {summary.get('elapsed_seconds', 0):.2f}s
        终止状态: {'已完成' if summary.get('is_terminal') else '未终止'}
        """
        ax_info.text(0.1, 0.5, info_text, fontsize=11, family=['monospace', 'SimHei', 'DejaVu Sans'],
                    verticalalignment='center')

        # 2. 最终世界状态
        ax_world = fig.add_subplot(gs[0, 1])
        world = final_report.get("final_world_state", {})
        metrics = ['人口', '熵值', '崩溃度']
        values = [
            world.get('total_population', 0) / 100000,
            world.get('total_entropy', 0),
            world.get('collapse_degree', 0)
        ]
        colors = ['green', 'red', 'orange']
        bars = ax_world.bar(metrics, values, color=colors, alpha=0.7)
        ax_world.set_title("最终世界指标", fontsize=12, fontweight='bold')
        ax_world.set_ylim(0, 1.2)
        for bar, val in zip(bars, values):
            ax_world.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                         f'{val:.3f}', ha='center', fontsize=10)

        # 3. 命途平衡
        ax_path = fig.add_subplot(gs[0, 2])
        pathway = final_report.get("pathway_balance", {})
        influences = pathway.get("influences", {})
        if influences:
            labels = list(influences.keys())
            sizes = list(influences.values())
            colors_pie = ['#4169E1', '#8B0000', '#9370DB']
            ax_path.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                       startangle=90)
            ax_path.set_title("命途影响力分布", fontsize=12, fontweight='bold')

        # 4. 泰坦状态
        ax_titan = fig.add_subplot(gs[1, :])
        titans = final_report.get("titan_states", {})
        titan_names = []
        titan_powers = []
        titan_alive = []
        for tid, state in titans.items():
            titan_names.append(state.get('name', tid))
            titan_powers.append(state.get('divine_power', 0))
            titan_alive.append(state.get('is_alive', False))

        colors_titan = ['green' if a else 'red' for a in titan_alive]
        bars = ax_titan.barh(titan_names, titan_powers, color=colors_titan, alpha=0.7)
        ax_titan.set_title("十二泰坦神权状态", fontsize=12, fontweight='bold')
        ax_titan.set_xlabel("神权强度")
        ax_titan.set_xlim(0, 1.2)
        for bar, val in zip(bars, titan_powers):
            ax_titan.text(val + 0.02, bar.get_y() + bar.get_height()/2,
                         f'{val:.3f}', va='center', fontsize=9)

        # 5. 因子状态
        ax_factor = fig.add_subplot(gs[2, :2])
        factors = final_report.get("factor_states", {})
        factor_names = []
        potentials = []
        golden_bloods = []
        for fname, fstate in factors.items():
            factor_names.append(fname)
            potentials.append(abs(fstate.get('potential_mean', 0)))
            golden_bloods.append(fstate.get('golden_blood', 0))

        x = np.arange(len(factor_names))
        width = 0.35
        ax_factor.bar(x - width/2, potentials, width, label='电位强度', alpha=0.7)
        ax_factor.bar(x + width/2, golden_bloods, width, label='金血浓度', alpha=0.7, color='red')
        ax_factor.set_title("十二因子状态", fontsize=12, fontweight='bold')
        ax_factor.set_xticks(x)
        ax_factor.set_xticklabels(factor_names, rotation=45, ha='right')
        ax_factor.legend()

        # 6. 毁灭方程最终值
        ax_dest = fig.add_subplot(gs[2, 2])
        ax_dest.axis('off')
        dest_val = final_report.get("destruction_equation_final", 0)
        dest_text = f"""
        毁灭方程
        ─────────────
        最终值: {dest_val:.6f}

        解释:
        值越高代表系统
        越接近毁灭的
        终极解。
        """
        color = 'red' if dest_val > 0.7 else 'orange' if dest_val > 0.4 else 'green'
        ax_dest.text(0.5, 0.5, dest_text, fontsize=11, family=['monospace', 'SimHei', 'DejaVu Sans'],
                    verticalalignment='center', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))

        if save:
            filepath = self.output_dir / "final_dashboard.png"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

        return fig
