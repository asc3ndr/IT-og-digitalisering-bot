from json import dump, load
from os import system
from pathlib import Path


class Custom:
    @staticmethod
    def read_JSON(file_name: str):
        """ Returns a dictionary representation of the JSON file """
        with open(f"{Path(__file__).resolve().parent}/{file_name}", "r") as file:
            return load(file)

    @staticmethod
    def write_JSON(file_name: str, obj: dict):
        """ Takes a dictionary and converts it to JSON, then overwrite the file in path """
        with open(f"{Path(__file__).resolve().parent}/{file_name}", "w") as file:
            dump(obj, file)
