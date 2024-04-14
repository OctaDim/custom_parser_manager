import os.path
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
from random import randrange
from time import sleep


class ParserManager:  # DM
    def __init__(self, url: str,
                 local_full_filename: str,
                 headers: dict = None,
                 params: dict = None,
                 cookies: dict = None,
                 data: dict = None,
                 file_rewrite: bool = False,
                 not_200_create_local_file=True,
                 random_time_delay: int = -1,
                 get_or_post: str = "get",
                 ):

        self.url = url
        self.headers = headers
        self.local_full_filename = local_full_filename
        self.file_rewrite = file_rewrite
        self.not_200_create_local_file = not_200_create_local_file
        self.response = None
        self.status_code = None
        self.parsed_source = None
        self.random_time_delay = random_time_delay
        self.get_or_post = get_or_post
        self.params = params
        self.cookies = cookies
        self.data = data


    def get_response_and_status_code(self):
        try:
            if self.get_or_post == "get":
                self.response = requests.get(url=self.url,
                                             headers=self.headers,
                                             cookies=self.cookies,
                                             params=self.params,
                                             data=self.data
                                             )
            elif self.get_or_post == "post":
                self.response = requests.post(url=self.url,
                                              headers=self.headers,
                                              cookies=self.cookies,
                                              params=self.params,
                                              data=self.data
                                              )
            else:
                print(f"Error. Parameter 'get_or_post' value "
                      f"('{self.get_or_post}') is not equal 'get' or 'post'")

            self.status_code = self.response.status_code
            print(f"\n\tResponse status code: "
                  f"{self.status_code} - {self.response.reason}")

        except (RequestException, HTTPError, URLError,
                Exception) as request_error:
            print(f"Request error: {request_error}")


    def check_dir_exists_create(self):
        directory_name = os.path.dirname(self.local_full_filename)
        try:
            os.makedirs(directory_name, exist_ok=True)
        except (IOError, Exception) as error:
            print(f"Error occurred: {error}")


    def create_local_html_xml_file(self):
        try:
            with open(self.local_full_filename, "w",
                      encoding="utf-8") as local_file:

                local_file.write(self.response.text)
                print(f"\tLocal HTML(XML) file "
                      f"'{self.local_full_filename}' created")

        except (IOError, FileExistsError, Exception) as file_error:
            print(f"File writing error: {file_error}")


    def get_parsed_source_from_local_file(self):
        try:
            with open(self.local_full_filename, "r",
                      encoding="utf-8") as local_file:

                try:
                    self.parsed_source = BeautifulSoup(local_file,"lxml")
                except (HTTPError, URLError, Exception) as parsing_error:
                    print(f"Local file parsing error: {parsing_error}")

        except (IOError, FileNotFoundError, Exception) as file_error:
            print(f"File opening error: {file_error}")


    def get_parsed_source_from_response(self):
        try:
            self.parsed_source = BeautifulSoup(self.response.text,"lxml")
        except (HTTPError, URLError, Exception) as parsing_error:
                print(f"Response data parsing error: {parsing_error}")

        self.make_random_time_delay()


    def make_random_time_delay(self):
        """
        Make random time-delay in the range of (1 - random_time_delay)
        seconds if random_time_delay parameter > 0. Default value = -1
        :return: None
        """
        if self.random_time_delay > 0:
            sleep(randrange(1,self.random_time_delay))


    def __enter__(self):
        if not self.file_rewrite and os.path.exists(self.local_full_filename):
            print(f"\n\tLocal HTML(XML) file '{self.local_full_filename}' used")
            self.get_parsed_source_from_local_file()
            print()
            return self.parsed_source

        self.get_response_and_status_code()
        if (self.status_code == 200
                or self.not_200_create_local_file):
            self.check_dir_exists_create()
            self.create_local_html_xml_file()
            self.get_parsed_source_from_response()
            # self.get_parsed_source_from_local_file()
            print()
            return self.parsed_source

        print()
        return self.parsed_source


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
