import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from modules import Plots, Config

# EBC и M0C (посмотреть на ячейки) тоже учесть в общей сумме.

def describe_root_file(
        root_file
):
    print("ROOT FILE CONTENTS:")
    print(f"Trees: {root_file.keys()}")
    tree = root_file["h1000"]
    tree.show()
    print(f"Branches: {tree.keys()}")


def describe_branch(
        root_file,
        branch_name,
        tree_name: str = "h1000",
):
    tree = root_file[tree_name]
    branch = tree[branch_name]

    print(f"\nBranch: {branch_name}")
    print(f"Name: {branch.name}")
    print(f"Title: {branch.title}")
    print(f"Entries: {branch.num_entries}")
    print(f"Interpretation: {branch.interpretation}")
    print(f"Branch type: {branch.typename}")

    branch_data = branch.array(library="np")
    print(f"Number of entries in branch {branch_name}: {len(branch_data)}")
    print(f"Data:\n{branch_data}")

    print("Shape:", branch_data.shape)
    print("Dimensions:", branch_data.ndim)
    print("Number of events:", branch_data.shape[0])
    print("Number of channels:", branch_data.shape[1])


def main():
    run_number = "2510758"
    file_path = f"{Config.DATA_PATH}/experiment/tiletb_{run_number}.root"

    plotter = Plots()

    with uproot.open(file_path) as file:
        describe_root_file(root_file=file)
        describe_branch(root_file=file, branch_name="EfitC02")







    # ==================================
    # with uproot.open(file_path) as file:
    #     tree = file["h1000"]
    #     # Read basic event information
    #     branches = [
    #         "Run",
    #         "Evt",
    #         "OFLunits",
    #         "S1cou",
    #         "S2cou",
    #         "S3cou",
    #         "Cher1",
    #         "Cher2",
    #         "Cher3",
    #         "Ximp_0",
    #         "Yimp_0",
    #     ]
    #
    #     data = tree.arrays(branches, library="np")
    #
    #     # 1. Run number
    #     runs, counts = np.unique(data["Run"], return_counts=True)
    #
    #     print("\nRun numbers:")
    #     for run, count in zip(runs, counts):
    #         print(f"{run}: {count} events")
    #
    #     # 2. Energy units
    #     units, counts = np.unique(data["OFLunits"], return_counts=True)
    #
    #     print("\nOFLunits:")
    #     for unit, count in zip(units, counts):
    #         print(f"{unit}: {count} events")
    #
    #     # 3. Beam position
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    #
    #     axes[0].hist(data["Ximp_0"], bins=100)
    #     axes[0].set_xlabel("Ximp_0")
    #     axes[0].set_ylabel("Events")
    #     axes[0].set_title("Beam X position")
    #
    #     axes[1].hist(data["Yimp_0"], bins=100)
    #     axes[1].set_xlabel("Yimp_0")
    #     axes[1].set_ylabel("Events")
    #     axes[1].set_title("Beam Y position")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #
    #
    #
    #     df = pd.DataFrame(data)
    #     fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    #
    #     for ax, branch in zip(
    #             axes,
    #             ["S1cou", "S2cou", "S3cou"]
    #     ):
    #         ax.hist(df[branch], bins=100)
    #         ax.set_title(branch)
    #         ax.set_xlabel("ADC counts")
    #         ax.set_ylabel("Events")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # S1 vs S2
    #
    #     plt.figure(figsize=(7, 6))
    #
    #     plt.hist2d(
    #         df["S1cou"],
    #         df["S2cou"],
    #         bins=100
    #     )
    #
    #     plt.xlabel("S1cou [ADC]")
    #     plt.ylabel("S2cou [ADC]")
    #     plt.title("S1 vs S2")
    #
    #     plt.colorbar(label="Events")
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # ==========================================
    #     # 2. CHERENKOV DISTRIBUTIONS
    #     # ==========================================
    #
    #     fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    #
    #     for ax, branch in zip(
    #             axes,
    #             ["Cher1", "Cher2", "Cher3"]
    #     ):
    #         ax.hist(df[branch], bins=100)
    #         ax.set_title(branch)
    #         ax.set_xlabel("ADC counts")
    #         ax.set_ylabel("Events")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # Cherenkov correlations
    #
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    #
    #     axes[0].hist2d(
    #         df["Cher1"],
    #         df["Cher2"],
    #         bins=100
    #     )
    #
    #     axes[0].set_xlabel("Cher1")
    #     axes[0].set_ylabel("Cher2")
    #     axes[0].set_title("Cher1 vs Cher2")
    #
    #     axes[1].hist2d(
    #         df["Cher1"],
    #         df["Cher3"],
    #         bins=100
    #     )
    #
    #     axes[1].set_xlabel("Cher1")
    #     axes[1].set_ylabel("Cher3")
    #     axes[1].set_title("Cher1 vs Cher3")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # ==========================================
    #     # 3. BEAM POSITION
    #     # ==========================================
    #
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    #
    #     axes[0].hist(df["Ximp_0"], bins=100)
    #     axes[0].set_xlabel("Ximp_0 [mm]")
    #     axes[0].set_ylabel("Events")
    #     axes[0].set_title("Beam X position")
    #
    #     axes[1].hist(df["Yimp_0"], bins=100)
    #     axes[1].set_xlabel("Yimp_0 [mm]")
    #     axes[1].set_ylabel("Events")
    #     axes[1].set_title("Beam Y position")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # Beam position in 2D
    #
    #     plt.figure(figsize=(7, 6))
    #
    #     plt.hist2d(
    #         df["Ximp_0"],
    #         df["Yimp_0"],
    #         bins=100
    #     )
    #
    #     plt.xlabel("Ximp_0 [mm]")
    #     plt.ylabel("Yimp_0 [mm]")
    #     plt.title("Beam impact position")
    #
    #     plt.colorbar(label="Events")
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # ==========================================
    #     # 4. TRACK QUALITY
    #     # ==========================================
    #
    #     df["DeltaX"] = df["Xcha2_0"] - df["Xcha1_0"]
    #     df["DeltaY"] = df["Ycha2_0"] - df["Ycha1_0"]
    #
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    #
    #     axes[0].hist(df["DeltaX"], bins=100)
    #     axes[0].set_title("X difference between chambers")
    #     axes[0].set_xlabel("Delta X [mm]")
    #
    #     axes[1].hist(df["DeltaY"], bins=100)
    #     axes[1].set_title("Y difference between chambers")
    #     axes[1].set_xlabel("Delta Y [mm]")
    #
    #     plt.tight_layout()
    #     plt.show()
    #
    #     # ==========================================
    #     # 5. ENERGY DISTRIBUTION
    #     # ==========================================
    #
    #     modules = ["A02", "C01", "C02", "E03"]
    #
    #     fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    #
    #     for ax, module in zip(axes.flat, modules):
    #         energy = tree[f"Efit{module}"].array(
    #             library="np"
    #         )
    #
    #         total_energy = np.sum(energy, axis=1)
    #
    #         ax.hist(total_energy, bins=100)
    #         ax.set_title(f"Total energy: {module}")
    #         ax.set_xlabel("Energy [OFL units]")
    #         ax.set_ylabel("Events")
    #
    #     plt.tight_layout()
    #     plt.show()


if __name__ == '__main__':
    main()
