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
        "garment": "./examples/garment_images/shirts/gucci upper.jpg",
        "description": "Gucci upper garment refined with IDM-VTON",
        "type": "upper_body"
    },
    "2": {
        "person": "./examples/person_images/korean girl.png", 
        "garment": "./examples/garment_images/shirts/gucci upper.jpg",
        "description": "Gucci upper garment for Korean girl",
        "type": "upper_body"
    },
    "3": {
        "person": "./examples/person_images/will_smith.jpg",
        "garment": "./examples/garment_images/shirts/gucci upper.jpg", 
        "description": "Gucci upper garment for Will Smith",
        "type": "upper_body"
    },
    "4": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/shirts/upper_2.jpg",
        "description": "Alternative upper garment for Arnav",
        "type": "upper_body"
    },
    "5": {
        "person": "./examples/person_images/Full Man.jpg",
        "garment": "./examples/garment_images/shirts/upper_2.jpg",
        "description": "Alternative upper garment for Full Man",
        "type": "upper_body"
    },
    "6": {
        "person": "./examples/person_images/Full Man.jpg",
        "garment": "./examples/garment_images/pants/pants.jpg",
        "description": "Dark cargo pants for Full Man",
        "type": "lower_body"
    },
    "7": {
        "person": "./examples/person_images/Arnav_A.jpg",
        "garment": "./examples/garment_images/pants/pants.jpg",
        "description": "Dark cargo pants for Arnav",
        "type": "lower_body"
    },
    "8": {
        "person": "./examples/person_images/korean girl.png",
        "garment": "./examples/garment_images/shirts/upper_2.jpg",
        "description": "Alternative upper garment for Korean girl",
        "type": "upper_body"
    },
    "9": {
        "person": "./examples/person_images/Joe.jpg",
        "garment": "./examples/garment_images/shirts/gucci upper.jpg",
        "description": "Gucci upper garment for Joe",
        "type": "upper_body"
    },
    "10": {
        "person": "./examples/person_images/Joe.jpg",
        "garment": "./examples/garment_images/shirts/upper_2.jpg",
        "description": "Alternative upper garment for Joe",
        "type": "upper_body"
    },
    "11": {
        "person": "./examples/person_images/Joe.jpg",
        "garment": "./examples/garment_images/pants/pants.jpg",
        "description": "Dark cargo pants for Joe",
        "type": "lower_body"
    }
}

def auto_process_new_garment(garment_path, garment_type):
    """Auto-process new garment by moving it to appropriate folder"""
    garment_images_dir = Path("./examples/garment_images")
    filename = Path(garment_path).name
    
    if garment_type == "upper_body":
        dest_dir = garment_images_dir / "shirts"
        dest_path = dest_dir / filename
    else:  # lower_body
        dest_dir = garment_images_dir / "pants"
        dest_path = dest_dir / filename
    
    # Create directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)
    
    # Copy the file if it's not already in the right place
    if not dest_path.exists():
        shutil.copy(garment_path, dest_path)
        print(f"✅ New garment auto-processed and saved to: {dest_path}")
    
    return str(dest_path)

