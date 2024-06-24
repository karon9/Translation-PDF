import argparse, os, asyncio, time, sys
from pathlib import Path


from translate_pdf.modules.translate import pdf_translate, PDF_block_check, write_logo_data
import tkinter as tk
from tkinter import filedialog
from translate_pdf.config import *
from translate_pdf.modules.translate_pdf import translate_local


def parse_args():
    """
    Parse command line arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="input file path")
    parser.add_argument("-o", "--output_path", default=None, type=str, help="output file path")
    parser.add_argument(
        "-m",
        "--model",
        default="google",
        choices=["google", "deepl"],
        type=str,
        help="model to use for translation",
    )

    return parser.parse_args()


def main():
    # argparse
    args = parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        translate_local(
            input_path=args.input_path,
            output_path=args.output_path,
            model=args.model,
        )
    )
