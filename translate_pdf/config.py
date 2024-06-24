import os
from dotenv import load_dotenv

# 環境変数を.envファイルから読み込む
load_dotenv()

# config.py
# ----- ローカル版 設定 ------
DeepL_API_Key = os.environ["DeepL_API_Key"]  # DeepLのAPIキーを環境変数から取得
DeepL_URL = "https://api-free.deepl.com/v2/translate"  # DeepL Proの場合は、「https://api.deepl.com/v2/translate」を設定してください
Output_folder_path = ""

# ----- 以下 API用 設定 --------
# Black BlazeオブジェクトDB設定
# BLACK_BLAZE_CONFIG = {
#     'public_key_id': os.environ["blackblaze_public_id"],
#     'public_key' : os.environ["blackblaze_public_key"],
#     'private_key_id': os.environ["blackblaze_private_id"],
#     'private_key' : os.environ["blackblaze_private_key"],
#     'public_bucket' : 'pdf-public',
#     'private_bucket' : 'pdf-private'
# }

# 接続許可リスト
CORS_CONFIG = ["https://indqx-demo-front.onrender.com", "http://localhost:5173"]

# URLリスト
URL_LIST = {"papers_link": "https://indqx-demo-front.onrender.com/abs/"}

# 翻訳設定
TRANSLATION_CONFIG = {"ALLOWED_LANGUAGES": ["en", "ja"]}

# token 計算用
SPACY_CONFIG = {"supported_languages": {"en": "en_core_web_sm", "ja": "ja_core_news_sm"}}

# デバッグ用ファイル位置
Debug_folder_path = "./debug/"
bach_process_path = "./Test Bench/result/"
