all: experiments parse

.PHONY: experiments parse clean cleanall

experiments: 
	$(MAKE) -C experiments experiments

parse:
	$(MAKE) -C experiments parse

clean:
	$(MAKE) -C experiments clean

cleanall:
	$(MAKE) -C experiments cleanall