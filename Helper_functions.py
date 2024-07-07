import shutil
import subprocess
import os
import json
import pytz
import random
from datetime import datetime
from PIL import Image


def execute_terminal_command(command: str):
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        output = str(output.decode("utf-8"))
        print(rf"Command executed successfully: {command}")
        return output
    except Exception as e:
        return None, str(e)


def correct_path(path: str):
    return path[1:] if path.startswith("\\") else path


def write_file(data_list: list, file_path: str, file_name: str = ""):
    if len(file_name) > 0:
        file_path = rf"{file_path}\{file_name}"

    # Writing JSON data
    with open(file_path, "w") as file:
        json.dump(data_list, file)


def read_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def copy_file(source_path: str, destination_path: str):
    try:
        shutil.copyfile(source_path, destination_path)
    except Exception as e:
        print(rf"Failed to copy {source_path} to {destination_path}")
        raise e


def read_image(image_path: str):
    try:
        image = Image.open(image_path)
        return image
    except IOError:
        print("Unable to load image")
        return None


def get_current_time():
    # Get the current datetime in UTC timezone
    current_datetime_utc = datetime.now(pytz.utc)
    # Convert UTC datetime to Egypt timezone
    egypt_timezone = pytz.timezone("Africa/Cairo")
    current_datetime_local = current_datetime_utc.astimezone(egypt_timezone)

    return str(current_datetime_local.strftime("%Y-%m-%d %H:%M:%S %Z"))


def get_random_str(sz: int):
    result: str = ""
    while len(result) < sz:
        result += str(random.randint(0, 9))

    return result


def create_folder(path: str, Replace_if_exist = True):
    try:
        if Replace_if_exist and os.path.exists(path):
            shutil.rmtree(path)

        os.makedirs(path, exist_ok=False)
        print(f"Folder '{path}' created successfully.")
    except Exception as e:
        print(f"Failed to create folder '{path}'. Error: {e}")