import sys
from pathlib import Path
import deepl
from colorama import init, Fore, Style

init()  # initialize colorama

# color constants
COLOR_SUCCESS = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_RESET = Style.RESET_ALL


class DeepLAuth:
    """Manages authentication and storage of DeepL API keys."""

    def __init__(self):
        self.home_dir = Path.home()
        self.api_key_path = self.home_dir / ".cache" / "translate_pdf" / "deepl_api_key"
        # create the directory if it doesn't exist
        self.api_key_path.parent.mkdir(parents=True, exist_ok=True)

    def get_api_key(self):
        """Returns a valid API key, prompting the user to enter it if necessary."""
        if not self.check_api_key():
            self.login()

        # read the API key from the file
        with open(self.api_key_path, "r") as file:
            api_key = file.read().strip()
        return api_key

    def check_api_key(self):
        """Checks if a valid API key is stored and tests it."""
        if not self.api_key_path.exists():
            return False

        with open(self.api_key_path, "r") as file:
            api_key = file.read().strip()
        return self._test_api_key(api_key)

    def _test_api_key(self, api_key):
        """Tests the loaded API key by attempting a basic DeepL interaction."""
        try:
            translator = deepl.Translator(api_key)
            result = translator.translate_text("Hello", target_lang="ja")
            return True
        except deepl.exceptions.AuthorizationException:
            print(COLOR_ERROR + "Authentication Error: API key is invalid or usage limit reached." + COLOR_RESET)
            return False
        except Exception as e:
            print(COLOR_ERROR + f"Error occurred while testing API key: {e}" + COLOR_RESET)
            return False

    def login(self):
        """Prompts the user to enter their API key and saves it."""
        for attempt in range(1, 4):
            api_key = input(f"Enter your DeepL API key (Attempt {attempt}/3): ")

            if self._test_api_key(api_key):
                with open(self.api_key_path, "w") as file:
                    file.write(api_key)
                print(
                    COLOR_SUCCESS
                    + f"API key saved successfully to: {self.api_key_path}"  # Display file path
                    + COLOR_RESET
                )
                return

        print(COLOR_ERROR + "Failed to save API key. Please check if the entered key is correct." + COLOR_RESET)
        sys.exit(1)
