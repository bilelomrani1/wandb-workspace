# Weights and Biases workspace

A simple workspace to work with [Weights & Biases](https://www.wandb.com), with automatic CSV dataframe generation.

## Installation

1. Clone or fork the project
2. Create a new virtual environment (recommended), for example with conda

    ```bash
    conda create -n wandb python=3.8
    conda activate wandb
    ```

3. Set your environment variables

    ```bash
    conda env config vars set WANDB_ENTITY=<entity> 
    conda env config vars set WANDB_PROJECT=<project-name>
    conda env config vars set WANDB_API_KEY=<secret-key>
    conda activate wandb
    ```

4. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

## Project structure

The `experiments` folder contains one subdirectory per experiment. Feel free to give the experiment directory more explicit names.

    experiments/
        exp1/
        exp2/
        exp3/
        ...

Each experiment subdirectory contains the following:

- `config.yaml`: the experiment configuration file, defining W&B meta-data (tags, groups, etc.) and fixed parameters of the experiment (e.g. learning rate, number of epochs, etc.)
- `script.py`: script for one job
- `submit.py`: script for submitting the experiment. Use it to launch `script.py` with several seeds, to solve a list of problem instances, etc.
- `README.md`: a brief documentation of the experiment
- `Makefile`

## Usage

In an experiment subdirectory, use `make` to automatically launch and parse the experiment. Additionally, you can use the following recipes:

- `make experiment` to launch the experiment only
- `make experiment NOTES=<message-note>` to launch the experiment with a note in W&B dashboard
- `make parse` to parse the current experiment
- `make clean` to run `wandb gc`
- `make cleanall` to clean and remove all artifacts of the current experiment

From the project root or from the `experiments` folder, use `make experiments`, `make parse`, `make clean` or `make cleanall` to launch the corresponding recipe on all experiments.

## Parsing

The script `submit.py` dumps the id of the submitted jobs in a YAML file `jobs.yaml`. In an experiment subdirectory, `make parse` creates a `dataframes/` folder and export the dataframes corresponding to the jobs in `jobs.yaml` (the latest runs for this experiment)

- `metrics.csv` contains the history of all logged values
- `summary.csv` contains the logged values for the last time step
- `system_events.csv` contains the logged system events.
