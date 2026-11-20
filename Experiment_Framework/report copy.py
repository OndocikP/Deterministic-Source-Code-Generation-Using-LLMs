import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import Experiment_Framework.funcion.report_manager as rm
import Experiment_Framework.funcion.file_manager as fm
from Experiment_Framework.funcion.tests.pythone_tests import test_single_file

Evaluation_folder = str(PROJECT_ROOT / "Evaluations")


def get_Languare(folder_name):
    switcher = {
        "Python": "pythone_tests",
        "C++": "cpp_tests",
        "Java": "java_tests"
    }
    return switcher.get(folder_name, None)

def llm_folder(LLM_folder, test_data):  ## generuje report v {test}{language}{LLM}

    #print(f"LLM folder: {LLM_folder}")
    llm_name = Path(LLM_folder).name
    repotrt_name = f"report_{llm_name}.csv"
    report = rm.get_report(LLM_folder, repotrt_name)

            #print(rm.count_report_rows(report))
            #print(fm.get_count_code_files(LLM_folder))
    if report is not None and rm.count_report_rows(report) == fm.get_count_code_files(LLM_folder):
        #rm.print_report(report)
        #average_report = rm.get_average_report(report)
        #print(f"Average report for {repotrt_name}: {average_report}")
        return False
    else:
        print(f"LLM folder: {LLM_folder}")
        print(f"Report for {repotrt_name} is not up-to-date.")
        print(f"Report rows: {rm.count_report_rows(report)}, Code files: {fm.get_count_code_files(LLM_folder)}")
        print(report)

    rm.delete_all_reports(LLM_folder)
            ## If the number of rows in the report matches the number of code files, finish processing this LLM folder.

    code_files = fm.open_folder_return_files(LLM_folder)
    code_files = [f for f in code_files if not f.lower().endswith(".csv")]  # Filter out .csv files

            # Remove behavioral equivalence report file from LLM_folder

            # Collect behavioral equivalence details for all files
    behavioral_equivalence_details = [rm.BEHAVIORAL_EQUIVALENCE_HEADER[:]]  # Start with header

            #print(f"Code files: {code_files}")
    test_results = []
    for code_file in code_files:
        #print(f"Processing code file: {code_file}")
        test_result, behavioral_details = test_single_file(test_data, code_file)
        print(f"Test result for: {test_result}")
        test_results.append(test_result)
        edit = True
                
                # Add behavioral details to the collection
        behavioral_equivalence_details.extend(behavioral_details)
    rm.write_report(LLM_folder, repotrt_name, test_results)

            # Write behavioral equivalence report with collected details
    if len(behavioral_equivalence_details) > 1:  # More than just header
        rm.write_behavioral_equivalence_report(LLM_folder, behavioral_equivalence_details)
        #print(f"Behavioral equivalence report written to: {LLM_folder}")

    #rm.print_report(report)
    return True
            
def generate_report_from_avr_chyldren_folder(
    file_path, report_file_name="report_average.csv", print_output=True
):
    rm.delete_all_reports(file_path)

    # {file_name: [sum_code_id, sum_ast, sum_behav, count]}
    stats_by_file = {}

    for child_folder in fm.open_folder_return_folders(file_path):
        report = rm.get_report(child_folder)
        if not report or len(report) <= 1:
            continue

        for row in report[1:]:
            if len(row) < 4:
                continue

            model_name = row[0].strip()
            try:
                code_id = float(row[1])
                ast_struct = float(row[2])
                behav_eq = float(row[3])
            except ValueError:
                continue

            if model_name not in stats_by_file:
                stats_by_file[model_name] = [0.0, 0.0, 0.0, 0]

            stats_by_file[model_name][0] += code_id
            stats_by_file[model_name][1] += ast_struct
            stats_by_file[model_name][2] += behav_eq
            stats_by_file[model_name][3] += 1

    averaged_rows = []
    for model_name, (sum_c, sum_a, sum_b, count) in stats_by_file.items():
        if count > 0:
            averaged_rows.append([
                model_name,
                round(sum_c / count, 4),
                round(sum_a / count, 4),
                round(sum_b / count, 4),
            ])

    if averaged_rows:
        rm.write_report(file_path, report_file_name, averaged_rows)

    if print_output:
        created_report = rm.get_report(file_path, report_file_name)
        rm.print_report(created_report)

    return Path(file_path) / report_file_name if averaged_rows else None


    
    return reports

