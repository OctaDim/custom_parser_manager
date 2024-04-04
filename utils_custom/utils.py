import os


def check_directory_exists_create(full_filename):  # DM
    directory_name = os.path.dirname(full_filename)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
