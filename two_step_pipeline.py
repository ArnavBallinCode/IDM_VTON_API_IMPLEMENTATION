#!/usr/bin/env python3
"""
Two-Step Virtual Try-On Pipeline
1. First: Use virtual-try-on for initial processing
2. Second: Use IDM-VTON for refined shirt results
"""

from gradio_client import Client, handle_file
import os
from pathlib import Path
import time
import shutil

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
    print("❌ Please set your Hugging Face token!")
    print("You can either:")
    print("1. Create .env file with: HUGGINGFACE_TOKEN=your_token_here")
    print("2. Set environment variable: export HUGGINGFACE_TOKEN=your_token_here")
    exit(1)

def step1_virtual_tryon(person_path, garment_path, garment_type="upper_body"):
    """
    Step 1: Initial virtual try-on using blackmamba2408/virtual-try-on
    """
    print("🚀 Step 1: Connecting to virtual-try-on space...")
    client1 = Client("blackmamba2408/virtual-try-on", hf_token=hf_token)
    print("✅ Connected to virtual-try-on!")
    
    print("⏳ Processing initial virtual try-on...")
    start_time = time.time()
    
    try:
        result = client1.predict(
            person_path=handle_file(person_path),
            garment_path=handle_file(garment_path),
            garment_type=garment_type,
            api_name="/virtual_tryon"
        )
        
        end_time = time.time()
        print(f"✅ Step 1 completed in {end_time - start_time:.1f} seconds")
        
        # Save intermediate result
        timestamp = int(time.time())
        intermediate_path = f"./examples/results/step1_result_{timestamp}.png"
        
        # The result is a dict, we need the path
        if isinstance(result, dict) and 'path' in result:
            shutil.copy(result['path'], intermediate_path)
        elif isinstance(result, str):
            shutil.copy(result, intermediate_path)
        else:
            # If result is a tuple/list, take the first element
            shutil.copy(result[0] if isinstance(result, (list, tuple)) else result, intermediate_path)
        
        print(f"💾 Step 1 result saved: {intermediate_path}")
        return intermediate_path
        
    except Exception as e:
        print(f"❌ Step 1 failed: {e}")
        return None

def step2_idm_vton(step1_result_path, original_garment_path, garment_description):
    """
    Step 2: Refined processing using IDM-VTON
    """
    print("🚀 Step 2: Connecting to IDM-VTON space...")
    client2 = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)
    print("✅ Connected to IDM-VTON!")
    
    print("⏳ Processing refined virtual try-on...")
    start_time = time.time()
    
    try:
        result = client2.predict(
            dict={
                "background": handle_file(step1_result_path),
                "layers": [],  # No manual mask
                "composite": None
            },
            garm_img=handle_file(original_garment_path),
            garment_des=garment_description,
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )
        
        end_time = time.time()
        print(f"✅ Step 2 completed in {end_time - start_time:.1f} seconds")
        
        # Save final results
        timestamp = int(time.time())
        final_result_path = f"./examples/results/final_result_{timestamp}.png"
        final_mask_path = f"./examples/results/final_mask_{timestamp}.png"
        
        if len(result) >= 2:
            shutil.copy(result[0], final_result_path)
            shutil.copy(result[1], final_mask_path)
            
            print(f"📸 Final results saved:")
            print(f"   Main result: {final_result_path}")
            print(f"   Mask result: {final_mask_path}")
            
            return final_result_path, final_mask_path
        else:
            print("❌ Unexpected result format from IDM-VTON")
            return None, None
            
    except Exception as e:
        print(f"❌ Step 2 failed: {e}")
        return None, None

