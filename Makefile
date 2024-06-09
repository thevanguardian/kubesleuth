# Makefile for KubeSleuth project

# Variables
PACKAGE_NAME = kubesleuth
PYTHON = python3
PIP = pip3
TWINE = twine

# Default target
.PHONY: all
all: install

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt
	$(PIP) install .

# Build distribution archives
.PHONY: build
build:
	$(PYTHON) setup.py sdist bdist_wheel

# Upload to PyPI
.PHONY: upload
upload:
	$(TWINE) upload dist/*

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build dist *.egg-info

# Test installation
.PHONY: test-install
test-install:
	$(PIP) install -e .

# Help
.PHONY: help
help:
	@echo "Makefile for KubeSleuth project"
	@echo
	@echo "Usage:"
	@echo "  make install       Install dependencies and the package"
	@echo "  make build         Build distribution archives"
	@echo "  make upload        Upload distribution archives to PyPI"
	@echo "  make clean         Clean build artifacts"
	@echo "  make test-install  Install the package in editable mode"
	@echo "  make help          Display this help message"
