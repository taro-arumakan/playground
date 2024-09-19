import base64
from PIL import Image       # pip install pillow
from pyzbar.pyzbar import decode

"""
if zbar shared library not found after brew install,
$ mkdir ~/lib
$ ln -s $(brew --prefix zbar)/lib/libzbar.dylib ~/lib/libzbar.dylib
"""

def write_to_file(data_list, output_file):
    data = b''.join(d.data for d in data_list)
    with open(output_file, 'wb') as f:
        f.write(base64.b64decode(data))

data_list = decode(Image.open('zipped.png'))
write_to_file(data_list, 'test.zip')
