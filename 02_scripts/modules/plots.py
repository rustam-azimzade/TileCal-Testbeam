import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import logging
from .config import Config
from pathlib import Path
from datetime import datetime, timezone
import os
import atlas_mpl_style as ampl
from matplotlib.ticker import MaxNLocator


logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logging.getLogger('fontTools').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class Plots:
    def __init__(self):
        self._set_plot_style()

        self._current_figure = None
        self._current_plot_name = None

    def _set_plot_style(self):
        ampl.use_atlas_style(atlasLabel="ATLAS", usetex=False, fancyLegend=False,)
        ampl.set_color_cycle(pal='Petroff')
        plt.rcParams.update({
            'figure.dpi': 300,
            'figure.facecolor': "white",
            'figure.edgecolor': "white",
            'savefig.dpi': 300,
            'savefig.bbox': 'tight',
            'savefig.pad_inches': 0.05,
            'pdf.fonttype': 42,
            'ps.fonttype': 42,
            'svg.fonttype': 'none',
            'savefig.transparent': False,
            'savefig.facecolor': "white",
            'savefig.edgecolor': "white",

            "axes.grid": True,
            "axes.grid.axis": "both",
            "axes.grid.which": "major",
            "grid.color": Config.COLORS["gray"],
            "grid.linestyle": "--",
            "grid.linewidth": 0.5,
            "grid.alpha": 0.25,

            'axes.autolimit_mode': 'data',
            #"axes.xmargin": 0.05,
            #"axes.ymargin": 0.05,
            #"axes.formatter.useoffset": False,

            'xaxis.labellocation': 'right',
            'yaxis.labellocation': 'top',

            'boxplot.medianprops.linewidth': 1.5,
            'boxplot.medianprops.color': Config.COLORS["atlas:blue"],
        })

    def _add_technical_label(
            self,
            run_number: str,
            module_name: str,
            add_space: bool = False,
            expansion_factor=1.4,
            location=Config.TECHNICAL_INFO_LOCATION,
    ):
        run_info = Config.RUNS_DESCRIPTION[run_number]

        info_text = (
            rf'$\mathit{{TestBeam}},\ \mathbf{{Run\ {run_number}}}$'
            '\n'
            rf'Beam: {run_info["particle_type"]}, $E={run_info["energy"]}\,\mathrm{{GeV}}$'
            '\n'
            rf'Module: {module_name}'
            '\n'
            rf'$\theta={run_info["impact_angle"]}^\circ$, $\Delta Z({run_info["cell"]})={run_info["delta_Z"]}\,[\mathrm{{mm}}]$'
        )

        axis = self._current_figure.axes[0]

        if add_space:
            # Add some free space at the top
            ymin, ymax = axis.get_ylim()
            axis.set_ylim(ymin, ymax * expansion_factor)

        # Add information
        axis.text(
            location[0],
            location[1],
            info_text,
            transform=axis.transAxes,
            fontweight="normal",
            verticalalignment="top",
            horizontalalignment="left",
            multialignment="left",
            clip_on=False,
            bbox=dict(
                boxstyle="square,pad=0.25",
                facecolor="white",
                edgecolor="none",
                alpha=0.9
            ),
            zorder=10,
        )


    @staticmethod
    def units_processing(
            events: np.ndarray,
            mode: str,
            baseline_unit: str,
            target_unit: str = None,
    ):
        if mode not in Config.UNIT_SYSTEMS:
            raise ValueError(
                f"Unknown physical quantity: {mode}. "
                f"Available modes: {list(Config.UNIT_SYSTEMS)}"
            )

        units = Config.UNIT_SYSTEMS[mode]

        # copying an array to avoid accidental modifications via a reference
        events = np.asarray(events)
        events_processed = events.copy()

        baseline_scale = units[baseline_unit]

        if target_unit is not None:
            if target_unit == baseline_unit:
                return events_processed, baseline_unit

            target_scale = units[target_unit]

            conversion_factor = baseline_scale / target_scale
            events_processed *= conversion_factor

            return events_processed, target_unit

        max_value = np.max(np.abs(events_processed))
        if max_value == 0:
            return events_processed, baseline_unit

        lower_limit = 10.0 ** (Config.POWER_LIMITS[0] + 1)
        upper_limit = 10.0 ** (Config.POWER_LIMITS[1] - 1)

        sorted_units = sorted(
            units.items(),
            key=lambda item: item[1]
        )

        # Find the first suitable unit
        for unit, unit_scale in sorted_units:
            conversion_factor = baseline_scale / unit_scale
            converted_max = max_value * conversion_factor

            if lower_limit <= converted_max <= upper_limit:
                events_processed *= conversion_factor
                return events_processed, unit

        return events_processed, baseline_unit


    def plot_two_histograms(
            self,
            run_number: str,
            variable1: np.ndarray,
            variable2: np.ndarray,
            label1: str,
            label2: str,
            xlabel: str,
            ylabel: str,
            bins=None,
            baseline_unit: str = "MeV",
            module_name: str = "",
            additional_info: str = None,
            plot_name: str = "histograms",
            show_statistics: bool = True,
            zoom: bool = False,
            xlim_quantiles: tuple[float, float] = (0.0, 0.997),
            show_boxplots: bool = False,
    ):
        variable1_visible = np.asarray(variable1).copy()
        variable2_visible = np.asarray(variable2).copy()

        combined_values = np.concatenate([variable1_visible, variable2_visible])

        if zoom:
            variable_min, variable_max = np.quantile(combined_values, xlim_quantiles)

            variable1_visible_condition = (variable1_visible <= variable_max) & (variable1_visible >= variable_min)
            variable1_visible = variable1_visible[variable1_visible_condition]

            variable2_visible_condition = (variable2_visible <= variable_max) & (variable2_visible >= variable_min)
            variable2_visible = variable2_visible[variable2_visible_condition]

            visible_values = np.concatenate([variable1_visible, variable2_visible])
        else:
            visible_values = combined_values

        # FIND OPTIMAL UNIT
        _, common_unit = self.units_processing(
            events=visible_values,
            mode="energy",
            baseline_unit=baseline_unit,
            target_unit=None,
        )
        variable1_visible, _ = self.units_processing(
            events=variable1_visible,
            mode="energy",
            baseline_unit=baseline_unit,
            target_unit=common_unit,
        )
        variable2_visible, _ = self.units_processing(
            events=variable2_visible,
            mode="energy",
            baseline_unit=baseline_unit,
            target_unit=common_unit,
        )
        variable1, _ = self.units_processing(
            events=variable1,
            mode="energy",
            baseline_unit=baseline_unit,
            target_unit=common_unit,
        )
        variable2, _ = self.units_processing(
            events=variable2,
            mode="energy",
            baseline_unit=baseline_unit,
            target_unit=common_unit,
        )

        combined_values = np.concatenate([variable1, variable2])
        visible_values = np.concatenate([variable1_visible, variable2_visible])

        if bins is None:
            bins = np.histogram_bin_edges(
                combined_values,
                bins='scott',
            )

        if show_boxplots:
            figure, (histogram_axis, boxplot_axis) = plt.subplots(
                figsize=(Config.PLOT_SIZE[0], Config.PLOT_SIZE[1] * ( (4.0 + 1.5 + 0.05) / 4.0)),
                nrows=2,
                ncols=1,
                sharex=True,
                gridspec_kw={
                    "height_ratios": (4.0, 1.5),
                    "hspace": 0.05,
                },
            )
        else:
            figure, histogram_axis = plt.subplots()
            boxplot_axis = None

        # HISTOGRAM
        histogram_axis.hist(
            variable1_visible,
            bins=bins,
            color=Config.COLORS["atlas:lightBlue"],
            label=label1,
            zorder=1,
        )
        if show_statistics:
            histogram_axis.plot([], [], ' ', label=f'Events: {variable1.size:,}')
            histogram_axis.plot([], [], ' ', label=f'Median: {np.median(variable1):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Mean: {np.average(variable1):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Std: {np.std(variable1):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Min: {np.min(variable1):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Max: {np.max(variable1):,.3f}')
        histogram_axis.hist(
            variable2_visible,
            bins=bins,
            histtype="step",
            color=Config.COLORS["petroff:red"],
            linewidth=1.2,
            hatch="//",
            label=label2,
            zorder=2,
        )
        if show_statistics:
            histogram_axis.plot([], [], ' ', label=f'Events: {variable2.size:,}')
            histogram_axis.plot([], [], ' ', label=f'Median: {np.median(variable2):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Mean: {np.average(variable2):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Std: {np.std(variable2):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Min: {np.min(variable2):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Max: {np.max(variable2):,.3f}')
        if additional_info is not None:
            histogram_axis.set_title(additional_info)
            # Добавить с помощью histogram_axis.text и выяснить можно ли автоматически подобрать наилучшее расположение
        histogram_axis.legend(fontsize=("small" if show_statistics else None),)
        histogram_axis.set_ylabel(ylabel,)

        # BOXPLOTS
        if boxplot_axis is not None:
            boxplot = boxplot_axis.boxplot(
                [variable1, variable2],
                vert=False,
                widths=0.55,
            )
            boxplot['medians'][0].set_color(Config.COLORS["atlas:lightBlue"])
            boxplot['medians'][1].set_color(Config.COLORS["petroff:red"])
            boxplot_axis.tick_params(
                which='minor',
                right=False,
                left=False,
            )
            boxplot_axis.set_yticks([1, 2], [label1, label2], rotation=30)
            boxplot_axis.invert_yaxis()

        lower_axis = boxplot_axis if boxplot_axis is not None else histogram_axis
        lower_axis.set_xlabel(f"{xlabel} [{common_unit}]",)
        if zoom:
            locator = MaxNLocator(nbins=10,)
            ticks = locator.tick_values(visible_values.min(), visible_values.max())

            lower_axis.set_xlim((ticks[0], ticks[-1]))
            lower_axis.xaxis.set_major_locator(locator)
            #lower_axis.set_xlim((visible_values.min(), visible_values.max()))

        self._current_figure = figure
        self._current_plot_name = plot_name
        self._add_technical_label(
            run_number=run_number,
            module_name=module_name,
            add_space=True,
            expansion_factor=1.4,
        )

        return self


    def plot_histogram(
            self,
            run_number: str,
            events: np.ndarray,
            xunit: str,
            xlabel: str,
            ylabel: str,
            bins = None,
            label: str = "",
            module_name: str = "",
            plot_name: str = "histogram",
            show_statistics: bool = False,
            show_boxplot: bool = True,
    ):
        if bins is None:
            bins = np.histogram_bin_edges(events, bins='scott')

        if show_boxplot:
            figure, (histogram_axis, boxplot_axis) = plt.subplots(
                figsize=(Config.PLOT_SIZE[0], Config.PLOT_SIZE[1] * ( (4.0 + 1.0 + 0.05) / 4.0)),
                nrows=2,
                ncols=1,
                sharex=True,
                gridspec_kw={
                    "height_ratios": (4.0, 1.0),
                    "hspace": 0.05,
                },
            )
        else:
            figure, histogram_axis = plt.subplots(figsize=Config.PLOT_SIZE)
            boxplot_axis = None
        # HISTOGRAM
        histogram_axis.hist(
            events,
            bins=bins,
            color=Config.COLORS["atlas:blue"],
            label=label if label else None,
        )
        if show_statistics:
            histogram_axis.plot([], [], ' ', label=f'Events: {events.size:,}')
            histogram_axis.plot([], [], ' ', label=f'Median: {np.median(events):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Mean: {np.average(events):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Std: {np.std(events):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Min: {np.min(events):,.3f}')
            histogram_axis.plot([], [], ' ', label=f'Max: {np.max(events):,.3f}')
        if label:
            histogram_axis.legend()
        histogram_axis.set_ylabel(ylabel,)

        # BOXPLOT
        if boxplot_axis is not None:
            boxplot_axis.boxplot(
                events,
                vert=False,
                widths=0.55,
                medianprops={
                    'color': Config.COLORS["atlas:blue"],
                }
            )
            boxplot_axis.set_yticks([])

        lower_axis = boxplot_axis if boxplot_axis is not None else histogram_axis
        lower_axis.set_xlabel(f"{xlabel} [{xunit}]",)

        self._current_figure = figure
        self._current_plot_name = plot_name
        self._add_technical_label(
            run_number=run_number,
            module_name=module_name,
            add_space=True,
            expansion_factor=1.4,
        )

        return self


    def _create_save_dirs(self, save_path):
        os.makedirs(os.path.join(save_path, '01_png'), exist_ok=True)
        os.makedirs(os.path.join(save_path, '02_pdf'), exist_ok=True)


    def save_plot(self, save_path='/', plot_name=None):
        if self._current_figure is None:
            raise RuntimeError("No figure to save. Generate a plot first.")

        name = plot_name or self._current_plot_name
        if name is None:
            raise ValueError("Plot name must be specified.")

        # Create timestamp
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        name = f'{name}_{timestamp}'

        path = Path(save_path)
        self._create_save_dirs(save_path=path)

        png_path = os.path.join(path, '01_png', f'{name}.png')
        pdf_path = os.path.join(path, '02_pdf', f'{name}.pdf')

        self._current_figure.savefig(png_path, dpi=300)
        self._current_figure.savefig(pdf_path)
        plt.close(self._current_figure)

        self._current_figure = None
        self._current_plot_name = None