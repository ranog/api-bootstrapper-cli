#!/usr/bin/env bash
# Script to initialize git hooks and commit template for new contributors
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔧 Setting up development environment...${NC}"
echo ""

# Install pre-commit hooks
echo -e "${YELLOW}📦 Installing pre-commit hooks...${NC}"
poetry run pre-commit install --install-hooks
poetry run pre-commit install --hook-type commit-msg

# Configure git commit template
echo -e "${YELLOW}📝 Configuring git commit template...${NC}"
git config commit.template .gitmessage

# Make scripts executable
echo -e "${YELLOW}🔨 Making helper scripts executable...${NC}"
chmod +x scripts/*.sh

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  • Use ${YELLOW}bash scripts/commit.sh${NC} for interactive commits"
echo -e "  • Use ${YELLOW}bash scripts/bump.sh${NC} to bump version & generate changelog"
echo -e "  • Read ${YELLOW}CONTRIBUTING.md${NC} for detailed guidelines"
echo ""
echo -e "${BLUE}Quick commands:${NC}"
echo -e "  ${YELLOW}poetry run cz commit${NC}                    # Interactive commit"
echo -e "  ${YELLOW}poetry run cz bump --changelog${NC}          # Auto bump version"
echo -e "  ${YELLOW}poetry run cz bump --changelog --increment PATCH${NC}  # Patch bump"
echo ""
