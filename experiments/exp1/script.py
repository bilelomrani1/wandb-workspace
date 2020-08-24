#!/usr/bin/env python
# -*- coding: utf-8 -*-


################ Import packages ################

import os
import argparse
import yaml
import numpy as np
import wandb
import random


################ Helper functions ################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes", help="Notes for the run")
    parser.add_argument("--seed", help="Random seed", type=int)
    parser.add_argument("--id", help="Id for the run")
    return parser.parse_args()


def load_yaml(path):
    with open(path, 'r') as config_stream:
        try:
            config = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return config


################ Initial parsing ################

# Load experiment's config.yaml
exp_config = load_yaml('config.yaml')

# Set the experiment's project and entity name
# to project's name and entity
exp_config['project'] = os.getenv("WANDB_PROJECT", "project_test") 
exp_config['entity'] = os.getenv("WANDB_ENTITY", None)


############## Parse cmd arguments ##############

args = parse_args()

if args.notes is not None or args.notes != '':
    exp_config['notes'] = args.notes
if args.id is not None:
    exp_config['id'] = args.id
if args.seed is None:
    np.random.seed(42)
    random.seed(42)
else:
    np.random.seed(args.seed)
    random.seed(args.seed)

# Initialize run
wandb.init(**exp_config)


################# Experiment #################

# Write experiment here.
#
# Experiment's parameters:
#   Use wandb.config as a dictionary containing
#   the parameters specified in config.yaml
#
# Logging metrics:
#   Use wandb.log() to log metrics
#
# Saving files:
#   Use wandb.save() to upload a file (checkpoints, etc.)

for i in range(100):
    foo = i + 15*random.random()
    wandb.log({'foo': foo})
