#!/usr/bin/env python3
"""
Sequential Layered Virtual Try-On Pipeline
Step 1: Apply pants using virtual-try-on
Step 2: Apply upper garment using IDM-VTON on the result
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
    exit(1)

def apply_complete_outfit(person_path, pants_path, upper_path, outfit_description):
    """
    Apply complete outfit: pants first, then upper garment
    """
    print("\n" + "="*70)
    print("👔 Sequential Layered Virtual Try-On Pipeline")
    print("="*70)
    print(f"👤 Person: {person_path}")
    print(f"👖 Pants: {pants_path}")  
    print(f"👕 Upper: {upper_path}")
    print(f"📝 Description: {outfit_description}")
    print("-"*70)
    
    timestamp = int(time.time())
    
    # STEP 1: Apply pants using virtual-try-on
    print("\n🚀 STEP 1: Applying pants with virtual-try-on...")
    print("   Model: blackmamba2408/virtual-try-on")
    print("   Garment: Lower body (pants)")
    
    client1 = Client("blackmamba2408/virtual-try-on", hf_token=hf_token)
    
    step1_start = time.time()
    pants_result = client1.predict(
        person_path=handle_file(person_path),
        garment_path=handle_file(pants_path),
        garment_type="lower_body",  # Apply pants
        api_name="/virtual_tryon"
    )
    step1_end = time.time()
    
    # Save pants result
    pants_result_path = f"./examples/results/step1_pants_{timestamp}.png"
    
    if isinstance(pants_result, dict) and 'path' in pants_result:
        shutil.copy(pants_result['path'], pants_result_path)
    elif isinstance(pants_result, str):
        shutil.copy(pants_result, pants_result_path)
    else:
        shutil.copy(pants_result[0] if isinstance(pants_result, (list, tuple)) else pants_result, pants_result_path)
    
    print(f"✅ STEP 1 completed in {step1_end - step1_start:.1f}s")
    print(f"   Result: Person wearing pants → {pants_result_path}")
    
    print("-"*70)
    
    # STEP 2: Apply upper garment using IDM-VTON on the pants result
    print("\n🚀 STEP 2: Applying upper garment with IDM-VTON...")
    print("   Model: blackmamba2408/IDM-VTON")
    print("   Input: Person with pants (from Step 1)")
    print("   Garment: Upper body (shirt/top)")
    
    client2 = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)
    
    step2_start = time.time()
    final_result = client2.predict(
        dict={
            "background": handle_file(pants_result_path),  # Use person with pants as background
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(upper_path),  # Apply upper garment
        garment_des=outfit_description,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )
    step2_end = time.time()
    
    # Save final complete outfit result
    final_outfit_path = f"./examples/results/complete_outfit_{timestamp}.png"
    final_mask_path = f"./examples/results/outfit_mask_{timestamp}.png"
    
    if len(final_result) >= 2:
        shutil.copy(final_result[0], final_outfit_path)
        shutil.copy(final_result[1], final_mask_path)
        
        print(f"✅ STEP 2 completed in {step2_end - step2_start:.1f}s")
        print(f"   Result: Complete outfit → {final_outfit_path}")
        
        total_time = step2_end - step1_start
        print(f"\n🎉 COMPLETE OUTFIT APPLIED!")
        print(f"📸 Results:")
        print(f"   👖 Step 1 (Pants): {pants_result_path}")
        print(f"   👔 Final Outfit: {final_outfit_path}")
        print(f"   🎭 Process Mask: {final_mask_path}")
        print(f"⏱️  Total Time: {total_time:.1f} seconds")
        
        return final_outfit_path, pants_result_path, final_mask_path
    else:
        print("❌ STEP 2 failed - unexpected result format")
        return None, pants_result_path, None

# Example outfit combinations
OUTFIT_EXAMPLES = {
    "1": {
        "person": "./examples/person_images/Full Man.jpg",
        "pants": "./examples/garment_images/pants.jpg", 
        "upper": "./examples/garment_images/gucci upper.jpg",
        "description": "Complete outfit: Dark cargo pants + Gucci upper"
    },
    "2": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "pants": "./examples/garment_images/pants.jpg",
        "upper": "./examples/garment_images/upper_3.jpg", 
        "description": "Complete outfit: Dark cargo pants + Red checkered shirt"
    },
    "3": {
        "person": "./examples/person_images/Full Man.jpg",
        "pants": "./examples/garment_images/pants.jpg",
        "upper": "./examples/garment_images/upper_2.jpg",
        "description": "Complete outfit: Dark cargo pants + Alternative upper"
    },
    "4": {
        "person": "./examples/person_images/will_smith.jpg", 
        "pants": "./examples/garment_images/pants.jpg",
        "upper": "./examples/garment_images/gucci upper.jpg",
        "description": "Complete outfit: Dark cargo pants + Gucci upper for Will Smith"
    },
    "5": {
        "person": "./examples/person_images/korean girl.png",
        "pants": "./examples/garment_images/pants.jpg",
        "upper": "./examples/garment_images/upper_3.jpg",
        "description": "Complete outfit: Dark cargo pants + Red checkered shirt for Korean girl"
    }
}

def main():
    """Interactive menu for complete outfit try-on"""
    print("\n" + "="*70)
    print("👔 Sequential Layered Virtual Try-On")
    print("Step 1: Pants (virtual-try-on) → Step 2: Upper (IDM-VTON)")
    print("="*70)
    
    print("\nAvailable Complete Outfit Examples:")
    for key, example in OUTFIT_EXAMPLES.items():
        person_name = Path(example['person']).stem
        pants_name = Path(example['pants']).stem  
        upper_name = Path(example['upper']).stem
        print(f"{key}. {person_name} → {pants_name} + {upper_name}")
    
    print("\nCommands:")
    print("• Enter example number (1-5) to try complete outfit")
    print("• 'all' to run all outfit combinations")
    print("• 'custom' to use your own garments")
    print("• 'q' to quit")
    
    while True:
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == 'all':
            print("🚀 Trying all complete outfits...")
            for key, example in OUTFIT_EXAMPLES.items():
                print(f"\n{'='*50}")
                print(f"Outfit Example {key}")
                print('='*50)
                apply_complete_outfit(
                    example['person'],
                    example['pants'], 
                    example['upper'],
                    example['description']
                )
                print("-" * 50)
        elif choice == 'custom':
            person_path = input("Enter person image path: ").strip()
            pants_path = input("Enter pants image path: ").strip() 
            upper_path = input("Enter upper garment path: ").strip()
            description = input("Enter outfit description: ").strip()
            
            apply_complete_outfit(person_path, pants_path, upper_path, description)
        elif choice in OUTFIT_EXAMPLES:
            example = OUTFIT_EXAMPLES[choice]
            apply_complete_outfit(
                example['person'],
                example['pants'],
                example['upper'], 
                example['description']
            )
        else:
            print("❌ Invalid choice. Please enter 1-5, 'all', 'custom', or 'q'")

if __name__ == "__main__":
    main()
