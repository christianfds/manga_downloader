import multiprocessing
import os
import shutil

import tqdm
from PIL import Image


class PdfUtils:
    @staticmethod
    def convert_folder_to_pdf(folder_path: str, keep_original: bool = False) -> str:
        """
        Static Method to convert the pdf's.
        Args:
            folder_path (string): specify the folder path.
        Args:
            keep_original (bool): -> specify True to save the original files (default: False).
        """
        files_list = None
        for root, _, files in os.walk(folder_path):
            files_list = [os.path.join(root, name) for name in files]
            files_list.sort()

        image_list = [Image.open(im).convert("RGB") for im in files_list]

        if folder_path.endswith("/"):
            pdf_path = folder_path[:-1]
        else:
            pdf_path = folder_path
        pdf_path = f"{pdf_path}.pdf"

        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])

        if not keep_original:
            shutil.rmtree(folder_path)

        return pdf_path

    @staticmethod
    def _multiproc_intermediary_to_convert_folder_to_pdf(args: tuple[str, bool]) -> str:
        """
        Static method to initiate the pdf converts.
        Args:
            args tuple[str, bool]: default arguments.
        """
        return PdfUtils.convert_folder_to_pdf(args[0], args[1])

    @staticmethod
    def convert_multiple_folders_to_pdf(folder_paths: list[str], keep_original: bool = False) -> list[str]:
        """
        Static method to initiate the multiple converts of pdf's.
        Args:
            folder_paths (string): specify the folder path.
        Args:
            keep_original (bool): -> specify True to save the original files (default: False).
        """
        print("Converting to PDF")
        with multiprocessing.Pool() as pool:
            inputs = list(zip(folder_paths, [keep_original] * len(folder_paths)))
            results = list(
                tqdm.tqdm(
                    pool.imap(
                        PdfUtils._multiproc_intermediary_to_convert_folder_to_pdf,
                        inputs,
                    ),
                    total=len(inputs),
                    unit="Pdf",
                )
            )

        return results
