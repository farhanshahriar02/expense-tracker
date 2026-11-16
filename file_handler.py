"""
file_handler.py
Handles JSON file save/load with exception handling.
"""
import json
import os

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, records: list):
        try:
            directory = os.path.dirname(self.file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4, ensure_ascii=False)
            return True, "Data saved successfully."
        except OSError as error:
            return False, f"File save error: {error}"

    def load(self):
        try:
            if not os.path.exists(self.file_path):
                return [], "No data file found. Starting with empty data."
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                return [], "Data file format is invalid."
            return data, "Data loaded successfully."
        except json.JSONDecodeError:
            return [], "Data file is corrupted."
        except OSError as error:
            return [], f"File load error: {error}"