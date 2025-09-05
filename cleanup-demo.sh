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
read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled."
    exit 0
fi

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
