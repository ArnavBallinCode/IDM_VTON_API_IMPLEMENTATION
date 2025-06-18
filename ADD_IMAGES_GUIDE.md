# Adding New Images Guide

## 🖼️ New Images to Add

You need to manually save these 3 images to complete the setup:

### 1. Full Man.jpg → examples/person_images/
- **Source**: Second attachment (full body male in blue shirt)
- **Description**: Full body male model, perfect for complete outfit try-ons
- **Usage**: Great for both upper and lower body garments

### 2. pants.jpg → examples/garment_images/
- **Source**: First attachment (dark cargo pants)
- **Description**: Dark cargo/work pants with utility pockets
- **Usage**: Lower body garment, works with virtual-try-on model
- **Type**: "lower_body" in garment_type parameter

### 3. upper_3.jpg → examples/garment_images/
- **Source**: Third attachment (red checkered shirt)
- **Description**: Red and white checkered casual shirt
- **Usage**: Upper body garment, casual style
- **Type**: "upper_body" in garment_type parameter

## 📝 How to Add Them

1. **Save the attachments**:
   - Right-click each image attachment
   - Save to the corresponding folder with exact filename

2. **Verify files**:
   ```bash
   ls -la examples/person_images/Full\ Man.jpg
   ls -la examples/garment_images/pants.jpg  
   ls -la examples/garment_images/upper_3.jpg
   ```

3. **Test with new combinations**:
   ```bash
   python two_step_pipeline.py
   # Try options 5-8 for new combinations!
   ```

## 🎯 New Example Options

Once images are added, you'll have these new options:

**5.** Full Man + Red Checkered Shirt (upper_body)
**6.** Full Man + Dark Cargo Pants (lower_body) 
**7.** Arnav + Dark Cargo Pants (lower_body)
**8.** Korean Girl + Red Checkered Shirt (upper_body)

## 🔧 File Validation

Run this to check all files are properly added:
```bash
python test_setup.py  # Will verify all required files exist
```

The system will automatically detect the new images and include them in the pipeline!
