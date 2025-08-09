#!/bin/bash

# Vercel Deployment Script for Secure File Encryption Tool
# This script automates the deployment process to fix the 404 error

echo "🚀 Deploying Secure File Encryption Tool to Vercel..."
echo "This will fix the 404 NOT_FOUND error you're experiencing."
echo

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is ready"
echo

# Deploy to Vercel
echo "🔄 Deploying to Vercel..."
echo "When prompted:"
echo "  - Framework Preset: Select 'Other'"
echo "  - Build Command: Leave empty (press Enter)"
echo "  - Output Directory: Leave empty (press Enter)"
echo "  - Install Command: pip install -r requirements.txt"
echo

# Run Vercel deployment
vercel --prod

echo
echo "🎉 Deployment complete!"
echo
echo "Your Secure File Encryption Tool should now be accessible at the Vercel URL provided above."
echo "The 404 error should be resolved, and you'll see a modern web interface for file encryption."
echo
echo "Features of the deployed web app:"
echo "  ✅ Modern drag-and-drop interface"
echo "  ✅ AES-256 encryption (same as desktop version)"
echo "  ✅ Mobile-friendly responsive design"
echo "  ✅ Real-time file processing"
echo "  ✅ Automatic file downloads"
echo
echo "If you encounter any issues, check the VERCEL_DEPLOYMENT_GUIDE.md file for troubleshooting."
