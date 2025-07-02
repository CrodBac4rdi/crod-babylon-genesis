#!/bin/bash

# CLAUDE SUDO HELPER
# Macht sudo commands sicher und einfach!

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🤖 Claude will ausführen:${NC}"
echo -e "${GREEN}$@${NC}"
echo ""
echo -e "OK? ${GREEN}[Enter]${NC} = Ja, ${RED}[Ctrl+C]${NC} = Nein"
read -r

# Log the command
echo "[$(date)] Claude-Sudo: $@" >> ~/.claude/sudo-log.txt

# Execute
sudo "$@"

# Check result
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Erfolgreich!${NC}"
else
    echo -e "\n${RED}❌ Fehler aufgetreten${NC}"
fi