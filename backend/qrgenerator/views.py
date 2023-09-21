import io
import qrcode
from django.http import FileResponse
from PIL import Image

def generate_qr(request):
    # Define a function named generate_qr that takes a request from $data.
    data = request.GET.get('data', 'https://example.com')

    # Create a qrcode.QRCode object
    qr = qrcode.QRCode(
        version=1,    # Version 1 (indicates the smallest size of the QR code)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level is ERROR_CORRECT_L (indicating low error correction level, about 7% error correction capability)
        box_size=10,  # Each square has a pixel size of 10
        border=4,  # The border width is 4
    )

    # Add data to the QR code object and call the make method to generate the QR code.
    qr.add_data(data)
    qr.make(fit=True)  # Automatic resizing of QR codes based on the data provided

    # Converting QR code objects to images
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converting PIL image objects to byte streams
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return FileResponse(buffer, content_type='image/png')
