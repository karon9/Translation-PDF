import argparse, os, asyncio, time
from pathlib import Path
from translate_pdf.modules.translate import pdf_translate, PDF_block_check, write_logo_data
import tkinter as tk
from tkinter import filedialog
from translate_pdf.config import *


async def translate_local(
    input_path: str, output_path: str = None, model: str = "google", disble_translate: bool = False
):
    """
    Translate PDF file
    """

    # set input path
    input_path = Path(input_path)

    if not input_path.exists():
        raise Exception("Input file not found")

    with open(str(input_path), "rb") as f:
        input_pdf_data = f.read()

    # translate pdf
    result_pdf = await pdf_translate(
        input_pdf_data, model=model, debug=False, disable_translate=disble_translate
    )

    if result_pdf is None:
        raise Exception("PDF translation failed")

    # set output path
    if output_path is None:
        output_path = Path.cwd() / f"translated_{input_path.name}"
    else:
        output_path = Path(output_path)

    with open(str(output_path), "wb") as f:
        f.write(result_pdf)
