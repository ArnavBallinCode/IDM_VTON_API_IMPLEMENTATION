#!/bin/bash

# Demo script to showcase the two-step pipeline
echo "🎭 IDM-VTON Two-Step Pipeline Demo"
echo "=================================="

# Check if conda environment is activated
if [[ "$CONDA_DEFAULT_ENV" != "viton" ]]; then
    echo "⚠️  Activating conda environment..."
    conda activate viton
fi

echo "🧪 Testing setup..."
python test_setup.py

echo ""
echo "🚀 Running two-step pipeline demo..."
echo "This will process Arnav + Gucci upper with both models"

# Run with explicit example
python -c "
import sys
sys.path.append('.')
from two_step_pipeline import run_two_step_pipeline

# Run example 1: Arnav + Gucci upper
run_two_step_pipeline(
    './examples/person_images/Arnav_A.jpg',
    './examples/garment_images/gucci upper.jpg', 
    'Gucci upper garment refined with two-step pipeline',
    'upper_body'
)
"

echo ""
echo "✅ Demo completed! Check ./examples/results/ for outputs"
echo "📁 Results include:"
echo "   - step1_*.png (initial virtual-try-on)"
echo "   - final_result_*.png (IDM-VTON refined)"
echo "   - final_mask_*.png (processing mask)"