def list_available_items():
    """List all available persons and garments"""
    person_dir = Path("./examples/person_images")
    shirts_dir = Path("./examples/garment_images/shirts")
    pants_dir = Path("./examples/garment_images/pants")
    
    # List persons
    persons = []
    if person_dir.exists():
        persons = [f for f in person_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    # List shirts
    shirts = []
    if shirts_dir.exists():
        shirts = [f for f in shirts_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    # List pants
    pants = []
    if pants_dir.exists():
        pants = [f for f in pants_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
    
    return persons, shirts, pants

def select_person():
    """Interactive person selection"""
    persons, _, _ = list_available_items()
    
    if not persons:
        print("❌ No person images found in ./examples/person_images/")
        custom_path = input("Enter custom person image path: ").strip()
        if os.path.exists(custom_path):
            return custom_path
        else:
            print("❌ File not found!")
            return None
    
    print("\n👤 Available Persons:")
    for i, person in enumerate(persons, 1):
        print(f"{i}. {person.stem}")
    
    print(f"{len(persons) + 1}. Add new person image")
    
    while True:
        try:
            choice = input(f"\nSelect person (1-{len(persons) + 1}): ").strip()
            
            if choice == str(len(persons) + 1):
                custom_path = input("Enter new person image path: ").strip()
                if os.path.exists(custom_path):
                    # Copy to person images folder
                    filename = Path(custom_path).name
                    dest_path = Path("./examples/person_images") / filename
                    shutil.copy(custom_path, dest_path)
                    print(f"✅ New person image added: {dest_path}")
                    return str(dest_path)
                else:
                    print("❌ File not found!")
                    continue
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(persons):
                return str(persons[choice_idx])
            else:
                print(f"❌ Please enter a number between 1 and {len(persons) + 1}")
        except ValueError:
            print("❌ Please enter a valid number")

def select_shirt():
    """Interactive shirt selection"""
    _, shirts, _ = list_available_items()
    
    print("\n👕 Select Shirt:")
    print("1. Choose from available shirts")
    print("2. Add new shirt")
    print("3. Skip shirt")
    
    while True:
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "3":
                return None, None, None
            
            elif choice == "2":
                custom_path = input("Enter new shirt image path: ").strip()
                if not os.path.exists(custom_path):
                    print("❌ File not found!")
                    continue
                
                processed_path = auto_process_new_garment(custom_path, "upper_body")
                description = input("Enter shirt description: ").strip() or "Custom shirt"
                return processed_path, description, "upper_body"
            
            elif choice == "1":
                if not shirts:
                    print("❌ No shirts found. Please add one or skip.")
                    continue
                
                print("\n👕 Available Shirts:")
                for i, shirt in enumerate(shirts, 1):
                    print(f"{i}. {shirt.stem}")
                
                shirt_choice = input(f"Select shirt (1-{len(shirts)}): ").strip()
                shirt_idx = int(shirt_choice) - 1
                
                if 0 <= shirt_idx < len(shirts):
                    selected_shirt = str(shirts[shirt_idx])
                    description = input("Enter shirt description: ").strip() or f"{shirts[shirt_idx].stem} shirt"
                    return selected_shirt, description, "upper_body"
                else:
                    print(f"❌ Please enter a number between 1 and {len(shirts)}")
            
            else:
                print("❌ Please enter 1, 2, or 3")
                
        except ValueError:
            print("❌ Please enter a valid number")

def select_pants():
    """Interactive pants selection"""
    _, _, pants = list_available_items()
    
    print("\n👖 Select Pants:")
    print("1. Choose from available pants")
    print("2. Add new pants")
    print("3. Skip pants")
    
    while True:
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "3":
                return None, None, None
            
            elif choice == "2":
                custom_path = input("Enter new pants image path: ").strip()
                if not os.path.exists(custom_path):
                    print("❌ File not found!")
                    continue
                
                processed_path = auto_process_new_garment(custom_path, "lower_body")
                description = input("Enter pants description: ").strip() or "Custom pants"
                return processed_path, description, "lower_body"
            
            elif choice == "1":
                if not pants:
                    print("❌ No pants found. Please add one or skip.")
                    continue
                
                print("\n👖 Available Pants:")
                for i, pant in enumerate(pants, 1):
                    print(f"{i}. {pant.stem}")
                
                pant_choice = input(f"Select pants (1-{len(pants)}): ").strip()
                pant_idx = int(pant_choice) - 1
                
                if 0 <= pant_idx < len(pants):
                    selected_pants = str(pants[pant_idx])
                    description = input("Enter pants description: ").strip() or f"{pants[pant_idx].stem} pants"
                    return selected_pants, description, "lower_body"
                else:
                    print(f"❌ Please enter a number between 1 and {len(pants)}")
            
            else:
                print("❌ Please enter 1, 2, or 3")
                
        except ValueError:
            print("❌ Please enter a valid number")

def select_garment():
    """Interactive garment selection - LEGACY FUNCTION"""
    _, shirts, pants = list_available_items()
    
    print("\n👕 Select Garment Type:")
    print("1. Shirts/Upper Body")
    print("2. Pants/Lower Body")
    print("3. Add new garment")
    
    while True:
        try:
            type_choice = input("\nSelect type (1-3): ").strip()
            
            if type_choice == "3":
                custom_path = input("Enter new garment image path: ").strip()
                if not os.path.exists(custom_path):
                    print("❌ File not found!")
                    continue
                
                garment_type_input = input("Is this upper_body or lower_body? [upper_body]: ").strip() or "upper_body"
                processed_path = auto_process_new_garment(custom_path, garment_type_input)
                description = input("Enter garment description: ").strip() or "Custom garment"
                return processed_path, description, garment_type_input
            
            elif type_choice == "1":
                if not shirts:
                    print("❌ No shirts found. Please add one.")
                    continue
                
                print("\n👕 Available Shirts:")
                for i, shirt in enumerate(shirts, 1):
                    print(f"{i}. {shirt.stem}")
                
                shirt_choice = input(f"Select shirt (1-{len(shirts)}): ").strip()
                shirt_idx = int(shirt_choice) - 1
                
                if 0 <= shirt_idx < len(shirts):
                    selected_shirt = str(shirts[shirt_idx])
                    description = input("Enter shirt description: ").strip() or f"{shirts[shirt_idx].stem} shirt"
                    return selected_shirt, description, "upper_body"
                else:
                    print(f"❌ Please enter a number between 1 and {len(shirts)}")
            
            elif type_choice == "2":
                if not pants:
                    print("❌ No pants found. Please add one.")
                    continue
                
                print("\n👖 Available Pants:")
                for i, pant in enumerate(pants, 1):
                    print(f"{i}. {pant.stem}")
                
                pant_choice = input(f"Select pants (1-{len(pants)}): ").strip()
                pant_idx = int(pant_choice) - 1
                
                if 0 <= pant_idx < len(pants):
                    selected_pants = str(pants[pant_idx])
                    description = input("Enter pants description: ").strip() or f"{pants[pant_idx].stem} pants"
                    return selected_pants, description, "lower_body"
                else:
                    print(f"❌ Please enter a number between 1 and {len(pants)}")
            
            else:
                print("❌ Please enter 1, 2, or 3")
                
        except ValueError:
            print("❌ Please enter a valid number")

def main():
    """Interactive virtual try-on interface"""
    print("\n" + "="*60)
    print("🎭 Two-Step Virtual Try-On Pipeline")
    print("Step 1: virtual-try-on → Step 2: IDM-VTON")
    print("="*60)
    
    while True:
        print("\n🎯 Main Menu:")
        print("1. Start Complete Outfit Try-On (Shirt + Pants)")
        print("2. Start Single Garment Try-On")
        print("3. Run All Examples (Legacy)")
        print("4. Quit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "4":
            print("👋 Goodbye!")
            break
        
        elif choice == "3":
            print("🚀 Running all predefined examples...")
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
        
        elif choice == "2":
            print("\n🎬 Starting Single Garment Try-On...")
            
            # Step 1: Select person
            person_path = select_person()
            if not person_path:
                continue
            
            # Step 2: Select single garment (legacy function)
            garment_result = select_garment()
            if not garment_result:
                continue
            
            garment_path, description, garment_type = garment_result
            
            # Step 3: Confirm and run
            print(f"\n✅ Configuration:")
            print(f"Person: {Path(person_path).name}")
            print(f"Garment: {Path(garment_path).name}")
            print(f"Description: {description}")
            print(f"Type: {garment_type}")
            
            confirm = input("\nProceed with virtual try-on? (y/n) [y]: ").strip().lower() or "y"
            
            if confirm == "y":
                run_two_step_pipeline(person_path, garment_path, description, garment_type)
            else:
                print("❌ Try-on cancelled.")
        
        elif choice == "1":
            print("\n🎬 Starting Complete Outfit Try-On...")
            
            # Step 1: Select person
            person_path = select_person()
            if not person_path:
                continue
            
            # Step 2: Select shirt
            print(f"\n👤 Selected person: {Path(person_path).name}")
            shirt_result = select_shirt()
            
            # Step 3: Select pants
            pants_result = select_pants()
            
            # Check if at least one garment is selected
            if not shirt_result[0] and not pants_result[0]:
                print("❌ You must select at least one garment (shirt or pants)!")
                continue
            
            # Process selected garments
            garments_to_process = []
            
            if shirt_result[0]:  # If shirt is selected
                garments_to_process.append({
                    'path': shirt_result[0],
                    'description': shirt_result[1],
                    'type': shirt_result[2],
                    'name': 'Shirt'
                })
            
            if pants_result[0]:  # If pants is selected
                garments_to_process.append({
                    'path': pants_result[0],
                    'description': pants_result[1],
                    'type': pants_result[2],
                    'name': 'Pants'
                })
            
            # Show configuration
            print(f"\n✅ Complete Outfit Configuration:")
            print(f"Person: {Path(person_path).name}")
            for i, garment in enumerate(garments_to_process, 1):
                print(f"{garment['name']}: {Path(garment['path']).name} - {garment['description']}")
            
            confirm = input(f"\nProceed with {len(garments_to_process)} garment(s) try-on? (y/n) [y]: ").strip().lower() or "y"
            
            if confirm == "y":
                # Process each garment
                for i, garment in enumerate(garments_to_process, 1):
                    print(f"\n{'='*50}")
                    print(f"Processing {garment['name']} ({i}/{len(garments_to_process)})")
                    print('='*50)
                    
                    run_two_step_pipeline(
                        person_path, 
                        garment['path'], 
                        garment['description'], 
                        garment['type']
                    )
                    
                    if i < len(garments_to_process):
                        input("\n⏸️  Press Enter to continue to next garment...")
                
                print(f"\n🎉 Complete outfit try-on finished! Check results folder.")
            else:
                print("❌ Try-on cancelled.")
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4")

if __name__ == "__main__":
    main()
