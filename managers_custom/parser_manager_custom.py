import os.path
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from utils_custom.utils import check_directory_exists_create


class ParserManager:  # DM
    def __init__(self, url, filename, headers=None, file_exists_check=False):
        self.url: str = url
        self.headers: dict = headers
        self.filename: str = filename

        if file_exists_check and os.path.exists(filename):
            self.__enter__()
            print("\n\tLocal HTML file already exists\n")
            return

        check_directory_exists_create(self.filename)

        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.raise_for_status()

        except (RequestException, Exception) as error:
            print(f"\n\tRequest Exception: {error}")

        else:
            print(f"\n\tResponse status code: "
                  f"{response.status_code} - {response.reason}")

            try:
                with open(self.filename, 'w', encoding="utf-8") as local_file:
                    local_file.write(response.text)
                    print("\n\tLocal HTML file was created\n")

            except (IOError, Exception) as error:
                print(f"File error exception: {error}")


    def __enter__(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as local_file:
                self.local_file = local_file
                self.parsed_html = BeautifulSoup(local_file, "lxml")
                return self.parsed_html

        except (IOError,FileNotFoundError,Exception) as error:
            print(f"File error exception: {error}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.local_file:
            self.local_file.close()
