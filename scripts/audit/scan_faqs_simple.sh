#!/bin/bash

# English FAQ patterns
patterns="Is image processing secure|What image formats|Is there a file size limit|Can I process multiple images|How do I convert|What is the difference between|Does this tool|Will my images be|Can I use this|Is it free|How to|What happens to|Are my images|Is there a limit"

echo "=== COMPREHENSIVE UNTRANSLATED FAQ SCAN ==="
echo ""

# Check each language directory
for lang in ar de es fr ja pt zh; do
    echo "--- Scanning $lang directory ---"
    
    # Find files with English in HTML FAQ sections
    html_files=$(find ./$lang -name "index.html" -exec grep -l -i "$patterns" {} \; 2>/dev/null)
    html_count=$(echo "$html_files" | wc -l)
    
    echo "Files with English in HTML: $html_count"
    
    if [ $html_count -gt 0 ]; then
        echo "Files:"
        echo "$html_files" | while read -r file; do
            # Get sample text
            sample=$(grep -o -i "$patterns" "$file" | head -1)
            echo "  - $file (Sample: $sample)"
        done
    fi
    echo ""
done

echo "=== CHECKING FOR ENGLISH IN JSON-LD ==="
echo ""

# Check for English in JSON-LD
for lang in ar de es fr ja pt zh; do
    echo "--- Checking $lang JSON-LD ---"
    
    jsonld_files=$(find ./$lang -name "index.html" -exec grep -l '"FAQPage"' {} \; 2>/dev/null)
    
    if [ -n "$jsonld_files" ]; then
        for file in $jsonld_files; do
            if grep -q -i "$patterns" "$file"; then
                echo "  - $file has English in JSON-LD"
                sample=$(grep -o -i "$patterns" "$file" | head -1)
                echo "    Sample: $sample"
            fi
        done
    fi
done
