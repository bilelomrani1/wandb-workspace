EXPERIMENTS := $(wildcard */)

all: $(EXPERIMENTS) parse

$(EXPERIMENTS):
	$(MAKE) -C $@ experiment

experiments: $(EXPERIMENTS)

parse:
	@for exp in $(EXPERIMENTS); do \
		$(MAKE) -C $$exp parse; \
	done

.PHONY: all experiments $(EXPERIMENTS) parse clean cleanall

clean:
	@for exp in $(EXPERIMENTS); do \
		$(MAKE) -C $$exp clean; \
	done

cleanall:
	@for exp in $(EXPERIMENTS); do \
		$(MAKE) -C $$exp cleanall; \
	done
