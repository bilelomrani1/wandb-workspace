#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The script submit.py is used to execute a run or
# a series of runs. Examples of use include :
#   - Running the same experiments multiple times
#     in case of randomized code
#   - Solving a list of problem instances
#   - etc.


################ Import packages ################

import argparse
from subprocess import Popen
from wandb.util import generate_id
import yaml
import sys
from pathlib import Path
import random
from tqdm import tqdm


################ Helper functions ################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes", help="Notes for the runs")
    return parser.parse_args()


################ Submit code ################

if __name__ == "__main__":

    args = parse_args()

    NB_JOBS = 3

    # Create job ids
    job_ids = [generate_id() for _ in range(NB_JOBS)]

    # Create random seeds
    random.seed(42)
    job_seeds = [str(random.randint(0, 1000)) for _ in range(NB_JOBS)]

    # Dumb the job ids in jobs.yaml for future parsing
    with open('jobs.yaml', 'w') as buf:
        buf.write(yaml.safe_dump({'jobs_ids': job_ids}, default_flow_style=False))

    # Create the process list and execute the command
    process_list = []

    # Progress bar
    t = tqdm(range(NB_JOBS), desc='Sending job', leave=True)
    for index_run in t:

        t.set_description(f"Sending job {index_run+1}/{NB_JOBS}")
        t.refresh()

        # Create the command
        cmd = ['python3', 'script.py', '--id',
            job_ids[index_run], '--seed', job_seeds[index_run]]
        if args.notes is not None or args.notes != '':
            cmd.extend(['--notes', args.notes])

        process = Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        process_list.append(process)

    # Wait for the processes to complete
    for process in process_list:
        process.wait()
