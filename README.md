# Translation of PDF Documents

## Installation
To install the tool, you need to have Python installed on your system. You can download Python from the official website [here](https://www.python.org/downloads/). Once you have installed Python, you can install the tool by running the following command in your terminal:

### Step 1: Install the tool

```bash
pip install .
```

This will install the tool and all its dependencies on your system.

### Step 2: Download the translation models

```bash
spacy download en_core_web_sm
```

## Usage
To use the tool, you need to have a PDF document that you want to translate. You can then run the following command in your terminal:

```bash
translate_pdf $input_path [--output_path $output_path] [--model $model]
```

Where:
- `$input_path` is the path to the input PDF document you want to translate.
- `$output_path` is the path to the output PDF document where the translated text will be saved. If not specified, the translated text will be printed to the console.
- `$model` is the translation model you want to use. default is `google`. The available models are:
  - `google`: Google Translate
  - `deepl`: DeepL Translator

For example, to translate a PDF document using the Google Translate model, you can run the following command:
    
```bash
translate_pdf input.pdf -o output.pdf -m google
```

#

## Acknowledgments

This project is a modification of [Index_PDF_Translation](https://github.com/Mega-Gorilla/Index_PDF_Translation), which is licensed under the BSD-3-Clause License. The original code has been modified and extended for the specific purposes of this project.
