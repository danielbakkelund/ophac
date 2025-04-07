#!/bin/bash

# To use this file, set the following environment variables:
# - TWINE_USERNAME: __token__
# - TWINE_PASSWORD: <your PyPI token>

# Stop immediately if a command exits with a non-zero status
set -e

pip install --upgrade build twine

PACKAGE_NAME="ophac"

# Step 1: Clean previous builds
echo "🔄 Cleaning old builds..."
rm -rf dist/ build/ *.egg-info

# Step 2: Build sdist and wheel
echo "📦 Building source and wheel distributions..."
python -m build

# Step 3: Check the distribution
echo "🕵️ Checking distribution with twine..."
twine check dist/*

# Step 4: Upload to PyPI
echo "🚀 Uploading to PyPI..."
twine upload dist/*

echo "✅ Done! Package $PACKAGE_NAME uploaded to PyPI."
