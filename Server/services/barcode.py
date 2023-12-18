"""Python barcode generator (usage)"""

from barcode import Code128
from barcode.writer import ImageWriter
from barcode.errors import BarcodeError

import cv2
from pyzbar import pyzbar


class BarcodeService:

    def __init__(self):
        pass

    @staticmethod
    def scan(img_path):

        try:
            if img_path is not None:
                image = cv2.imread(img_path)
                barcodes = pyzbar.decode(image)
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    print("Barcode Data:", barcode_data)
                    return barcode_data
            else:
                print('Error: No image file')
                return
        except BarcodeError as err:
            print(f'Error decoding: {err}')
            return None

    @staticmethod
    def generate(code):
        try:
            print(code)
            result_image = Code128(code, writer=ImageWriter(format='png'))
            result_image.save('result', options={"module_width": 0.4, "module_height": 20})
        except Exception as e:
            print(f'Error encoding: {e}')
