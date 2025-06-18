#!/usr/bin/env python3
"""
Test script to verify the two-step pipeline works
"""

import sys
from pathlib import Path

def test_imports():
    """Test if required packages are available"""
    try:
        from gradio_client import Client, handle_file
        print("✅ gradio_client imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_files():
    """Test if required files exist"""
    required_files = [
        "./examples/person_images/Arnav_A.jpg",
        "./examples/person_images/korean girl.png", 
        "./examples/person_images/will_smith.jpg",
        "./examples/garment_images/gucci upper.jpg",
        "./examples/garment_images/upper_2.jpg",
        "./.env.example"
    ]
    
    # New optional files
    new_files = [
        "./examples/person_images/Full Man.jpg",
        "./examples/garment_images/pants.jpg",
        "./examples/garment_images/upper_3.jpg"
    ]
    
    print("📁 Core Files:")
    all_exist = True
    for file_path in required_files:
        file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
        if Path(file_path).exists() and file_size > 0:
            print(f"✅ Found: {file_path} ({file_size:,} bytes)")
        else:
            print(f"❌ Missing or empty: {file_path}")
            all_exist = False
    
    print("\n🆕 New Files:")
    new_files_exist = 0
    for file_path in new_files:
        file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
        if Path(file_path).exists() and file_size > 0:
            print(f"✅ Found: {file_path} ({file_size:,} bytes)")
            new_files_exist += 1
        else:
            print(f"⚠️  Not added yet: {file_path}")
    
    print(f"\n📊 Summary: {new_files_exist}/{len(new_files)} new files added")
    if new_files_exist < len(new_files):
        print("💡 See ADD_IMAGES_GUIDE.md for instructions to add missing images")
    
    return all_exist

def test_env():
    """Test environment setup"""
    import os
    
    # Try to load from .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
        print("✅ .env file loaded")
    else:
        print("⚠️  .env file not found (using environment variables)")
    
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if hf_token:
        print("✅ HUGGINGFACE_TOKEN found")
        print(f"   Token starts with: {hf_token[:10]}...")
        return True
    else:
        print("❌ HUGGINGFACE_TOKEN not found")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Two-Step Pipeline Setup")
    print("="*40)
    
    # Test imports
    print("\n1. Testing imports...")
    imports_ok = test_imports()
    
    # Test files
    print("\n2. Testing required files...")
    files_ok = test_files()
    
    # Test environment
    print("\n3. Testing environment...")
    env_ok = test_env()
    
    # Summary
    print("\n" + "="*40)
    if imports_ok and files_ok and env_ok:
        print("🎉 All tests passed! Ready to run two-step pipeline!")
        print("\nNext steps:")
        print("1. python two_step_pipeline.py")
        print("2. python inference.py")
        print("3. python run_examples.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if not imports_ok:
            print("\nTo fix imports:")
            print("pip install gradio_client")
        
        if not env_ok:
            print("\nTo fix environment:")
            print("1. cp .env.example .env")
            print("2. Edit .env and add your HF token")
    
    print("="*40)

if __name__ == "__main__":
    main()
