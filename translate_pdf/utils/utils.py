import os
import json

async def pdf_block_bach():
    """
    Batch process all PDF files in the directory
    """

    original_directory = os.getcwd()
    directory = ".\Test Bench\\raw"
    import glob

    os.chdir(directory)

    pdf_files = glob.glob("**/*.pdf", recursive=True)

    pdf_files = [os.path.join(directory, file) for file in pdf_files]
    pdf_files = glob.glob("**/*.pdf", recursive=True)

    os.chdir(original_directory)

    for file_path in pdf_files:
        file_path = directory + "\\" + file_path
        with open(file_path, "rb") as f:
            input_pdf_data = f.read()
        print(f"Loaded: {file_path}")

        result_pdf = await PDF_block_check(input_pdf_data)
        result_pdf = await write_logo_data(result_pdf)

        if result_pdf is None:
            continue
        _, file_name = os.path.split(file_path)
        output_path = bach_process_path + "Blocks_" + file_name

        with open(output_path, "wb") as f:
            f.write(result_pdf)
        print(f"Saved: {output_path}")


def load_json_to_list(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise Exception(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise Exception(f"Error decoding JSON file")
    except Exception as e:
        raise e
