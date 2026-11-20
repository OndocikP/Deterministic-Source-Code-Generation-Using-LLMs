import os
import sys
from pathlib import Path
import Experiment_Framework.report as report


path = "D:\\GitHub\\Tuke\\Deterministic-Source-Code-Generation-Using-LLMs\\Evaluations\\Results\\Linux\\absolute_value"


def main():
    print("test")
    folder = Path(".")
    print(folder)
    folder_gild = report.fm.open_folder_return_folders(path)
    print(folder_gild)
    report.generate_report_from_avr_chyldren_folder(path)

    



if __name__ == "__main__":
    main()