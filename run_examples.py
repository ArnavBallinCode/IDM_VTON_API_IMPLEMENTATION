#!/usr/bin/env python3
"""
Example runner for IDM-VTON Virtual Try-On
Run different combinations of person and garment images easily
"""

from gradio_client import Client, handle_file
import os
from pathlib import Path
import time

# Try to load from .env file
env_file = Path(".env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"')

# Get token from environment
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if not hf_token:
    print("Please set your Hugging Face token!")
    print("You can either:")
    print("1. Create .env file with: HUGGINGFACE_TOKEN=your_token_here")
    print("2. Set environment variable: export HUGGINGFACE_TOKEN=your_token_here")
    exit(1)

# Initialize client
print(" Connecting to your IDM-VTON space...")
client = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)
print(" Connected successfully!")

# Available examples
EXAMPLES = {
    "1": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/gucci upper.jpg",
        "description": "Arnav wearing Gucci upper garment"
    },
    "2": {
        "person": "./examples/person_images/korean girl.png", 
        "garment": "./examples/garment_images/gucci upper.jpg",
        "description": "Korean girl wearing Gucci upper garment"
    },
    "3": {
        "person": "./examples/person_images/will_smith.jpg",
        "garment": "./examples/garment_images/gucci upper.jpg", 
        "description": "Will Smith wearing Gucci upper garment"
    },
    "4": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/upper_2.jpg",
        "description": "Arnav wearing alternative upper garment"
    },
    "5": {
        "person": "./examples/person_images/korean girl.png",
        "garment": "./examples/garment_images/upper_2.jpg", 
        "description": "Korean girl wearing alternative upper garment"
    }
}

def run_example(example_key):
    """Run a specific example"""
    if example_key not in EXAMPLES:
        print(f" Example {example_key} not found!")
        return
    
    example = EXAMPLES[example_key]
    print(f"\n Running Example {example_key}: {example['description']}")
    print(f"👤 Person: {example['person']}")
    print(f"👕 Garment: {example['garment']}")
    
    # Check if files exist
    if not Path(example['person']).exists():
        print(f" Person image not found: {example['person']}")
        return
    if not Path(example['garment']).exists():
        print(f" Garment image not found: {example['garment']}")
        return
    
    print("⏳ Processing virtual try-on...")
    start_time = time.time()
    
    try:
        result = client.predict(
            dict={
                "background": handle_file(example['person']),
                "layers": [],
                "composite": None
            },
            garm_img=handle_file(example['garment']),
            garment_des=example['description'],
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )
        
        end_time = time.time()
        print(f" Completed in {end_time - start_time:.1f} seconds")
        
        # Save results with meaningful names
        timestamp = int(time.time())
        result_name = f"example_{example_key}_{timestamp}"
        
        # Copy results to examples/results folder
        if len(result) >= 2:
            import shutil
            result_path = f"./examples/results/{result_name}_tryon.png"
            mask_path = f"./examples/results/{result_name}_mask.png"
            
            shutil.copy(result[0], result_path)
            shutil.copy(result[1], mask_path)
            
            print(f"    Results saved:")
            print(f"   Main result: {result_path}")
            print(f"   Mask result: {mask_path}")
        
    except Exception as e:
        print(f" Error during processing: {e}")

def main():
    """Main interactive menu"""
    print("\n" + "="*50)
    print("IDM-VTON Example Runner")
    print("="*50)
    
    print("\nAvailable Examples:")
    for key, example in EXAMPLES.items():
        print(f"{key}. {example['description']}")
    
    print("\nCommands:")
    print("• Enter example number (1-5) to run")
    print("• 'all' to run all examples")
    print("• 'q' to quit")
    
    while True:
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == 'all':
            print(" Running all examples...")
            for key in EXAMPLES.keys():
                run_example(key)
                print("-" * 30)
        elif choice in EXAMPLES:
            run_example(choice)
        else:
            print("Invalid choice. Please enter 1-5, 'all', or 'q'")

if __name__ == "__main__":
    main()
