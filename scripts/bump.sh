#!/usr/bin/env bash
# Helper script for bumping version and generating changelog
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Version Bump & Changelog Generator${NC}"
echo ""

# Get increment type from argument or default to auto
INCREMENT_TYPE=${1:-""}

if [[ -n "$INCREMENT_TYPE" ]]; then
    case "$INCREMENT_TYPE" in
        patch|PATCH)
            INCREMENT="PATCH"
            ;;
        minor|MINOR)
            INCREMENT="MINOR"
            ;;
        major|MAJOR)
            INCREMENT="MAJOR"
            ;;
        *)
            echo -e "${RED}❌ Invalid increment type: $INCREMENT_TYPE${NC}"
            echo -e "${YELLOW}Usage: $0 [patch|minor|major]${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${YELLOW}🔢 Bumping version (${INCREMENT})...${NC}"
    echo ""
    
    cz bump --changelog --increment "$INCREMENT" --yes
else
    echo -e "${YELLOW}🔢 Auto-detecting version bump from commits...${NC}"
    echo ""
    
    cz bump --changelog
fi

echo ""
echo -e "${GREEN}✅ Version bumped successfully!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo -e "   1. Review ${BLUE}CHANGELOG.md${NC}"
echo -e "   2. Review version changes in ${BLUE}pyproject.toml${NC}"
echo -e "   3. ${BLUE}git push${NC}"
echo -e "   4. ${BLUE}git push --tags${NC}"
echo -e "   5. ${BLUE}poetry publish --build${NC} (if ready for PyPI)"
