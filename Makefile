include env.mk
include mk/prepare.mk
include local.mk

all: help
	@true

post_stub:
	@for p in miscutil/*.pyi.patch; do if test -f "$$p"; then \
		patch -p1 < $$p; \
	fi; done

%:
	@$(MAKE) -f mk/util.mk $@
