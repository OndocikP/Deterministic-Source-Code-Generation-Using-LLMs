import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import Experiment_Framework.funcion.file_manager as fm
from Experiment_Framework.funcion.tests.pythone_code_tests import test__folders

CODE_GENERATION_TASKS = str(PROJECT_ROOT / "Code_Generation_Tasks")


def main():
    print("Zacinam prechadzat testovaciu zlozk:")
    for folder in fm.open_folder_return_folders(CODE_GENERATION_TASKS):
        if not test__folders(folder):
            print(f"\033[91mTest failed for folder: {folder}\033[0m")
        else:
            print(f"\033[92mTest passed for folder: {folder}\033[0m")


if __name__ == "__main__":
    main()