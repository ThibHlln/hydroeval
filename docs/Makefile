# Minimal makefile for Sphinx documentation
#
.ONESHELL:

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = _doc_src
BUILDDIR      = _doc_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

github_clean:
	@make local_clean
	find . \( -type d -maxdepth 1 ! -name "." \) \
	-and \( -type d -maxdepth 1 ! -name "*.*.*" \) \
	-and \( -type d -maxdepth 1 ! -name "_doc_*" \) \
	-exec rm -rf {} +

github_html:
	@make github_clean
	@make local_html
	cp -a $(BUILDDIR)/html/. .
ifdef VERSION_RELEASE
	cp -a $(BUILDDIR)/html/. ./$(VERSION_RELEASE)
endif

local_clean:
	rm -rf $(BUILDDIR)/*

local_html:
	@make local_clean
	$(MAKE) html
