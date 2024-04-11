import os
from fake_headers import Headers
import json
import csv
import re

def create_dir_if_not_exists(full_filename: str) -> None:
    """
    Check whether a directory exists and creates it if not
    :param full_filename: string containing the full path and local_full_filename
    :return: None
    """
    directory_name = os.path.dirname(full_filename)
    try:
        os.makedirs(directory_name, exist_ok=True)
    except (IOError, Exception) as error:
            print(f"Error occurred: {error}")


def create_real_headers(access: str, user_agent: str) -> dict|None:
    """
    :param access: string containing the real access
    :param user_agent: string containing the real user agent
    :return: dict|None containing the real headers or None if "" value(s)
    """
    if access and user_agent:
        real_headers = {"access": access, "user-agent": user_agent}
        return real_headers
    return None


def create_fake_headers() -> dict:
    """
    Create a fake headers using fake_headers library
    :return: dict
    """
    fake_headers = Headers().generate()
    return fake_headers


def compose_full_filename(directories_paths: tuple | str,
                          file_name: str) -> str|None:
    """
    Create a fullpath local_full_filename
    :param directories_paths: str containing one directory
    or tuple containing directories
    :param file_name: str containing the local_full_filename with extension
    :return: str containing the fullpath local_full_filename with extension
    """
    if file_name:
        if isinstance(directories_paths, tuple):
            return os.path.join(*directories_paths, file_name)

        if isinstance(directories_paths, str):
            return os.path.join(directories_paths, file_name)
    return None


def create_json_file(json_full_filename: str, data_dictionary: dict|list,
                     file_rewrite: bool = False) -> None:
    """
    Create JSON file from data_dicts_list. If file_rewrite is True,
    the file will allways be rewritten when creating. Otherwise, it will
    be passing creating a new json file
    :param json_full_filename: str: Full initial_name of the json file
    :param data_dictionary: dict: Data dictionary to be saved into json file
    :param file_rewrite: bool: Rewrite existing json or not
    :return: None
    """

    if not file_rewrite and os.path.exists(json_full_filename):
        print(f"\n\tExisting JSON file '{json_full_filename}' used")
        return

    create_dir_if_not_exists(json_full_filename)

    try:
        with open(json_full_filename, "w", encoding="utf-8") as json_file:

            try:
                json.dump(data_dictionary, json_file, ensure_ascii=False, indent=4)
                print(f"\n\tJSON file '{json_full_filename}' created")
            except (json.JSONDecodeError, Exception) as json_error:
                print(f"JSON dump error: {json_error}")

    except (IOError, FileExistsError, Exception) as file_error:
        print(f"File write error: {file_error}")


def create_csv_file(csv_full_filename: str, csv_headers: list,
                    data_dicts_list: list, file_rewrite: bool = False) -> None:
    """
    Create CSV file from data_list. If file_rewrite is True,
    the file will allways be rewritten when creating. Otherwise, it will
    be passing creating a new csv file
    :param csv_full_filename: str: Full initial_name of the csv file
    :param csv_headers: list: List of the columns(fields) names to be included in the csv file
    :param data_dicts_list: list: Data with dictionaries list to be saved into csv file
    :param file_rewrite: bool: Rewrite existing csv file or not
    :return: None
    """

    if not file_rewrite and os.path.exists(csv_full_filename):
        print(f"\n\tExisting CSV file '{csv_full_filename}' used")
        return

    create_dir_if_not_exists(csv_full_filename)

    try:
        with open(csv_full_filename, "w", encoding="utf-8", newline="") as csv_file:

            try:
                writer = csv.DictWriter(csv_file,
                                        fieldnames=csv_headers,
                                        dialect="excel",
                                        # restval="",  # if has no value in dictionary
                                        extrasaction="ignore"  # if dictionary key not not found field names
                                        )
                writer.writeheader()
                writer.writerows(data_dicts_list)

                print(f"\n\tCSV file '{csv_full_filename}' created")
            except (csv.Error, Exception) as csv_error:
                print(f"CSV write error: {csv_error}")

    except (IOError, FileExistsError, Exception) as file_error:
        print(f"File write error: {file_error}")


def read_json_file(json_full_filename: str) -> dict:
    """
    Reads the json file specified by csv_full_filename
    :param json_full_filename: str: Full initial_name of the json
    :return: dict: Data dictionary to be red from the json file
    """
    try:
        with open(json_full_filename, "r", encoding="utf-8") as json_file:

            try:
                json_data = json.load(json_file)
                return json_data
            except (json.JSONDecodeError, Exception) as json_error:
                print(f"JSON load error: {json_error}")

    except (IOError, FileNotFoundError, Exception) as file_error:
        print(f"File opening error: {file_error}")


def make_slashed_name(initial_name: str):
    initial_name = initial_name.strip()
    substitutable_symbols = (", ", "' ", "- ", "\\. ", ",", "'", "-", "\\.", " ", "__", "___")
    substitutable_re_string = "|".join(substitutable_symbols)
    slashed_name = re.sub(substitutable_re_string, "_", initial_name)
    # for symbol in substitutable_symbols:
    #     if symbol in initial_name:
    #         initial_name = initial_name.replace(symbol, "_")
    #         print(initial_name)
    return slashed_name
