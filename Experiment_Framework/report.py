import os
import sys
from pathlib import Path



import Experiment_Framework.funcion.report_manager as rm
import Experiment_Framework.funcion.file_manager as fm
import Experiment_Framework.funcion.tests.pythone_tests as py_tests

Evaluation_folder = str(fm.PROJECT_ROOT.parent / "Evaluations")
     
def os_task_folder(folder_os_task, tests_data):
    #print(f"OS Task Folder: {folder_os_task}")
    #print(f"Tests Data: {tests_data}")
    if not folder_os_task.exists():
        print(f"Folder not found: {folder_os_task}")
        return False
    if not tests_data:
        print(f"No tests data provided for {folder_os_task}")
        return False

    zmena = False
    print("test OS")
    for folder_languare in fm.open_folder_return_folders(folder_os_task):
        print(f"\t{Path(folder_languare).name}")

        for folder_model in fm.open_folder_return_folders(folder_languare):
            print(f"\t\t{Path(folder_model).name}")

            report_files = rm.get_report(folder_model)

            if rm.count_report_rows(report_files) == fm.get_count_code_files(folder_model):
                print(f"\t\t   -Skipping folder, as report is complete.")
                continue

            zmena = True

            match Path(folder_languare).name:
                case "Python":
                    py_tests.run_all_tests(folder_model, tests_data)
                case _:
                    print(f"Unsupported language folder: {folder_languare}")
                    continue

        #return zmena#XXX
        if zmena or rm.get_report(folder_languare) is None:
            zmena = True
            rm.delete_all_reports(folder_languare)
            for folder_model in fm.open_folder_return_folders(folder_languare):
                report_languare_name = Path(folder_languare).name +"_report.csv"
                report_languare_path = Path(folder_languare) / report_languare_name
                row = [Path(folder_model).name] + rm.get_average_report(rm.get_report(folder_model))
                #print(row)
                rm.write_report_B(report_languare_path, row)
            rm.print_report(rm.get_report(folder_languare))

        if rm.get_report(folder_os_task) is None or zmena:
            zmena = True
            rm.create_avg_report_from_chyldren_folders(folder_os_task)

        return zmena



def main(zmena):
    for folder_os in fm.open_folder_return_folders(os.path.join(Evaluation_folder, "Results")):
        print(Path(folder_os).name)
        zmenav_os = False
        for folder_task in fm.open_folder_return_folders(os.path.join(Evaluation_folder, "Prompts")):
            print("  " + Path(folder_task).name)

            file_path = Path(folder_task) / "tests_data.txt"
                    
            if not file_path.is_file():
                print(f"\033[93m'tests_data.txt' not found in {folder_task}\033[0m")
                continue
            tests_data = fm.load_setup(os.path.join(folder_task, "tests_data.txt"))

            #print(tests_data)
            if not tests_data:
                print(f"\033[93mNo tests data found in {folder_task}\033[0m")
                continue

            if not (Path(folder_os) / Path(folder_task).name).exists():
                print(f"\033[93mFolder not found: {Path(folder_os) / Path(folder_task).name}\033[0m")
                continue

            print("test")
            zmenav_os = zmenav_os or os_task_folder(Path(folder_os) / Path(folder_task).name,tests_data)
            print(f"Changes detected: {zmenav_os}")
            #break#XXX


            if zmenav_os:
                main(zmenav_os)
                return

        if zmenav_os or rm.get_report(folder_os) is None:
            rm.create_avg_report_from_chyldren_folders(folder_os)

        #break#XXX
    if zmenav_os or rm.get_report(os.path.join(Evaluation_folder, "Results")) is None:
        rm.create_avg_report_from_chyldren_folders(os.path.join(Evaluation_folder, "Results"))



if __name__ == "__main__":
    main(False)