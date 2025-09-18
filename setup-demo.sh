#!/bin/bash

# Upsun Demo Ecosystem Setup Script
# This script makes it easy for team members to set up the demo ecosystem

set -e  # Exit on any error

# Record start time
START_TIME=$(date +%s)

echo "🚀 Upsun Demo Ecosystem Setup"
echo "=============================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if upsunstg CLI is available
if ! command -v upsunstg &> /dev/null; then
    echo "❌ Upsun CLI (upsunstg) is required but not installed."
    echo "Please install the Upsun CLI and try again."
    echo "Visit: https://docs.upsun.com/get-started/install-cli"
    exit 1
fi

# Check if user is logged in
if ! upsunstg auth:info &> /dev/null; then
    echo "❌ You are not logged in to Upsun."
    echo "Please run: upsunstg auth:browser-login"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Generate and run the setup script
echo "📋 Generating demo ecosystem setup script..."
python3 demo-setup.py --config demo-config.json --action setup

if [ $? -eq 0 ]; then
    echo "✅ Setup script generated successfully"
    echo ""
    echo "🚀 Running demo ecosystem setup..."
    echo "This will create organizations and projects for the yacht industry demo."
    echo ""
    
    chmod +x setup-demo-ecosystem.sh
    ./setup-demo-ecosystem.sh
    
    if [ $? -eq 0 ]; then
        # Calculate total time
        END_TIME=$(date +%s)
        DURATION=$((END_TIME - START_TIME))
        MINUTES=$((DURATION / 60))
        SECONDS=$((DURATION % 60))
        
        echo ""
        echo "🎉 Demo ecosystem setup completed successfully!"
        echo ""
        echo "📊 What was created:"
        echo "  • 6 Organizations (3 Fixed, 3 Flex)"
        echo "  • 16 Projects across yacht industry brands"
        echo "  • Marketing sites (Drupal 10)"
        echo "  • E-commerce stores (WordPress WooCommerce)"
        echo "  • Blog platforms (WordPress Bedrock)"
        echo "  • Regional business applications (Flask, Rails, etc.)"
        echo ""
        echo "⏱️  Total setup time: ${MINUTES}m ${SECONDS}s"
        echo ""
        echo "🔗 View your projects at: https://console.upsun.plat.farm"
        echo ""
        echo "🧹 To clean up when done, run: ./cleanup-demo.sh"
    else
        echo "❌ Setup failed. Check the output above for errors."
        exit 1
    fi
else
    echo "❌ Failed to generate setup script"
    exit 1
fi
