#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "============================================"
echo "  YOLOv11 project - one-click setup"
echo "============================================"
echo
echo "Step 1/2: Installing required Python packages..."
python3 -m pip install -r requirements.txt --quiet

echo
echo "Step 2/2: Downloading the dataset from Google Drive..."
python3 main.py --mode download

echo
echo "============================================"
echo "  All done! The dataset is ready in ./dataset"
echo "  You can now run: python3 main.py"
echo "============================================"
read -p "Press Enter to close..."
