# KOSMOS Multi-Slit Data Reduction Pipeline with CofI Reduction Widget

Welcome to the official repository for the CofI Reduction Widget, a modern, user-friendly pipeline for KOSMOS multi-slit spectroscopic data reduction. This package provides an intuitive graphical user interface (GUI) within a Jupyter Notebook, designed to streamline the entire reduction workflow from raw data to final science products.

This repository represents the latest, application-focused version of our reduction tools, prioritizing ease of use and an efficient, interactive workflow.

## About the Project

This pipeline is designed to guide users through the complex process of multi-slit data reduction without requiring extensive coding. It is built upon the robust astro-pyvista library and encapsulates the entire workflow from calibration and slit identification to 2D/1D spectral extraction and post-processing analysis into an interactive widget.

For users interested in the foundational, cell-by-cell code and a more detailed explanation of the base algorithms, please visit our earlier development repository: CofI_Abdullah_2024 (https://github.com/mwbest/CofI_Abdullah_2024). While that repository provides a thorough breakdown of the core concepts, it lacks a reflection of our recent updates to the code. This repository contains our most up-to-date and user-friendly implementation.

## Repository Contents

This repository includes everything you need to get started:

- **The cofi_reduction Package:** The core Python package containing the interactive widget, processing modules, and post-analysis tools.

- **A Draft User Manual (widgets_notebook_workflow.pdf):** A comprehensive guide detailing the operation of the user interface and the underlying scientific workflow.

- **Sample Data:** A complete dataset from an M3 mask is included for a trial run, allowing you to test the pipeline from start to finish.

- **Jupyter Notebook:** An example notebook that demonstrates how to install the package, launch the widget, and begin the reduction process.

- **Sample Data:** A complete dataset from an M3 mask is included for a trial run, allowing you to test the pipeline from start to finish.

- **Jupyter Notebook:** An example notebook that demonstrates how to install the package, launch the widget, and begin the reduction process.

# Getting Started
**!Note:** Follow the workflow guide for proper installation. This one is still in progress.

1. **Clone the repository:**

  ```git clone``` https://github.com/mwbest/CofI_2025.git

3. **Navigate to the root directory:**

  ```cd CofI_multi```

5. **Install the package and its dependencies:**

  ```pip install .```

For development, you can use ```pip install -e .``` for an editable install.
