NOTES ?= ''

all: experiment parse

.PHONY: experiment parse clean cleanall

jobs.yaml: 
	$(MAKE) experiment

experiment: script.py submit.py
	python submit.py --notes "$(NOTES)"

parse: jobs.yaml ../parser.py
	python ../parser.py --directory . --jobs $< dataframes/

clean:
	wandb gc

cleanall:
	rm -rf dataframes/
	rm -rf wandb/
	rm -f jobs.yaml
