# IDM-VTON Virtual Try-On

A Python script for virtual try-on using the IDM-VTON (Improving Diffusion Models for Authentic Virtual Try-on in the Wild) model via Hugging Face Spaces API.

## Overview

This project allows you to virtually try on garments on person images using state-of-the-art diffusion models. The script uses your private Hugging Face Pro space for faster processing and no rate limits.

## Features

- ✨ Virtual garment try-on using IDM-VTON model
- 🚀 Private Hugging Face Pro space integration
- 🔒 Secure token-based authentication
- 🎨 High-quality diffusion-based results
- 📸 Support for various image formats

## Prerequisites

- Python 3.7+
- Hugging Face Pro account
- Conda environment (recommended)

## Installation

1. **Clone or download this repository**

2. **Create and activate conda environment:**
   ```bash
   conda create -n viton python=3.10
   conda activate viton
   ```

3. **Install required packages:**
   ```bash
   pip install gradio_client huggingface_hub python-dotenv
   ```

4. **Install Hugging Face CLI (optional but recommended):**
   ```bash
   pip install --upgrade huggingface_hub[cli]
   ```

## Setup

### 1. Hugging Face Account & CLI Setup

#### **Step 1: Create HF Pro Account**
1. Sign up at [Hugging Face](https://huggingface.co/)
2. Upgrade to [HF Pro](https://huggingface.co/pricing) for private spaces and priority access

#### **Step 2: Install and Login to HF CLI**
```bash
# Install HF CLI
pip install --upgrade huggingface_hub[cli]

# Login to HF CLI (this will prompt for your token)
huggingface-cli login

# Verify login
huggingface-cli whoami
```

#### **Step 3: Alternative - Manual Token Setup**
If you prefer not to use HF CLI login:

1. **Get your token:**
   ```bash
   # Go to: https://huggingface.co/settings/tokens
   # Create new token with "Read" or "Write" access
   ```

2. **Set up token (choose one method):**

   **Method A: Using .env file (recommended for development)**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env file and add your token
   echo "HUGGINGFACE_TOKEN=hf_your_actual_token_here" > .env
   ```

   **Method B: Environment variable (for production)**
   ```bash
   # Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
   export HUGGINGFACE_TOKEN="hf_your_token_here"
   
   # Or set for current session only
   export HUGGINGFACE_TOKEN="hf_your_token_here"
   ```

   **Method C: Using HF CLI to set token**
   ```bash
   # Set token using CLI
   huggingface-cli login --token hf_your_token_here
   ```

### 2. Private Space Setup & Configuration

#### **Step 1: Duplicate the Original Space**

**Option A: Using HF CLI (Recommended)**
```bash
# Duplicate the space to your account
huggingface-cli repo duplicate yisol/IDM-VTON your_username/IDM-VTON --type space

# Or with specific settings
huggingface-cli repo duplicate yisol/IDM-VTON your_username/IDM-VTON \
  --type space \
  --private \
  --exist-ok
```

**Option B: Using Web Interface**
1. Go to [yisol/IDM-VTON](https://huggingface.co/spaces/yisol/IDM-VTON)
2. Click "⋯" menu → "Duplicate this Space"
3. Set your space name: `your_username/IDM-VTON`
4. ✅ Check "Private" if you want it private
5. Click "Duplicate Space"

#### **Step 2: Configure Your Private Space**

1. **Wait for space to build** (may take 5-10 minutes)
2. **Check space status:**
   ```bash
   # Check if your space is running
   huggingface-cli api info your_username/IDM-VTON --repo-type space
   ```

3. **Test space accessibility:**
   ```bash
   # Test API endpoint
   curl -H "Authorization: Bearer $HUGGINGFACE_TOKEN" \
        https://huggingface.co/api/spaces/your_username/IDM-VTON
   ```

#### **Step 3: Space Management Commands**

```bash
# View your spaces
huggingface-cli api list-repos --type space

# Check space info
huggingface-cli api info your_username/IDM-VTON --repo-type space

# Restart space if needed
huggingface-cli api restart-space your_username/IDM-VTON

# Make space private/public
huggingface-cli api update-repo-visibility your_username/IDM-VTON \
  --repo-type space --private

# Delete space (be careful!)
# huggingface-cli api delete-repo your_username/IDM-VTON --repo-type space
```

### 3. Token Permissions & Security

#### **Required Token Permissions:**
- **Read**: For accessing public spaces and models ✅
- **Write**: For managing your own spaces and repositories ✅  
- **Fine-grained**: For specific repository access (advanced)

#### **Security Best Practices:**
```bash
# 1. Never commit tokens to git
echo ".env" >> .gitignore
echo "*.token" >> .gitignore

# 2. Use environment variables in production
export HUGGINGFACE_TOKEN="hf_your_token"

# 3. Rotate tokens regularly
huggingface-cli auth token --new

# 4. Check token validity
huggingface-cli auth whoami
```

#### **Troubleshooting Authentication:**
```bash
# Clear cached credentials
huggingface-cli auth clear

# Re-login
huggingface-cli login

# Test authentication
python -c "from huggingface_hub import HfApi; print(HfApi().whoami())"
```

### 4. Advanced Space Configuration

#### **Space Monitoring & Health Checks**
```bash
# Check space status and logs
huggingface-cli api info your_username/IDM-VTON --repo-type space

# Monitor space runtime
python -c "
from gradio_client import Client
import time

try:
    client = Client('your_username/IDM-VTON')
    print('✅ Space is running and accessible')
    print(f'Space URL: {client.src}')
except Exception as e:
    print(f'❌ Space issue: {e}')
"

# Check space build status
curl -H "Authorization: Bearer $HUGGINGFACE_TOKEN" \
     "https://huggingface.co/api/spaces/your_username/IDM-VTON/runtime"
```

#### **Space Configuration Management**
```bash
# Clone space repository for local editing
git clone https://huggingface.co/spaces/your_username/IDM-VTON
cd IDM-VTON

# Edit configuration files locally
# - app.py (main application)
# - requirements.txt (dependencies) 
# - README.md (space documentation)

# Push changes
git add .
git commit -m "Update space configuration"
git push
```

#### **Environment Variables for Spaces**
```bash
# Set environment variables in your space
# Go to: https://huggingface.co/spaces/your_username/IDM-VTON/settings

# Common variables for IDM-VTON:
# HF_TOKEN=your_token_here
# GRADIO_SERVER_PORT=7860
# GRADIO_ROOT_PATH=/
```

#### **Space Hardware & Performance**
```bash
# Check available hardware tiers
huggingface-cli api whoami

# For HF Pro users - upgrade hardware:
# Go to space settings → Hardware → Select GPU
# Options: CPU basic (free) → T4 small → A10G → A100

# Monitor space performance
python -c "
import time
from gradio_client import Client

client = Client('your_username/IDM-VTON')
start_time = time.time()

# Test inference speed
result = client.predict('test', api_name='/tryon')
end_time = time.time()

print(f'Inference time: {end_time - start_time:.2f} seconds')
"
```

## Usage

### Basic Usage

1. **Prepare your images:**
   - Place a person image in the directory (e.g., `person.jpg`)
   - Place a garment image in the directory (e.g., `garment.jpg`)

2. **Update the script:**
   - Open `inference.py`
   - Update the file paths to your images
   - Update the Hugging Face space name to yours

3. **Run the script:**
   ```bash
   conda activate viton
   python inference.py
   ```

### Example

```python
from gradio_client import Client, handle_file
import os

# Authentication
hf_token = os.getenv("HUGGINGFACE_TOKEN")
client = Client("your_username/IDM-VTON", hf_token=hf_token)

# Inference
result = client.predict(
    dict={
        "background": handle_file("./person_image.jpg"),
        "layers": [],
        "composite": None
    },
    garm_img=handle_file("./garment_image.jpg"),
    garment_des="Description of the garment",
    is_checked=True,
    is_checked_crop=False,
    denoise_steps=30,
    seed=42,
    api_name="/tryon"
)
```

## Quick Start Guide

For experienced users, here's the fastest way to get started:

```bash
# 1. Setup environment
conda create -n viton python=3.10 -y
conda activate viton
pip install gradio_client huggingface_hub python-dotenv

# 2. Login to HF
huggingface-cli login
# Enter your token when prompted

# 3. Duplicate space (replace 'your_username' with your HF username)
huggingface-cli repo duplicate yisol/IDM-VTON your_username/IDM-VTON --type space --private

# 4. Wait for space to build (check status)
huggingface-cli api info your_username/IDM-VTON --repo-type space

# 5. Setup token file
echo "HUGGINGFACE_TOKEN=$(huggingface-cli auth token)" > .env

# 6. Update inference.py with your space name and run
python inference.py
```

**⚠️ Important**: Replace `your_username` with your actual Hugging Face username!

## File Structure

```
├── inference.py          # Main inference script
├── README.md            # This file
├── Arnav_A.jpg          # Person image (example)
├── gucci upper.jpg      # Garment image (example)
├── result_tryon_*.png   # Generated try-on results
└── result_mask_*.png    # Generated mask outputs
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `background` | Person image to try clothes on | Required |
| `garm_img` | Garment image to be worn | Required |
| `garment_des` | Text description of garment | Required |
| `is_checked` | Enable garment processing | `True` |
| `is_checked_crop` | Enable automatic cropping | `False` |
| `denoise_steps` | Number of denoising steps | `30` |
| `seed` | Random seed for reproducibility | `42` |

## Tips for Best Results

### Person Images
- Use high-resolution images (512x512 or higher)
- Ensure the person is clearly visible and well-lit
- Front-facing pose works best
- Minimal background clutter

### Garment Images
- Use clean, isolated garment images
- Good lighting and contrast
- Flat lay or on mannequin works well
- Clear view of the garment details

## Troubleshooting

### Common Issues

1. **401 Unauthorized Error**
   - Check your Hugging Face token
   - Ensure the token has read access
   - Verify your space name is correct

2. **IndexError**
   - Check image file paths are correct
   - Ensure images are accessible
   - Verify image formats (JPG, PNG supported)

3. **Environment Issues**
   - Activate the conda environment: `conda activate viton`
   - Reinstall packages if needed: `pip install --upgrade gradio_client`

### Debug Mode

Add this to your script for more detailed output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Sample Results

The script generates two outputs:
- **Main result**: Virtual try-on image showing the person wearing the garment
- **Mask result**: Processing mask used by the model

## Performance

- **Processing time**: ~30-60 seconds per image (depends on HF Pro queue)
- **Quality**: High-resolution diffusion-based results
- **Rate limits**: None (with HF Pro space)

## License

This project uses the IDM-VTON model. Please check the original model's license and terms of use.

## Credits

- **IDM-VTON Model**: [yisol/IDM-VTON](https://huggingface.co/spaces/yisol/IDM-VTON)
- **Gradio Client**: For API integration
- **Hugging Face**: For hosting and infrastructure

## Contributing

Feel free to submit issues and enhancement requests!

## Support

For issues with:
- **This script**: Create an issue in this repository
- **IDM-VTON model**: Check the original space documentation
- **Hugging Face**: Contact HF support

---

**Happy Virtual Try-On! 👕✨**
