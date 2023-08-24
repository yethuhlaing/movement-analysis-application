from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.lib import utils
from reportlab.pdfgen import canvas

def capture_frame_page(frame, page_height, page_number):
    x = frame.winfo_rootx()
    y = frame.winfo_rooty() + page_height * (page_number - 1)
    width = frame.winfo_width()
    height = page_height
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return image

def images_to_pdf(images, output_path):
    c = canvas.Canvas(output_path, pagesize=images[0].size)
    for image in images:
        c.drawImage(image, 0, 0, width=image.width, height=image.height)
        c.showPage()
    c.save()