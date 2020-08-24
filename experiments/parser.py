#!/usr/bin/env python
# -*- coding: utf-8 -*-


################ Import packages ################

import argparse
import os
import yaml
import pandas as pd
import wandb
from pathlib import Path
from tqdm import tqdm


################ Helper functions ################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--directory", help="Path to an experiment directory")
    parser.add_argument(
        "--all", help="Create dataframes for all runs in the project", action="store_true")
    parser.add_argument("--jobs", help="Path to the jobs YAML file")
    return parser.parse_args()


def load_yaml(path):
    with open(path, 'r') as config_stream:
        try:
            config = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return config


################ Parsing runs ################


def parse_runs(runs_iter):

    summary_list = []
    config_list = []
    id_list = []
    history_list = []
    system_list = []
    nb_runs = len(runs_iter)

    # Progress bar
    t = tqdm(enumerate(runs_iter), desc='Parsing', leave=True)

    for i, run in t:

        t.set_description(f"Parsing {i+1}/{nb_runs} runs")
        t.refresh()

        # run.summary are the output key/values like accuracy.  We call ._json_dict to omit large files
        summary_list.append(run.summary._json_dict)

        # run.config is the input metrics.  We remove special values that start with _.
        config_list.append(
            {k: v for k, v in run.config.items() if not k.startswith('_')})

        # run.id is the id of the run
        id_list.append(run.id)

        # history contains the logged metrics
        history = run.scan_history()
        history_df = pd.DataFrame.from_records([row for row in history])
        history_df['id'] = run.id
        history_list.append(history_df)

        # system contains the logged system events
        events_df = run.history(stream='events')
        events_df['id'] = run.id
        system_list.append(events_df)


    # Exporting dataframes
    print("Exporting...")
    os.makedirs(Path(args.output), exist_ok=True)

    summary_df = pd.DataFrame.from_records(summary_list)
    config_df = pd.DataFrame.from_records(config_list)
    id_df = pd.DataFrame({'id': id_list})

    summary_dataframe = pd.concat([id_df, config_df, summary_df], axis=1)
    summary_dataframe.to_csv( Path(args.output).joinpath("summary.csv"), index=False)

    history_dataframe = pd.concat(history_list, axis=0)
    history_dataframe.to_csv(Path(args.output).joinpath("metrics.csv"), index=False)

    events_dataframe = pd.concat(system_list, axis=0)
    events_dataframe.to_csv(Path(args.output).joinpath(
        "system_events.csv"), index=False)

    print("Done!")


################ Parsing ################

if __name__ == "__main__":

    args = parse_args()
    entity = os.getenv("WANDB_ENTITY", None)
    project_name = os.getenv("WANDB_PROJECT", "project_test")

    # Parse all runs in the project
    if args.all:
        api = wandb.Api()
        try:
            all_runs = api.runs(f"{entity}/{project_name}")
        except wandb.apis.CommError as exc:
            print(exc)
            exit(1)
        parse_runs(all_runs)

    if args.directory is not None:
        api = wandb.Api()
        jobs_yaml = load_yaml(args.jobs)
        try:
            runs = [api.run(f"{entity}/{project_name}/{run_id}")
                    for run_id in jobs_yaml['jobs_ids']]
        except wandb.apis.CommError as exc:
            print(exc)
            exit(1)
        parse_runs(runs)
