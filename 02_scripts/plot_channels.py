import uproot
import numpy as np
from modules import Plots, Config
import logging

# 30 mm < Ximp_0 / cos (20 deg) < -30 mm, 30 mm < Yimp_0 < -30 mm

def get_first_tree(root_file):
    first_tree_name = next(
        (object_name for object_name, object_class in root_file.classnames().items()
         if object_class.startswith("TTree")),
        None
    )
    return root_file[first_tree_name]


logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    level=logging.INFO
)
logging.getLogger('fontTools').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    run_number = "2510758"
    file_path = f"{Config.DATA_PATH}/experiment/tiletb_{run_number}.root"

    plotter = Plots()

    with uproot.open(file_path) as file:
        tree = get_first_tree(root_file=file)

        # PLOT EACH CHANNEL FOR EACH RECONSTRUCTION METHOD
        # for reconstruction_method_encoding in Config.RECONSTRUCTION_METHOD_ENCODINGS:
        #     logger.info(f"Reconstruction Method: {reconstruction_method_encoding}")
        #     for module_encoding, module_name in Config.MODULE_ENCODINGS.items():
        #         logger.info(f"\tModule Name: {module_name}")
        #         variable_name = f"E{reconstruction_method_encoding}{module_encoding}"
        #
        #         reconstructed_energy = tree[variable_name]
        #         reconstructed_energy_data = reconstructed_energy.array(library="np")
        #
        #         for channel_index, channel_data in enumerate(reconstructed_energy_data.T):
        #             logger.info(f"\t\tChannel Index: {channel_index}")
        #
        #             channel_data, channel_data_unit = units_processing(
        #                 events=channel_data,
        #                 mode="energy",
        #                 baseline_unit="MeV",
        #             )
        #
        #             reconstructed_channel_energy_plot = plotter.plot_histogram(
        #                 run_number=run_number,
        #                 events=channel_data,
        #                 xlabel="Reconstructed Energy",
        #                 xunit=channel_data_unit,
        #                 ylabel="Events",
        #                 label=f"Channel Index {channel_index}",
        #                 module_name=module_name,
        #                 plot_name=f"{module_name}_ch{channel_index}_histogram",
        #                 show_statistics=True,
        #                 show_boxplot=True,
        #             )
        #             save_path = f"../03_results/runs/{run_number}/energies/{reconstruction_method_encoding}/modules/{module_name}/channels/"
        #             reconstructed_channel_energy_plot.save_plot(save_path=save_path)


        # PLOT EACH CHANNEL WITH EACH RECONSTRUCTION METHOD
        for module_encoding, module_name in Config.MODULE_ENCODINGS.items():
            logger.info(f"\tModule Name: {module_name}")
            variable_name_fit = f"Efit{module_encoding}"
            reconstructed_energy_fit = tree[variable_name_fit]
            reconstructed_energy_fit_data = reconstructed_energy_fit.array(library="np")

            variable_name_opt = f"Eopt{module_encoding}"
            reconstructed_energy_opt = tree[variable_name_opt]
            reconstructed_energy_opt_data = reconstructed_energy_opt.array(library="np")

            for channel_index, (channel_data_fit, channel_data_opt) in enumerate(
                    zip(reconstructed_energy_fit_data.T, reconstructed_energy_opt_data.T)
            ):
                logger.info(f"\t\tChannel Index: {channel_index}")

                reconstructed_channel_energies_plot = plotter.plot_two_histograms(
                    run_number=run_number,
                    variable1=channel_data_fit,
                    variable2=channel_data_opt,
                    label1="Fit",
                    label2="Optimal Filtering",
                    xlabel="Reconstructed Energy",
                    ylabel="Events",
                    module_name=module_name,
                    additional_info=f"Channel Index {channel_index}",
                    plot_name=f"{module_name}_ch{channel_index}_histogram",
                    show_statistics=True,
                    zoom=False,
                    show_boxplots=True,
                )
                save_path = f"../03_results/runs/{run_number}/energies//modules/{module_name}/channels/"
                reconstructed_channel_energies_plot.save_plot(save_path=save_path)


        # PLOT TOTAL RECONSTRUCTION ENERGY FOR EACH METHOD
        # for module_encoding, module_name in Config.MODULE_ENCODINGS.items():
        #     logger.info(f"\tModule Name: {module_name}")
        #     excluded_channel_indices = sorted(Config.NON_OPERATIONAL_CHANNEL_INDICES.get(module_encoding, dict()))
        #     working_channel_indices = [
        #         channel_index
        #         for channel_index in range(Config.CHANNELS_NUMBER)
        #         if channel_index not in excluded_channel_indices
        #     ]
        #
        #     reconstructed_energy_variable_name_fit = f"Efit{module_encoding}"
        #     reconstructed_energy_fit = tree[reconstructed_energy_variable_name_fit]
        #     reconstructed_energy_fit_data = reconstructed_energy_fit.array(library="np")
        #     total_reconstructed_energy_fit_data = np.sum(
        #         reconstructed_energy_fit_data[:, working_channel_indices],
        #         axis=1,
        #     )
        #
        #     reconstructed_energy_variable_name_opt = f"Eopt{module_encoding}"
        #     reconstructed_energy_opt = tree[reconstructed_energy_variable_name_opt]
        #     reconstructed_energy_opt_data = reconstructed_energy_opt.array(library="np")
        #     total_reconstructed_energy_opt_data = np.sum(
        #         reconstructed_energy_opt_data[:, working_channel_indices],
        #         axis=1,
        #     )
        #
        #     # FIND OPTIMAL UNITS
        #     _, common_unit = units_processing(
        #         events=np.concatenate(
        #             [total_reconstructed_energy_fit_data, total_reconstructed_energy_opt_data]
        #         ),
        #         mode="energy",
        #         baseline_unit="MeV",
        #         target_unit=None,
        #     )
        #     total_reconstructed_energy_fit_data, _ = units_processing(
        #         events=total_reconstructed_energy_fit_data,
        #         mode="energy",
        #         baseline_unit="MeV",
        #         target_unit=common_unit,
        #     )
        #     total_reconstructed_energy_opt_data, _ = units_processing(
        #         events=total_reconstructed_energy_opt_data,
        #         mode="energy",
        #         baseline_unit="MeV",
        #         target_unit=common_unit,
        #     )
        #
        #     channels_info = (
        #             f"Sum over {len(working_channel_indices)} channels"
        #             + (
        #                 f"\n(except channels: {', '.join(map(str, excluded_channel_indices))})"
        #                 if excluded_channel_indices else ""
        #             )
        #     )
        #
        #     total_reconstructed_energies_plot = plotter.plot_two_histograms(
        #         run_number=run_number,
        #         events1=total_reconstructed_energy_fit_data,
        #         events2=total_reconstructed_energy_opt_data,
        #         label1="Fit Method",
        #         label2="Optimal Filtering Method",
        #         xunit=common_unit,
        #         xlabel="Reconstructed Energy",
        #         ylabel="Events",
        #         module_name=module_name,
        #         additional_info=channels_info,
        #         plot_name=f"{module_name}_histogram",
        #         show_boxplots=True,
        #     )
        #     save_path = f"../03_results/runs/{run_number}/energies/fit_vs_opt/modules/{module_name}/"
        #     total_reconstructed_energies_plot.save_plot(save_path=save_path)



            # axis.annotate(
            #    channel_label,
            #    xy=(0.65, 0.82),
            #    xycoords='axes fraction',
            #    textcoords="axes fraction",
            #    fontsize=Config.FONT_SIZE - 2,
            #    horizontalalignment="left",
            #    verticalalignment='top',
            #    bbox=dict(
            #        boxstyle="square,pad=0.3",
            #        facecolor="white",
            #        edgecolor="none",
            #        linewidth=0.8,
            #        alpha=0.9,
            #    )
            # )



if __name__ == '__main__':
    main()
