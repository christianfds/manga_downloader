import os

from PyPDF2 import PdfFileWriter

class PdfUtils():
    def __init__(self) -> None:
        pass

    def convert_folder_to_pdf(folder_path: str) -> str:
        for root, dirs, files in os.walk(folder_path):