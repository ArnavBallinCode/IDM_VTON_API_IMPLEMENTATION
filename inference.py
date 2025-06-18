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
    print("Please set your Hugging Face token!")
    print("You can either:")
    print("1. Create .env file with: HUGGINGFACE_TOKEN=your_token_here")
    print("2. Set environment variable: export HUGGINGFACE_TOKEN=your_token_here")
    exit(1)

# Configuration
PERSON_IMAGE = "./examples/person_images/Full Man.jpg"
PANTS_IMAGE = "./examples/garment_images/pants.jpg"
UPPER_IMAGE = "./examples/garment_images/gucci upper.jpg"
OUTFIT_DESCRIPTION = "Complete outfit: Dark cargo pants + Gucci upper"
USE_LAYERED_APPROACH = True  # True for pants→upper, False for single garment
USE_TWO_STEP = True  # Set to False for direct IDM-VTON only

if USE_LAYERED_APPROACH:
    print("👔 Layered Virtual Try-On Processing")
    print("="*50)
    print(f"👤 Person: {PERSON_IMAGE}")
    print(f"👖 Pants: {PANTS_IMAGE}")
    print(f"👕 Upper: {UPPER_IMAGE}")
    print(f"📝 Description: {OUTFIT_DESCRIPTION}")
    print(f"🔄 Mode: Layered approach (Pants → Upper)")
else:
    print("🎭 Virtual Try-On Processing")
    print("="*50)
    print(f"👤 Person: {PERSON_IMAGE}")
    print(f"👕 Garment: {UPPER_IMAGE}")
    print(f"📝 Description: {OUTFIT_DESCRIPTION}")
    print(f"🔄 Mode: {'Two-step pipeline' if USE_TWO_STEP else 'Direct IDM-VTON'}")
print("="*50)

if USE_LAYERED_APPROACH:
    # Layered approach: pants first, then upper garment
    print("\n🚀 Step 1: Applying pants with virtual-try-on...")
    
    client1 = Client("blackmamba2408/virtual-try-on", hf_token=hf_token)
    
    pants_result = client1.predict(
        person_path=handle_file(PERSON_IMAGE),
        garment_path=handle_file(PANTS_IMAGE),
        garment_type="lower_body",  # Apply pants first
        api_name="/virtual_tryon"
    )
    
    # Save pants result
    timestamp = int(time.time())
    pants_path = f"./examples/results/step1_pants_{timestamp}.png"
    
    if isinstance(pants_result, dict) and 'path' in pants_result:
        shutil.copy(pants_result['path'], pants_path)
    elif isinstance(pants_result, str):
        shutil.copy(pants_result, pants_path)
    else:
        shutil.copy(pants_result[0] if isinstance(pants_result, (list, tuple)) else pants_result, pants_path)
    
    print(f"✅ Step 1 completed! Person with pants: {pants_path}")
    
    print("\n🚀 Step 2: Applying upper garment with IDM-VTON...")
    
    client2 = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)
    
    final_result = client2.predict(
        dict={
            "background": handle_file(pants_path),  # Use person with pants as background
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(UPPER_IMAGE),  # Apply upper garment
        garment_des=OUTFIT_DESCRIPTION,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )
    
    print("✅ Step 2 completed! Complete outfit applied!")

elif USE_TWO_STEP:
    # Two-step pipeline: virtual-try-on → IDM-VTON (same garment)
    print("\n🚀 Step 1: Initial processing with virtual-try-on...")
    
    client1 = Client("blackmamba2408/virtual-try-on", hf_token=hf_token)
    
    step1_result = client1.predict(
        person_path=handle_file(PERSON_IMAGE),
        garment_path=handle_file(UPPER_IMAGE),
        garment_type="upper_body",
        api_name="/virtual_tryon"
    )
    
    # Save step 1 result
    timestamp = int(time.time())
    step1_path = f"./examples/results/step1_{timestamp}.png"
    
    if isinstance(step1_result, dict) and 'path' in step1_result:
        shutil.copy(step1_result['path'], step1_path)
    elif isinstance(step1_result, str):
        shutil.copy(step1_result, step1_path)
    else:
        shutil.copy(step1_result[0] if isinstance(step1_result, (list, tuple)) else step1_result, step1_path)
    
    print(f"✅ Step 1 completed! Intermediate result: {step1_path}")
    
    print("\n🚀 Step 2: Refinement with IDM-VTON...")
    
    client2 = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)
    
    final_result = client2.predict(
        dict={
            "background": handle_file(step1_path),  # Use step 1 result as background
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(UPPER_IMAGE),
        garment_des=OUTFIT_DESCRIPTION,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )
    
    print("✅ Step 2 completed!")
    
else:
    # Direct IDM-VTON processing
    print("\n🚀 Direct IDM-VTON processing...")
    
    client = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)

    final_result = client.predict(
        dict={
            "background": handle_file(PERSON_IMAGE),
            "layers": [],
            "composite": None
        },
        garm_img=handle_file(UPPER_IMAGE),
        garment_des=OUTFIT_DESCRIPTION,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )

# Save final results
if not 'timestamp' in locals():
    timestamp = int(time.time())

if USE_LAYERED_APPROACH:
    final_tryon_path = f"./examples/results/complete_outfit_{timestamp}.png"
    final_mask_path = f"./examples/results/outfit_mask_{timestamp}.png"
else:
    final_tryon_path = f"./examples/results/final_tryon_{timestamp}.png"
    final_mask_path = f"./examples/results/final_mask_{timestamp}.png"

if len(final_result) >= 2:
    shutil.copy(final_result[0], final_tryon_path)
    shutil.copy(final_result[1], final_mask_path)
    
    print(f"\n🎉 Processing completed!")
    print(f"📸 Results saved:")
    print(f"   Main result: {final_tryon_path}")
    print(f"   Mask result: {final_mask_path}")
    if USE_TWO_STEP:
        print(f"   Step 1 result: {step1_path}")

print("\nResult paths:", final_result)
