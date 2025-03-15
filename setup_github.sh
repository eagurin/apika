#!/bin/bash

# Script to initialize git repository and push to GitHub
# Usage: ./setup_github.sh

# Make script executable: chmod +x setup_github.sh

echo "Initializing git repository..."
git init

echo "Adding files to git..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit"

echo "Adding remote origin..."
git remote add origin https://github.com/eagurin/apika.git

echo "Pushing to GitHub..."
git push -u origin master

echo "Setup complete!"
echo "If you received an authentication error, you may need to:"
echo "1. Create a personal access token on GitHub"
echo "2. Use the token as your password when prompted"
echo "3. Or configure SSH keys for GitHub"

echo "Repository URL: https://github.com/eagurin/apika" 