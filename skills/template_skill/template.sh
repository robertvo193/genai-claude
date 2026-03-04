#!/bin/bash
# Template Generation Skill - Simple wrapper
# Usage: /template <excel_file.xlsx>

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Excel file provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Usage: /template <excel_file.xlsx>${NC}"
    echo ""
    echo "Example:"
    echo "  /template DT_cedo.xlsx"
    echo ""
    echo -e "${YELLOW}💡 Tip: The Excel file must be in the current directory${NC}"
    exit 1
fi

EXCEL_FILE="$1"

# Check if file exists
if [ ! -f "$EXCEL_FILE" ]; then
    echo -e "${RED}❌ Excel file not found: $EXCEL_FILE${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: Check current directory:${NC}"
    echo "   $(pwd)"
    echo ""
    echo -e "${YELLOW}Available .xlsx files:${NC}"
    ls -1 *.xlsx 2>/dev/null || echo "   No .xlsx files found"
    exit 1
fi

# Check if file is .xlsx
if [[ ! "$EXCEL_FILE" =~ \.xlsx$ ]]; then
    echo -e "${RED}❌ File must be .xlsx format (not .xls)${NC}"
    exit 1
fi

# Run the Python script
PYTHON_SCRIPT="$HOME/.claude/skills/dealtransfer2template/bin/generate_template.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Script not found: $PYTHON_SCRIPT${NC}"
    exit 1
fi

echo -e "${BLUE}🎯 Generating template from: $EXCEL_FILE${NC}"
echo ""

# Execute Python script
python3 "$PYTHON_SCRIPT" "$EXCEL_FILE"
exit_code=$?

# Check result
if [ $exit_code -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Template generation complete!${NC}"
    echo ""
    echo -e "${BLUE}📝 Next steps:${NC}"
    echo "   1. Review the checklist file"
    echo "   2. Fill in presale answers"
    echo "   3. Update template with confirmed values"
    echo "   4. Generate slides: /quotation slide <template.md>"
else
    echo ""
    echo -e "${RED}❌ Template generation failed${NC}"
    exit $exit_code
fi
