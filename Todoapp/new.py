import pytesseract
from PIL import Image

# Ensure pytesseract knows the path to tesseract executable
# On Ubuntu, it's usually installed globally and accessible without specifying the path

# Load an image
image_path = '/home/ubuntu/Pictures/a.png'
image = Image.open(image_path)

# Optional: preprocess the image for better OCR results
# image = image.convert('L')  # Convert to grayscale, etc.

# Extract text
text = pytesseract.image_to_string(image, lang='fas')

print(text)