def run_two_step_pipeline(person_path, garment_path, garment_description, garment_type="upper_body"):
    """
    Run the complete two-step pipeline
    """
    print("\n" + "="*60)
    print("🎭 Two-Step Virtual Try-On Pipeline")
    print("="*60)
    print(f"👤 Person: {person_path}")
    print(f"👕 Garment: {garment_path}")
    print(f"📝 Description: {garment_description}")
    print(f"🏷️ Type: {garment_type}")
    print("-"*60)
    
    # Check if input files exist
    if not Path(person_path).exists():
        print(f"❌ Person image not found: {person_path}")
        return
    if not Path(garment_path).exists():
        print(f"❌ Garment image not found: {garment_path}")
        return
    
    # Step 1: Initial virtual try-on
    step1_result = step1_virtual_tryon(person_path, garment_path, garment_type)
    if not step1_result:
        print("❌ Pipeline failed at Step 1")
        return
    
    print("-"*60)
    
    # Step 2: IDM-VTON refinement
    final_result, final_mask = step2_idm_vton(step1_result, garment_path, garment_description)
    if not final_result:
        print("❌ Pipeline failed at Step 2")
        return
    
    print("\n🎉 Two-step pipeline completed successfully!")
    print(f"📁 Check results in: ./examples/results/")
    
    return final_result, final_mask

# Example configurations
EXAMPLES = {
    "1": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/gucci upper.jpg",
        "description": "Gucci upper garment refined with IDM-VTON",
        "type": "upper_body"
    },
    "2": {
        "person": "./examples/person_images/korean girl.png", 
        "garment": "./examples/garment_images/gucci upper.jpg",
        "description": "Gucci upper garment for Korean girl",
        "type": "upper_body"
    },
    "3": {
        "person": "./examples/person_images/will_smith.jpg",
        "garment": "./examples/garment_images/gucci upper.jpg", 
        "description": "Gucci upper garment for Will Smith",
        "type": "upper_body"
    },
    "4": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/upper_2.jpg",
        "description": "Alternative upper garment for Arnav",
        "type": "upper_body"
    },
    "5": {
        "person": "./examples/person_images/Full Man.jpg",
        "garment": "./examples/garment_images/upper_3.jpg",
        "description": "Red checkered upper garment for Full Man",
        "type": "upper_body"
    },
    "6": {
        "person": "./examples/person_images/Full Man.jpg",
        "garment": "./examples/garment_images/pants.jpg",
        "description": "Dark cargo pants for Full Man",
        "type": "lower_body"
    },
    "7": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/pants.jpg",
        "description": "Dark cargo pants for Arnav",
        "type": "lower_body"
    },
    "8": {
        "person": "./examples/person_images/korean girl.png",
        "garment": "./examples/garment_images/upper_3.jpg",
        "description": "Red checkered shirt for Korean girl",
        "type": "upper_body"
    }
}

def main():
    """Interactive menu for running examples"""
    print("\n" + "="*60)
    print("🎭 Two-Step Virtual Try-On Pipeline")
    print("Step 1: virtual-try-on → Step 2: IDM-VTON")
    print("="*60)
    
    print("\nAvailable Examples:")
    for key, example in EXAMPLES.items():
        person_name = Path(example['person']).stem
        garment_name = Path(example['garment']).stem
        print(f"{key}. {person_name} + {garment_name}")
    
    print("\nCommands:")
    print("• Enter example number (1-8) to run")
    print("• 'all' to run all examples")
    print("• 'custom' to use custom images")
    print("• 'q' to quit")
    
    while True:
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == 'all':
            print("🚀 Running all examples...")
            for key, example in EXAMPLES.items():
                print(f"\n{'='*40}")
                print(f"Running Example {key}")
                print('='*40)
                run_two_step_pipeline(
                    example['person'], 
                    example['garment'], 
                    example['description'],
                    example['type']
                )
                print("-" * 40)
        elif choice == 'custom':
            person_path = input("Enter person image path: ").strip()
            garment_path = input("Enter garment image path: ").strip()
            description = input("Enter garment description: ").strip()
            garment_type = input("Enter garment type (upper_body/lower_body/dresses) [upper_body]: ").strip() or "upper_body"
            
            run_two_step_pipeline(person_path, garment_path, description, garment_type)
        elif choice in EXAMPLES:
            example = EXAMPLES[choice]
            run_two_step_pipeline(
                example['person'], 
                example['garment'], 
                example['description'],
                example['type']
            )
        else:
            print("❌ Invalid choice. Please enter 1-4, 'all', 'custom', or 'q'")

if __name__ == "__main__":
    main()