def evaluacion_folder(test_data, file_path): ## generuje report v {test}{languare}
    edit = False

    for code_languare_folder in fm.open_folder_return_folders(file_path):
        languare = get_Languare(Path(code_languare_folder).name)
        print(f"Languare: {languare}")

        #print(code_languare_folder)

        # Process all LLM folders for this language
        for LLM_folder in fm.open_folder_return_folders(code_languare_folder):
            llm = llm_folder(LLM_folder, test_data)
            #print(f"Processing LLM folder: {LLM_folder}")
            edit = edit or llm

        # Skip report generation if no updates for this language folder, and a report already exists
        if not edit and rm.get_report(code_languare_folder) is not None:
            print(f"\tNo updates for {Path(code_languare_folder).name}")
            continue

        rm.delete_all_reports(code_languare_folder)
        for LLM_folder in fm.open_folder_return_folders(code_languare_folder):
            llm_name = Path(LLM_folder).name
            report_llm = rm.get_report(LLM_folder)
            if report_llm is None:
                print(f"Report not found for LLM folder: {LLM_folder}")
                return -1
            llm_report_average = rm.get_average_report(report_llm)
            if llm_report_average is None:
                print(f"Could not calculate average for LLM folder: {LLM_folder}")
                return -1
            row = [llm_name, *llm_report_average]
            #print(row)
            rm.write_report(code_languare_folder, f"Report_{Path(code_languare_folder).name}.csv", [row])

        rm.print_report(rm.get_report(code_languare_folder))
        
        # Reset edit flag for next language folder
        edit = True
    if edit:
        print("\tUpdates were made for at least one language folder.")
        #generate_report_from_avr_chyldren_folder(file_path)


    return edit


def report_os(folder_os):
    os_name = Path(folder_os).name
    print(os_name)


def main():
    if not Path(Evaluation_folder).exists():
        print(f"Evaluation folder not found: {Evaluation_folder}")
        return


    prompts_folder = Path(Evaluation_folder) / "Prompts"
    if not prompts_folder.exists() or not prompts_folder.is_dir():
        print("Priečinok 'Prompts' neexistuje (alebo je to len obyčajný súbor).")
        return

    Results_folder = Path(Evaluation_folder) / "Results"
    if not Results_folder.exists():
        print(f"Results folder not found in {Evaluation_folder}, creating it.")
        return

    update = False
    
    for folder_os in fm.open_folder_return_folders(Results_folder):
        update_os = False
        print(Path(folder_os).name)
        for folder in fm.open_folder_return_folders(prompts_folder):
                #print(folder)
            folder_tasks_name = Path(folder).name
            print(folder_tasks_name+":")
        
                # if tests_data.txt in folder
            file_path = Path(folder) / "tests_data.txt"
        
            if not file_path.is_file():
                print(f"\033[93m'tests_data.txt' not found in {folder}\033[0m")
                continue

            tests_data = fm.load_setup(os.path.join(folder, "tests_data.txt"))
            file_path = Path(folder_os) / folder_tasks_name
            # if folder_tasks_name je v folder_os
            if not file_path.exists():
                print(f"{folder_tasks_name} not found in {folder_os}")
                continue


            update_os = update_os or evaluacion_folder(tests_data, file_path)

        print(f"Update status for OS folder {Path(folder_os).name}: {update_os}")
        update = update or update_os

        #report_os = rm.get_report(folder_os)
        #rm.print_report(report_os)
        #if report_os is None or report_os:
        #    report_os(folder_os)

        if update == -1:
            print(f"Error occurred while evaluating folder: {file_path}")
            return -1


    
    print(f"Evaluation completed. Update status: {update}")
    if not update:
        print("No updates were made.")
        return



if __name__ == "__main__":
    main()