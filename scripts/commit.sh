#!/usr/bin/env bash
# Helper script for making conventional commits using commitizen
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Commitizen Helper${NC}"
echo ""

# Check if there are changes to commit
if [[ -z $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

echo -e "${GREEN}📝 Staged changes:${NC}"
git status -s
echo ""

# Use commitizen to create commit
echo -e "${BLUE}Creating conventional commit...${NC}"
echo ""

# Run commitizen commit
if cz commit; then
    echo ""
    echo -e "${GREEN}✅ Commit created successfully!${NC}"
    echo ""
    echo -e "${YELLOW}📊 To generate changelog and bump version:${NC}"
    echo -e "   ${BLUE}cz bump --changelog${NC}"
    echo ""
    echo -e "${YELLOW}💡 Or specify version increment:${NC}"
    echo -e "   ${BLUE}cz bump --changelog --increment PATCH${NC}  # 0.1.0 → 0.1.1"
    echo -e "   ${BLUE}cz bump --changelog --increment MINOR${NC}  # 0.1.0 → 0.2.0"
    echo -e "   ${BLUE}cz bump --changelog --increment MAJOR${NC}  # 0.1.0 → 1.0.0"
else
    echo ""
    echo -e "${RED}❌ Commit cancelled or failed${NC}"
    exit 1
fi
