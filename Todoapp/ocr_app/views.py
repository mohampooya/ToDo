from django.shortcuts import render
from .forms import ImageUploadForm
import pytesseract
from PIL import Image
from django.core.files.storage import default_storage

def ocr_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            # Save the uploaded image to a temporary file
            file_name = default_storage.save(image.name, image)
            file_path = default_storage.path(file_name)
            
            # Perform OCR on the image
            pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust based on your Tesseract path
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img, lang='fas')
            
            # Clean up the temporary file
            default_storage.delete(file_name)
            
            return render(request, 'ocr_app/ocr_result.html', {'text': text})
    else:
        form = ImageUploadForm()
    return render(request, 'ocr_app/upload_form.html', {'form': form})
