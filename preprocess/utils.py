import os
from PIL import Image
import shutil
import json
import re

def is_valid_image(file_name):
    if not os.path.isfile(file_name):
        return False
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False


def get_all_files(dirpath):
    return sum(
        [
            [os.path.join(os_walks[0], f) for f in os_walks[2]]
            for os_walks in os.walk(dirpath)
        ],
        [],
    )


def copy(src_path, dst_path):
    os.makedirs(dst_path.parent, exist_ok=True)
    shutil.copyfile(src_path, dst_path)


def get_all_images(dirpath):
    return [p for p in get_all_files(dirpath) if is_valid_image(p)]


def load_json(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data


def find_path(imgs, img_id):
    for s in imgs:
        if img_id in s:
            return s
    return None


def convert_to_binary_mask(input, output):
    # Open the image
    image = Image.open(input).convert("L")  # Convert to grayscale

    # Apply a threshold to convert the image to binary (black and white)
    threshold = 1  # Since background is always black, any pixel > 0 is considered as white (mask)
    binary_image = image.point(lambda p: p > threshold and 255)

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output), exist_ok=True)

    # Save the binary mask
    binary_image.save(output)

    # print(f"Binary mask saved to {output}")


def remove_folders(folder_paths):
    """
    Removes a list of folders, including their contents.

    Parameters:
    folder_paths (list): List of paths to the folders to be removed.
    """
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                # print(f"Successfully removed: {folder_path}")
            except Exception as e:
                print(f"Error removing {folder_path}: {e}")
        else:
            print(f"Folder does not exist: {folder_path}")


def extract_and_remove_strings(strings, substr):
    mask_strings = [string for string in strings if substr in string]
    strings[:] = [string for string in strings if substr not in string]
    return strings, mask_strings


def convert_busi_filename(filename):
    # Split the filename into directory path, base filename, and extension
    directory, base_name = os.path.split(filename)
    base_name = base_name.replace("_mask", "").replace(" ", "")  # Remove '_mask' from base name
    number = re.search(r"\((\d+)\)", base_name).group(
        1
    )
    # Extract number between parentheses
    return f"{number}_{base_name.replace(f'({number})', '')}"
