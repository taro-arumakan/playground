from reportlab.lib import pagesizes
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

def get_qr_code(data):
    return qr.QrCodeWidget(data)

def generate_qr_codes(data):

    chunk = 2809    # 22496 / 8 - 20 / 8

    qr_codes = []
    while data:
        qr_codes.append(get_qr_code(data[:chunk]))
        data = data[chunk:]
    return qr_codes

def write_to_pdf(qr_codes, output_file):
    c = canvas.Canvas(output_file, pagesize=pagesizes.A4)
    c.setFont('Helvetica', 8)

    height_title = 8
    height_qr = 200
    height_block = height_title + height_qr

    width_page, height_page = pagesizes.A4
    y_position = height_page - height_title
    second_col_x = width_page / 2
    first_col_x = 30

    for i, qr_code in enumerate(qr_codes):
        if y_position < height_block:
            print(f'adding a page: {y_position} {height_block}')
            c.showPage()        # add a page
            c.setFont('Helvetica', 8)
            y_position = height_page - height_title

        s = f'{i} QR Code chunk'
        print(f'drawing {s}')
        x_position = first_col_x if not i % 2 else second_col_x
        c.drawString(x_position, y_position, s)

        # Set the size of the QR code drawing
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        d = Drawing(200, 200, transform=[200/width, 0, 0, 200/height, 0, 0])
        d.add(qr_code)

        # Draw the QR code on the PDF canvas
        renderPDF.draw(d, c, x_position, y_position - height_qr)

        if i % 2:
            y_position -= height_block

    c.save()


import base64
with open(r'C:\working\sample.zip', 'rb') as f:
    data = base64.b64encode(f.read()).decode('utf-8')
qrs = generate_qr_codes(data)
write_to_pdf(qrs, r'C:\working\sample_qr.pdf')

