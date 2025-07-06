#!/bin/bash
# CROD UNIFIED SYSTEM STARTER
# One script to rule them all!

echo "
╔═══════════════════════════════════════════════════════════════╗
║                  CROD UNIFIED SYSTEM                          ║
║                                                               ║
║  Starting the complete CROD ecosystem...                      ║
╚═══════════════════════════════════════════════════════════════╝
"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "CROD_UNIVERSAL_LAUNCHER.js" ]; then
    echo -e "${RED}Error: Not in CROD root directory!${NC}"
    echo "Please run this script from the crod-babylon-genesis directory"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"

if ! command_exists node; then
    echo -e "${RED}Node.js is not installed!${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}npm is not installed!${NC}"
    exit 1
fi

# Optional dependencies
if command_exists python3; then
    echo -e "${GREEN}✓ Python 3 found${NC}"
else
    echo -e "${YELLOW}⚠ Python 3 not found - some features will be disabled${NC}"
fi

if command_exists docker; then
    echo -e "${GREEN}✓ Docker found${NC}"
else
    echo -e "${YELLOW}⚠ Docker not found - containerized services disabled${NC}"
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${CYAN}Installing root dependencies...${NC}"
    npm install
fi

if [ ! -d "crod-chain-app/node_modules" ]; then
    echo -e "${CYAN}Installing Tauri app dependencies...${NC}"
    cd crod-chain-app && npm install && cd ..
fi

# Deploy smart contracts
echo -e "${MAGENTA}Deploying CROD Smart Contracts...${NC}"
node -e "
const { CRODContractFactory } = require('./src/contracts/CRODSmartContracts.js');
const factory = new CRODContractFactory();
factory.deployAllContracts();
console.log('Smart contracts deployed!');
"

# Start the universal launcher
echo -e "${GREEN}Starting CROD Universal Launcher...${NC}"
node CROD_UNIVERSAL_LAUNCHER.js

# Trap Ctrl+C to cleanup
trap cleanup INT

cleanup() {
    echo -e "\n${YELLOW}Shutting down CROD services...${NC}"
    # The launcher handles its own cleanup
    exit 0
}

# Keep the script running
wait