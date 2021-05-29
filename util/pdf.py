import os
from PIL import Image


class PdfUtils():
    @staticmethod
    def convert_folder_to_pdf(folder_path: str) -> str:
        files_list = None
        for root, _, files in os.walk(folder_path):
            files_list = [os.path.join(root, name) for name in files]
            files_list.sort()

        image_list = [Image.open(im).convert('RGB') for im in files_list]

        if folder_path.endswith('/'):
            pdf_path = folder_path[:-1]
        else:
            pdf_path = folder_path
        pdf_path = f'{pdf_path}.pdf'

        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
