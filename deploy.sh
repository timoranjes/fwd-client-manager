#!/bin/bash

# Deploy FWD Client Manager to Railway
# Run this script in your terminal

echo "🚀 Deploying FWD Client Manager to Railway..."
echo ""

# Check if logged in
if ! railway whoami &>/dev/null; then
    echo "📝 Step 1: Login to Railway"
    echo "   Opening browser for login..."
    railway login
fi

echo ""
echo "📦 Step 2: Initializing project"
echo "   Select 'Deploy from GitHub repo' when prompted"
railway init

echo ""
echo "🚀 Step 3: Deploying..."
railway up

echo ""
echo "✅ Done! Your app URL:"
railway domain
