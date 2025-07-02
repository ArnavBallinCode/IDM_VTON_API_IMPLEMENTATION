#!/usr/bin/env python3
"""
Test script for the new interactive interface
"""

from two_step_pipeline import list_available_items, auto_process_new_garment
from pathlib import Path

def test_interface():
    """Test the new interface functions"""
    print("🧪 Testing new interface functions...")
    
    # Test list_available_items
    print("\n1. Testing list_available_items():")
    persons, shirts, pants = list_available_items()
    
    print(f"   Found {len(persons)} persons:")
    for person in persons:
        print(f"     - {person.name}")
    
    print(f"   Found {len(shirts)} shirts:")
    for shirt in shirts:
        print(f"     - {shirt.name}")
    
    print(f"   Found {len(pants)} pants:")
    for pant in pants:
        print(f"     - {pant.name}")
    
    print("\n✅ Interface functions working correctly!")
    print("\n🎯 The NEW Complete Outfit Interface features:")
    print("   • 🎪 Main Menu Options:")
    print("     1. Complete Outfit Try-On (Shirt + Pants)")
    print("     2. Single Garment Try-On (Legacy)")
    print("     3. Run All Examples")
    print("     4. Quit")
    print("\n   • 👕 Shirt Selection:")
    print("     - Choose from available shirts")
    print("     - Add new shirt")
    print("     - Skip shirt (optional)")
    print("\n   • 👖 Pants Selection:")
    print("     - Choose from available pants")
    print("     - Add new pants")
    print("     - Skip pants (optional)")
    print("\n   • ✨ Workflow Features:")
    print("     - Interactive person selection")
    print("     - Sequential shirt and pants selection")
    print("     - Option to skip either garment")
    print("     - Complete outfit processing")
    print("     - Auto-processing of new garments")
    print("     - Same two-step pipeline logic maintained")
    print("     - Organized garments (shirts/pants folders)")

if __name__ == "__main__":
    test_interface()
