post_stub:
	@for p in miscutil/*.pyi.patch; do if test -f "$$p"; then \
		patch -p1 < $$p; \
	fi; done
