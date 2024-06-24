import asyncio
import deepl
import googletrans
from tqdm import tqdm
from translate_pdf.config import *
from translate_pdf.modules.pdf_edit import *
from translate_pdf.modules.deepl_auth import DeepLAuth


async def translate_str_data(text: str, model: str, target_lang: str, api_url: str) -> str:
    """
    An asynchronous function that translates the input text to the specified language using the DeepL API.
    Note that tag handling is set to XML.

    Args:
        text (str): The text to be translated.
        target_lang (str): The language code of the translation target (e.g., "EN", "JA", "FR", etc.).

    Returns:
        str: The translated text.

    Raises:
        Exception: If the API request fails.
    """

    translated_text = ""
    if model == "google":
        translator = googletrans.Translator()
        print("Start Google Translate")
        for t in tqdm(text.split("\n")):
            if t == "":
                translated_text += "\n"
            else:
                try:
                    result = translator.translate(t, src="en", dest=target_lang)
                    # concatnate translated text
                    translated_text += result.text + "\n"
                except Exception as e:
                    raise Exception(f"Google API request failed: {e}")
    elif model == "deepl":
        print("Start DeepL Translate")

        # Get the DeepL API key
        deepl_auth = DeepLAuth()
        key = deepl_auth.get_api_key()
        translator = deepl.Translator(key)

        # Send a request to the DeepL API
        try:
            result = translator.translate_text(text, target_lang=target_lang, tag_handling="xml", formality="more")
            translated_text = result.text
        except Exception as e:
            raise Exception(f"DeepL API request failed: {e}")
    else:
        raise Exception("Model is not defined")

    return translated_text


async def translate_blocks(blocks, model: str, target_lang: str, api_url: str):
    # テキスト検出
    translate_text = ""
    for page in blocks:
        for block in page:
            translate_text += block["text"] + "\n"

    # 翻訳
    translated_text = await translate_str_data(
        text=translate_text, model=model, target_lang=target_lang, api_url=api_url
    )

    translated_text = translated_text.split("\n")

    # 翻訳後テキスト挿入
    for page in blocks:
        for block in page:
            block["text"] = translated_text.pop(0)

    return blocks


async def preprocess_translation_blocks(blocks, end_maker=(".", ":", ";"), end_maker_enable=True):
    """
    blockの文字列について、end makerがない場合、一括で翻訳できるように変換します。
    変換結果のblockを返します
    """
    results = []

    text = ""
    coordinates = []
    block_no = []
    page_no = []
    font_size = []

    for page in blocks:
        page_results = []
        temp_block_no = 0
        for block in page:
            text += " " + block["text"]
            page_no.append(block["page_no"])
            coordinates.append(block["coordinates"])
            block_no.append(block["block_no"])
            font_size.append(block["size"])

            if text.endswith(end_maker) or block["block_no"] - temp_block_no <= 1 or end_maker_enable == False:
                # マーカーがある場合格納
                page_results.append(
                    {
                        "page_no": page_no,
                        "block_no": block_no,
                        "coordinates": coordinates,
                        "text": text,
                        "size": font_size,
                    }
                )
                text = ""
                coordinates = []
                block_no = []
                page_no = []
                font_size = []
            temp_block_no = block["block_no"]

        results.append(page_results)
    return results


async def deepl_convert_xml_calc_cost(json_data):
    """
    翻訳コストを算出します。
    """
    cost = 0
    price_per_character = 0.0025  # 1文字あたりの料金(円)
    xml_output = ""
    for page in json_data:
        for block in page:
            text = block["text"]
            # 翻訳にて問題になる文字列を変換
            # text = text.replace('\n', '')

            xml_output += f"<div>{text}</div>\n"
    return xml_output, cost


async def pdf_translate(
    pdf_data,
    source_lang="en",
    to_lang="ja",
    api_url="https://api.deepl.com/v2/translate",
    model="google",
    debug=False,
    disable_translate=False,
):

    block_info = await extract_text_coordinates_dict(pdf_data)

    if debug:
        text_blocks, fig_blocks, remove_info, plot_images = await remove_blocks(
            block_info, 10, lang=source_lang, debug=True
        )
    else:
        text_blocks, fig_blocks, _, _ = await remove_blocks(block_info, 10, lang=source_lang)
    # 翻訳部分を消去したPDFデータを制作
    removed_textbox_pdf_data = await remove_textbox_for_pdf(pdf_data, text_blocks)
    removed_textbox_pdf_data = await remove_textbox_for_pdf(removed_textbox_pdf_data, fig_blocks)
    print("1.Generate removed_textbox_pdf_data")

    # 翻訳前のブロック準備
    preprocess_text_blocks = await preprocess_translation_blocks(text_blocks, (".", ":", ";"), True)
    preprocess_fig_blocks = await preprocess_translation_blocks(fig_blocks, (".", ":", ";"), False)
    print("2.Generate Prepress_blocks")

    # 翻訳実施
    if disable_translate is False:
        translate_text_blocks = await translate_blocks(
            preprocess_text_blocks, model=model, target_lang=to_lang, api_url=api_url
        )
        translate_fig_blocks = await translate_blocks(
            preprocess_fig_blocks, model=model, target_lang=to_lang, api_url=api_url
        )
        print("3.translated blocks")
        # pdf書き込みデータ作成
        write_text_blocks = await preprocess_write_blocks(translate_text_blocks, to_lang)
        write_fig_blocks = await preprocess_write_blocks(translate_fig_blocks, to_lang)
        print("4.Generate wirte Blocks")
        # pdfの作成
        if write_text_blocks != []:
            translated_pdf_data = await write_pdf_text(removed_textbox_pdf_data, write_text_blocks, to_lang)
        if write_fig_blocks != []:
            translated_pdf_data = await write_pdf_text(translated_pdf_data, write_fig_blocks, to_lang)
        translated_pdf_data = await write_logo_data(translated_pdf_data)
    else:
        print("99.Translate is False")

    # 見開き結合の実施
    marged_pdf_data = await create_viewing_pdf(pdf_data, translated_pdf_data)
    print("5.Generate PDF Data")
    return marged_pdf_data


async def PDF_block_check(pdf_data, source_lang="en"):
    """
    ブロックの枠を作画します
    """

    block_info = await extract_text_coordinates_dict(pdf_data)

    text_blocks, fig_blocks, leave_blocks = await remove_blocks(block_info, 10, lang=source_lang)

    text_block_pdf_data = await pdf_draw_blocks(
        pdf_data, text_blocks, width=0, fill_opacity=0.3, fill_colorRGB=[0, 0, 1]
    )
    fig_block_pdf_data = await pdf_draw_blocks(
        text_block_pdf_data, fig_blocks, width=0, fill_opacity=0.3, fill_colorRGB=[0, 1, 0]
    )
    all_block_pdf_data = await pdf_draw_blocks(
        fig_block_pdf_data, leave_blocks, width=0, fill_opacity=0.3, fill_colorRGB=[1, 0, 0]
    )

    return all_block_pdf_data
