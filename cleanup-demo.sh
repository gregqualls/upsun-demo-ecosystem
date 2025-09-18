#!/bin/bash

# Upsun Demo Ecosystem Cleanup Script
# This script cleans up the demo ecosystem when you're done

set -e  # Exit on any error

echo "🧹 Upsun Demo Ecosystem Cleanup"
echo "==============================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if upsunstg CLI is available
if ! command -v upsunstg &> /dev/null; then
    echo "❌ Upsun CLI (upsunstg) is required but not installed."
    exit 1
fi

# Check if user is logged in
if ! upsunstg auth:info &> /dev/null; then
    echo "❌ You are not logged in to Upsun."
    echo "Please run: upsunstg auth:browser-login"
    exit 1
fi

echo "⚠️  WARNING: This will delete ALL projects and organizations created by the demo."
echo "This action cannot be undone!"
echo ""

# Escalating funny verification prompts
echo "🧨 SCORCHED EARTH VERIFICATION SEQUENCE 🧨"
echo "=========================================="
echo ""

read -p "1. Are you sure you want to delete all projects and orgs? [y/N]: " confirm1
if [ "$confirm1" != "y" ] && [ "$confirm1" != "Y" ]; then
    echo "❌ Cleanup cancelled. You're safe... for now."
    exit 0
fi

read -p "2. Seriously? Like, for real? [y/N]: " confirm2
if [ "$confirm2" != "y" ] && [ "$confirm2" != "Y" ]; then
    echo "❌ Cleanup cancelled. Your data thanks you."
    exit 0
fi

read -p "3. Are you in a healthy mindspace right now? [y/N]: " confirm3
if [ "$confirm3" != "y" ] && [ "$confirm3" != "Y" ]; then
    echo "❌ Cleanup cancelled. Maybe take a walk first and touch some grass?"
    exit 0
fi

read -p "4. Did you ask your mom for permission? [y/N]: " confirm4
if [ "$confirm4" != "y" ] && [ "$confirm4" != "Y" ]; then
    echo "❌ Cleanup cancelled. Call your mom first. She misses you"
    exit 0
fi

read -p "5. Have you eaten? [y/N]: " confirm5
if [ "$confirm5" != "y" ] && [ "$confirm5" != "Y" ]; then
    echo "❌ Cleanup cancelled. Go get a snack first. You don't want to do this on an empty stomach."
    exit 0
fi

read -p "6. This is like scorched earth. You know everything will be gone right? [y/N]: " confirm6
if [ "$confirm6" != "y" ] && [ "$confirm6" != "Y" ]; then
    echo "❌ Cleanup cancelled. Your projects are glad to live another day."
    exit 0
fi

read -p "7. Are you absolutely, positively, 100% certain? [y/N]: " confirm7
if [ "$confirm7" != "y" ] && [ "$confirm7" != "Y" ]; then
    echo "❌ Cleanup cancelled. Better safe than sorry. You don't need a panic attack right now."
    exit 0
fi

read -p "8. Last chance to back out... [y/N]: " confirm8
if [ "$confirm8" != "y" ] && [ "$confirm8" != "Y" ]; then
    echo "❌ Cleanup cancelled. You chose wisely. Think of all the work it would take to rebuild this."
    exit 0
fi

read -p "9. Fine, but don't say I didn't warn you... [y/N]: " confirm9
if [ "$confirm9" != "y" ] && [ "$confirm9" != "Y" ]; then
    echo "❌ Cleanup cancelled. Your future self will thank you."
    exit 0
fi

read -p "10. OKAY FINE! Let's burn it all down! (type 'BURN IT DOWN'): " confirm10
if [ "$confirm10" != "BURN IT DOWN" ]; then
    echo "❌ Cleanup cancelled. You're not ready for this level of destruction. You need to be more determined."
    exit 0
fi

echo ""
echo "🔥 BURN IT DOWN! 🔥"
echo "==================="
echo "Proceeding with nuclear cleanup..."
echo "                                                         c=====e"
echo "                                                            H"
echo "   ____________                                         _,,_H__"
echo "  (__((__((___()                                       //|     |"
echo " (__((__((___()()_____________________________________// |GREG |"
echo "(__((__((___()()()------------------------------------'  |_____|"
echo ""

echo ""
echo "📋 Generating cleanup script..."
python3 demo-setup.py --config demo-config.json --action cleanup

if [ $? -eq 0 ]; then
    echo "✅ Cleanup script generated successfully"
    echo ""
    echo "🧹 Running cleanup..."
    
    chmod +x cleanup-demo-ecosystem.sh
    ./cleanup-demo-ecosystem.sh
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "          _ ._  _ , _ ._"
        echo "        (_ ' ( \`  )_  .__)"
        echo "      ( (  (    )   \`)  ) _)"
        echo "     (__ (_   (_ . _) _) ,__)"
        echo "         \`~~\`\\ ' . /\`~~\`"
        echo "              ;   ;"
        echo "              /   \\"
        echo "_____________/_ __ \\_____________"
        echo ""
        echo "✅ Demo ecosystem cleanup completed successfully!"
        echo "All projects and organizations have been deleted."
    else
        echo "❌ Cleanup failed. Check the output above for errors."
        exit 1
    fi
else
    echo "❌ Failed to generate cleanup script"
    exit 1
fi
