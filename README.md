# IDM-VTON Virtual Try-On

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![HuggingFace](https://img.shields.io/badge/🤗-Hugging%20Face-yellow.svg)
![AI](https://img.shields.io/badge/AI-Diffusion%20Models-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)

A Python script for virtual try-on using the IDM-VTON (Improving Diffusion Models for Authentic Virtual Try-on in the Wild) model via Hugging Face Spaces API.

> 🚀 **Try on any garment on any person with AI-powered precision!**

## 🎭 Examples & Results

See the magic of AI-powered virtual try-on! Here are real results from our example images:

### Example Results Table

<table>
<tr>
<th width="25%">👤 Person</th>
<th width="25%">👕 Garment</th>
<th width="25%">✨ Result</th>
<th width="25%">📝 Description</th>
</tr>
<tr>
<td align="center">
<img src="examples/person_images/Arnav_A.jpg" width="150" alt="Arnav"><br>
<em>Arnav A.</em>
</td>
<td align="center">
<img src="examples/garment_images/gucci upper.jpg" width="150" alt="Gucci Upper"><br>
<em>Gucci Upper</em>
</td>
<td align="center">
<img src="examples/results/result_tryon_arnav.png" width="150" alt="Result"><br>
<em>Virtual Try-On</em>
</td>
<td>
<strong>Young Male + Luxury Garment</strong><br>
Perfect fit demonstration with premium Gucci upper garment on young male subject
</td>
</tr>
<tr>
<td align="center">
<img src="examples/person_images/korean girl.png" width="150" alt="Korean Girl"><br>
<em>Korean Girl</em>
</td>
<td align="center">
<img src="examples/garment_images/gucci upper.jpg" width="150" alt="Gucci Upper"><br>
<em>Gucci Upper</em>
</td>
<td align="center">
<img src="examples/results/result_tryon.png" width="150" alt="Result"><br>
<em>Virtual Try-On</em>
</td>
<td>
<strong>Female + Clean Background</strong><br>
Excellent garment transfer with clean background preservation and natural fitting
</td>
</tr>
<tr>
<td align="center">
<img src="examples/person_images/will_smith.jpg" width="150" alt="Will Smith"><br>
<em>Will Smith</em>
</td>
<td align="center">
<img src="examples/garment_images/upper_2.jpg" width="150" alt="Alternative Upper"><br>
<em>Alternative Upper</em>
</td>
<td align="center">
⚡ <strong>Generate Now!</strong><br>
<code>python run_examples.py</code><br>
<em>Option 3</em>
</td>
<td>
<strong>Celebrity + Alternative Style</strong><br>
Professional photo with alternative garment - perfect for formal wear demonstration
</td>
</tr>
</table>

