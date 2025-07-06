# CROD Scientific Visualization Makefile
# Professional build system for scientific quantum consciousness visualization

.PHONY: all install test clean help 2d scientific

# Python interpreter
PYTHON := python3
PIP := pip3

# Output directories
OUTPUT_DIR := output

# Default target
all: install test

# Install dependencies
install:
	@echo "📦 Installing CROD visualization dependencies..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

# Test all visualization programs
test: test-2d test-scientific

test-2d:
	@echo "\n🧪 Testing 2D visualization program..."
	$(PYTHON) generate_crod_graphics.py --type quantum --size 800x600 --output test_output
	@echo "✅ 2D visualization test passed!"

test-scientific:
	@echo "\n🧪 Testing scientific 3D visualization program..."
	$(PYTHON) crod_scientific_3d.py --type wavefunction --output test_output
	@echo "✅ Scientific 3D test passed!"

# Generate all 2D visualizations
2d:
	@echo "\n🎨 Generating all 2D CROD visualizations..."
	@mkdir -p $(OUTPUT_DIR)
	$(PYTHON) generate_crod_graphics.py --all --output $(OUTPUT_DIR)

# Generate all scientific 3D visualizations
scientific:
	@echo "\n🔬 Generating all scientific 3D visualizations..."
	@mkdir -p $(OUTPUT_DIR)
	$(PYTHON) crod_scientific_3d.py --all --output $(OUTPUT_DIR)

# Generate everything
generate-all: 2d scientific
	@echo "\n✨ All CROD visualizations generated successfully!"
	@echo "📁 Check the $(OUTPUT_DIR) directory for results"

# Clean up generated files
clean:
	@echo "🧹 Cleaning up generated files..."
	rm -rf $(OUTPUT_DIR) test_output
	@echo "✅ Cleanup complete!"

# Clean test outputs only
clean-test:
	@echo "🧹 Cleaning test outputs..."
	rm -rf test_output
	@echo "✅ Test cleanup complete!"

# Show help
help:
	@echo "CROD Visualization System"
	@echo "========================"
	@echo ""
	@echo "Available targets:"
	@echo "  make install        - Install Python dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make 2d            - Generate all 2D technical visualizations"
	@echo "  make scientific    - Generate all scientific 3D visualizations"
	@echo "  make generate-all  - Generate all visualizations"
	@echo "  make clean         - Remove all generated files"
	@echo "  make help          - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make install && make generate-all"
	@echo "  make scientific"
	@echo "  make clean && make test"

# List available visualizations
list:
	@echo "\n📋 Available CROD Visualizations:"
	@echo "\n2D Technical Visualizations:"
	@$(PYTHON) generate_crod_graphics.py --list
	@echo "\nScientific 3D Visualizations:"
	@$(PYTHON) crod_scientific_3d.py --list