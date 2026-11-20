
import csv
from pathlib import Path
import Experiment_Framework.funcion.file_manager as fm

HEADER = [
    "File_name",
    "Code_Identity",
    "AST_Structure",
    "Behavioral_Equivalence",
]

BEHAVIORAL_EQUIVALENCE_REPORT = "report_Behavioral_Equivalence.csv"
BEHAVIORAL_EQUIVALENCE_HEADER = [
    "File_name",
    "question",
    "Expect",
    "Get",
    "Test"
]

ROUND_TO = 2


def get_report(folder_path, report_name = None):
    if report_name is None:
        ## ziskaj .csv subor z foldera ale nesmie to bit BEHAVIORAL_EQUIVALENCE_REPORT
        for file in Path(folder_path).glob("*.csv"):
            if file.name != BEHAVIORAL_EQUIVALENCE_REPORT:
                report_name = file.name
                break

    if report_name is None:
        return None

    report_path = Path(folder_path) / report_name
    if report_path.exists():
        with report_path.open("r", encoding="utf-8", newline="") as f:
           rows_2d = list(csv.reader(f))
           return rows_2d
    return None

def write_report(report_file, report_name_or_results, test_results=None):
    if test_results is None:
        report_file = Path(report_file)
        test_results = report_name_or_results
    else:
        report_file = Path(report_file) / report_name_or_results

    if isinstance(test_results, (str, bytes)):
        raise TypeError("test_results must contain CSV rows, not text")

    if (
        isinstance(test_results, (list, tuple))
        and test_results
        and not isinstance(test_results[0], (list, tuple))
    ):
        test_results = [test_results]

    if not report_file.exists():
        with report_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

    with report_file.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(test_results)

def write_report_B(report_file, data):
    report_file = Path(report_file)
    if data is None or not data:
        return

    if not isinstance(data[0], (list, tuple)):
        data = [data]

    if not report_file.exists():
        with report_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)

    with report_file.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    


def delete_report(folder_path, report_file_name):
    report_file = Path(folder_path) / report_file_name
    if report_file.is_file():
        report_file.unlink()

def delete_behavioral_equivalence_report(folder_path):
    report_file = Path(folder_path) / BEHAVIORAL_EQUIVALENCE_REPORT
    if report_file.is_file():
        report_file.unlink()

def get_average_report(report, File_name = None): # kunkcia vezme folder s reportom a vypočíta priemerné hodnoty pre každý stĺpec (okrem prvého)
    C = 0.0
    B = 0.0
    A = 0.0
    for row in report[1:]:
        if File_name is not None and row[0] != File_name:
            continue
        try:
            C += float(row[1])
        except ValueError:
            pass
        try:
            B += float(row[2])
        except ValueError:
            pass
        try:
            A += float(row[3])
        except ValueError:
            pass

    count = max(len(report) - 1, 1)
    return [round(C / count, ROUND_TO), round(B / count, ROUND_TO), round(A / count, ROUND_TO)]

def delete_all_reports(folder_path):
    #odstran z foldera vsetke .cvs subory
    folder = Path(folder_path)
    for file in folder.glob("*.csv"):
        file.unlink()

def write_behavioral_equivalence_report(folder_path, rows_2d):
    report_file = Path(folder_path) / "report_Behavioral_Equivalence.csv"

    # ked subor neexistuje, vytvor ho s hlavičkou
    if not report_file.exists():
        with report_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(BEHAVIORAL_EQUIVALENCE_HEADER)

    with report_file.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_2d)

def print_report(report, min_gap: int = 2):
  if report is None:
    print("No report available.")
    return

  valid_rows = [
      [str(cell) for cell in row] for row in report if row is not None
  ]
  if not valid_rows:
    return

  # Zistíme šírku najdlhšej hodnoty v každom stĺpci a pridáme minimálny posun
  num_cols = max(len(row) for row in valid_rows)
  col_widths = []

  for col_idx in range(num_cols):
    max_len = max(
        (len(row[col_idx]) for row in valid_rows if col_idx < len(row)),
        default=0,
    )
    col_widths.append(max_len + min_gap)

  for row in valid_rows:
    formatted_cells = [
        cell.ljust(col_widths[idx]) for idx, cell in enumerate(row)
    ]
    print("".join(formatted_cells).rstrip())

def count_report_rows(report: list[list], include_header: bool = False) -> int:
  """Spočíta počet riadkov v načítanom reporte (2D zozname).

  Args:
      report: Dvojrozmerný zoznam riadkov reportu.
      include_header: Ak je True, započíta aj prvý riadok (hlavičku). Ak je
        False, počíta len dátové riadky (predvolené).
  """
  if not report:
    return 0

  if not include_header and len(report) > 0:
    return len(report) - 1
  return len(report)

def create_avg_report_from_chyldren_folders(folder_path):
    delete_all_reports(folder_path)
    report = {}

    for folder_languare in fm.open_folder_return_folders(folder_path):
        if get_report(folder_languare) is None:
            continue
        for row in get_report(folder_languare)[1:]:

            if row[0] not in report:
                report[row[0]] = [0.0,0.0,0.0,0]
            report[row[0]][0] += float(row[1])
            report[row[0]][1] += float(row[2])
            report[row[0]][2] += float(row[3])
            report[row[0]][3] += 1

    for row in report:
        for index in range(len(report[row][:-1])):
            #print(row, report[row][:-1], report[row][3])
            report[row][index] /= report[row][3] # zaokruhlit na ROUND_TO
            report[row][index] = round(report[row][index], ROUND_TO)

        #print([row] + report[row][:-1])
        report_file = Path(folder_path) / (
            f"{Path(folder_path).name}_report.csv"
        )
        write_report_B(report_file, [[row] + report[row][:-1]])
        #write_report(folder_path, folder_path / f"{Path(folder_path).name}_report.csv",[ [row] + report[row][:-1] ])


    print(f"Generated report for: {folder_path}")
        



    return