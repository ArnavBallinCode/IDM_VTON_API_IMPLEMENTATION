from gradio_client import Client, handle_file
import os
from pathlib import Path

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

client = Client("blackmamba2408/IDM-VTON", hf_token=hf_token)

result = client.predict(
    dict={
        "background": handle_file("/Users/arnavangarkar/Desktop/Arnav/VITON/Yisol idm/Arnav_A.jpg"),
        "layers": [],  # No manual mask
        "composite": None
    },
    garm_img=handle_file("/Users/arnavangarkar/Desktop/Arnav/VITON/Yisol idm/gucci upper.jpg"),
    garment_des="Gucci upper garment",
    is_checked=True,
    is_checked_crop=False,
    denoise_steps=30,
    seed=42,
    api_name="/tryon"
)

print("Result:", result)
