#!/bin/bash
#
# NTRLI Superbot - Build Environment Cleanup Script
# Run this before each new phase build to ensure clean artifacts
#
# Usage: ./cleanup_build.sh
#

set -e  # Exit on error

echo "=================================================="
echo "NTRLI Superbot - Build Environment Cleanup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to safely remove directory
cleanup_dir() {
    local dir=$1
    local desc=$2

    if [ -d "$dir" ]; then
        echo -e "${YELLOW}Removing $desc...${NC}"
        rm -rf "$dir"
        echo -e "${GREEN}✓ Removed: $dir${NC}"
    else
        echo -e "${GREEN}✓ Already clean: $dir${NC}"
    fi
}

# Function to check disk space
check_disk_space() {
    echo ""
    echo "Checking disk space..."
    df -h . | tail -1 | awk '{print "Available: " $4 " (" $5 " used)"}'
}

echo "Starting cleanup process..."
echo ""

# 1. Clean local buildozer cache
cleanup_dir ".buildozer" "local buildozer cache"

# 2. Clean global buildozer cache
cleanup_dir "$HOME/.buildozer" "global buildozer cache"

# 3. Clean Python cache files
echo -e "${YELLOW}Removing Python cache files...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo -e "${GREEN}✓ Python cache cleaned${NC}"

# 4. Clean old APK builds (optional)
if [ -d "bin" ]; then
    echo -e "${YELLOW}Found old APK builds in bin/...${NC}"
    read -p "Remove old APK files? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup_dir "bin" "old APK builds"
    else
        echo -e "${YELLOW}Keeping old APK files${NC}"
    fi
fi

# 5. Check for remaining artifacts
echo ""
echo "Checking for remaining build artifacts..."
ARTIFACTS=$(find . -type d \( -name ".buildozer" -o -name "__pycache__" -o -name "*.egg-info" \) 2>/dev/null | wc -l)
if [ "$ARTIFACTS" -eq 0 ]; then
    echo -e "${GREEN}✓ No build artifacts found${NC}"
else
    echo -e "${RED}⚠ Warning: $ARTIFACTS build artifacts still present${NC}"
fi

# 6. Display disk space after cleanup
check_disk_space

echo ""
echo "=================================================="
echo -e "${GREEN}Cleanup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Review changes to buildozer.spec"
echo "  2. Run: buildozer -v android debug"
echo "  3. Monitor build logs for errors"
echo "  4. Test APK thoroughly on device"
echo ""
echo "To build now, run:"
echo "  cd app1 && buildozer -v android debug"
echo ""

exit 0
