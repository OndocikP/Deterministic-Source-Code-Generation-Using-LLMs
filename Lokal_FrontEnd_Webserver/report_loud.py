


import os
from pathlib import Path
import json
import csv
import glob

from Experiment_Framework.funcion.file_manager import open_folder_return_folders


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
TASKS_DIR = PROJECT_ROOT / 'Code_Generation_Tasks'


def get_json():
    json_report = {}
    #print(TASKS_DIR)
    for test_file in open_folder_return_folders(TASKS_DIR):
        #print(test_file)
        folder_name = os.path.basename(test_file)
        json_report[folder_name] = {}
        #test ci test_file obsahuje file ".dashboard.json"
        if os.path.exists(os.path.join(test_file, ".dashboard.json")):
            with open(os.path.join(test_file, ".dashboard.json"), "r", encoding="utf-8") as f:
                json_report[folder_name] = json.load(f)

        for language_folder in open_folder_return_folders(test_file):
            language_name = os.path.basename(language_folder)
            json_report[folder_name][language_name] = {}
            csv_files = glob.glob(os.path.join(language_folder, "*.csv"))
            for csv_file in csv_files:
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)

                    for row in reader:
                        file_name = row["File_name"]

                        json_report[folder_name][language_name][file_name] = {
                            "Code_Identity": float(row["Code_Identity"]),
                            "AST_Structure": float(row["AST_Structure"]),
                            "Behavioral_Equivalence": float(row["Behavioral_Equivalence"])
                        }

            for model in open_folder_return_folders(language_folder):
                model_name = os.path.basename(model)
                #json_report[folder_name][language_name][model_name] = {}
                if os.path.exists(os.path.join(model, "report.csv")):
                    with open(os.path.join(model, "report.csv"), "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            file_name = row["File_name"]
                            if file_name not in json_report[folder_name][language_name]:
                                json_report[folder_name][language_name][model_name][file_name] = {}
                            json_report[folder_name][language_name][model_name][file_name]["report"] = {
                                "Code_Identity": float(row["Code_Identity"]),
                                "AST_Structure": float(row["AST_Structure"]),
                                "Behavioral_Equivalence": float(row["Behavioral_Equivalence"])
                            }

            

    return json_report


print(json.dumps(get_json(), indent=4, ensure_ascii=False))