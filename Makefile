# CROD Makefile
# Build and manage CROD binaries

# Variables
BINARY_NAME=crod
BUILD_DIR=build
GO=go
GOFLAGS=-ldflags "-s -w"
VERSION=$(shell git describe --tags --always --dirty)
PLATFORMS=darwin linux windows
ARCHITECTURES=amd64 arm64

# Default target
.DEFAULT_GOAL := build

# Build for current platform
.PHONY: build
build:
	@echo "Building CROD for current platform..."
	@mkdir -p $(BUILD_DIR)
	$(GO) build $(GOFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) cmd/crod/main.go
	@echo "✓ Build complete: $(BUILD_DIR)/$(BINARY_NAME)"

# Build for all platforms
.PHONY: build-all
build-all:
	@echo "Building CROD for all platforms..."
	@mkdir -p $(BUILD_DIR)
	@for GOOS in $(PLATFORMS); do \
		for GOARCH in $(ARCHITECTURES); do \
			output_name=$(BUILD_DIR)/$(BINARY_NAME)-$$GOOS-$$GOARCH; \
			if [ $$GOOS = "windows" ]; then \
				output_name=$$output_name.exe; \
			fi; \
			echo "Building $$output_name..."; \
			GOOS=$$GOOS GOARCH=$$GOARCH $(GO) build $(GOFLAGS) -o $$output_name cmd/crod/main.go; \
		done; \
	done
	@echo "✓ All builds complete"

# Install binary to system
.PHONY: install
install: build
	@echo "Installing CROD..."
	@sudo cp $(BUILD_DIR)/$(BINARY_NAME) /usr/local/bin/
	@sudo chmod +x /usr/local/bin/$(BINARY_NAME)
	@echo "✓ CROD installed to /usr/local/bin/$(BINARY_NAME)"

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	$(GO) test -v ./...

# Run with race detector
.PHONY: test-race
test-race:
	@echo "Running tests with race detector..."
	$(GO) test -race -v ./...

# Format code
.PHONY: fmt
fmt:
	@echo "Formatting code..."
	$(GO) fmt ./...

# Lint code
.PHONY: lint
lint:
	@echo "Linting code..."
	@if ! command -v golangci-lint &> /dev/null; then \
		echo "golangci-lint not installed. Installing..."; \
		go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest; \
	fi
	golangci-lint run

# Run the program
.PHONY: run
run: build
	@echo "Running CROD..."
	./$(BUILD_DIR)/$(BINARY_NAME)

# Run in development mode
.PHONY: dev
dev:
	@echo "Running CROD in development mode..."
	$(GO) run cmd/crod/main.go dev

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@echo "✓ Clean complete"

# Download dependencies
.PHONY: deps
deps:
	@echo "Downloading dependencies..."
	$(GO) mod download
	$(GO) mod tidy

# Update dependencies
.PHONY: update-deps
update-deps:
	@echo "Updating dependencies..."
	$(GO) get -u ./...
	$(GO) mod tidy

# Create release
.PHONY: release
release: clean build-all
	@echo "Creating release $(VERSION)..."
	@mkdir -p releases/$(VERSION)
	@cp -r $(BUILD_DIR)/* releases/$(VERSION)/
	@tar -czf releases/crod-$(VERSION).tar.gz -C releases $(VERSION)
	@echo "✓ Release created: releases/crod-$(VERSION).tar.gz"

# Show help
.PHONY: help
help:
	@echo "CROD Makefile Commands:"
	@echo "  make build       - Build for current platform"
	@echo "  make build-all   - Build for all platforms"
	@echo "  make install     - Install to /usr/local/bin"
	@echo "  make test        - Run tests"
	@echo "  make test-race   - Run tests with race detector"
	@echo "  make fmt         - Format code"
	@echo "  make lint        - Lint code"
	@echo "  make run         - Build and run"
	@echo "  make dev         - Run in development mode"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make deps        - Download dependencies"
	@echo "  make update-deps - Update dependencies"
	@echo "  make release     - Create release package"
	@echo "  make help        - Show this help"

# Version info
.PHONY: version
version:
	@echo "CROD version: $(VERSION)"