import ast
import contextlib
import difflib
import importlib.util
import inspect
import io
import math
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import Experiment_Framework.funcion.file_manager as fm


HEADER = [
    "File_name",
    "Code_Identity",
    "AST_Structure",
    "Behavioral_Equivalence",
]


def review_file_hed():
    return HEADER


def _iter_candidate_files(folder_path):
    files = []
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        if not os.path.isfile(file_path):
            continue
        if file_name.lower().endswith((".csv", ".txt")):
            continue
        files.append(file_path)
    return files


def _find_test_data_root(folder_path):
    current = os.path.abspath(folder_path)
    while True:
        for file_name in ("tests_data.txt", "test_data.txt"):
            candidate = os.path.join(current, file_name)
            if os.path.isfile(candidate):
                return current, candidate
        parent = os.path.dirname(current)
        if parent == current:
            return None, None
        current = parent


def _load_tests_data(folder_path):
    root_dir, file_path = _find_test_data_root(folder_path)
    if file_path is None:
        return {}, None
    return fm.load_setup(file_path), file_path


def _serialize_ast(source_code):
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None
    identifier_map = {}

    class _IdentifierNormalizer(ast.NodeTransformer):
        def _normalize(self, name):
            if name not in identifier_map:
                identifier_map[name] = f"id_{len(identifier_map)}"
            return identifier_map[name]

        def visit_Name(self, node):
            node.id = self._normalize(node.id)
            return self.generic_visit(node)

        def visit_arg(self, node):
            node.arg = self._normalize(node.arg)
            return self.generic_visit(node)

        def visit_FunctionDef(self, node):
            node.name = self._normalize(node.name)
            return self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node):
            node.name = self._normalize(node.name)
            return self.generic_visit(node)

        def visit_ClassDef(self, node):
            node.name = self._normalize(node.name)
            return self.generic_visit(node)

    normalized_tree = _IdentifierNormalizer().visit(tree)
    return ast.dump(normalized_tree, include_attributes=False)


def _is_correct_result(actual, expected):
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual is expected

    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=1e-9)

    if actual == expected:
        return True

    if isinstance(actual, str) and not isinstance(expected, str):
        parsed_actual = _parse_test_value(actual)
        if parsed_actual is not actual:
            return _is_correct_result(parsed_actual, expected)

    try:
        return math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=1e-9)
    except (TypeError, ValueError):
        return str(actual) == str(expected)


def _parse_test_value(raw_value):
    if not isinstance(raw_value, str):
        return raw_value

    value = raw_value.strip()
    if value == "":
        return value

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "none":
        return None

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        pass

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        return value


def _build_invocation_candidates(raw_input, parsed_input):
    candidates = [((raw_input,), {}, "raw")]

    if parsed_input is not raw_input:
        candidates.append(((parsed_input,), {}, "parsed"))

    if isinstance(parsed_input, tuple):
        candidates.append((tuple(parsed_input), {}, "tuple_unpack"))
    elif isinstance(parsed_input, list):
        candidates.append((tuple(parsed_input), {}, "list_unpack"))
    elif isinstance(parsed_input, dict):
        candidates.append(((), dict(parsed_input), "dict_kwargs"))

    if isinstance(raw_input, str):
        text = raw_input.strip()
        if "," in text and not any(ch in text for ch in "()[]{}"):
            split_parts = [part.strip() for part in text.split(",")]
            if all(part != "" for part in split_parts):
                parsed_parts = tuple(_parse_test_value(part) for part in split_parts)
                candidates.append((parsed_parts, {}, "comma_split"))

        if ";" in text and not any(ch in text for ch in "()[]{}"):
            split_parts = [part.strip() for part in text.split(";")]
            if all(part != "" for part in split_parts):
                parsed_parts = tuple(_parse_test_value(part) for part in split_parts)
                candidates.append((parsed_parts, {}, "semicolon_split"))

    unique_candidates = []
    seen = set()
    for args, kwargs, label in candidates:
        key = (repr(args), repr(sorted(kwargs.items())), label)
        if key in seen:
            continue
        seen.add(key)
        unique_candidates.append((args, kwargs, label))

    return unique_candidates


def _invoke_tested_function(tested_function, test_input):
    parsed_input = _parse_test_value(test_input)
    candidates = _build_invocation_candidates(test_input, parsed_input)
    signature = None

    try:
        signature = inspect.signature(tested_function)
    except (TypeError, ValueError):
        signature = None

    last_error = None
    for args, kwargs, _ in candidates:
        if signature is not None:
            try:
                signature.bind(*args, **kwargs)
            except TypeError:
                continue

        try:
            return tested_function(*args, **kwargs), None
        except Exception as error:
            last_error = error

    if last_error is None:
        try:
            return tested_function(test_input), None
        except Exception as error:
            return None, error

    return None, last_error


def _has_single_required_argument(callable_obj):
    try:
        signature = inspect.signature(callable_obj)
    except (TypeError, ValueError):
        return False

    required_positional = [
        parameter for parameter in signature.parameters.values()
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        and parameter.default is inspect.Parameter.empty
    ]
    return len(required_positional) == 1


def _resolve_tested_function(source_module, function_name):
    tested_function = getattr(source_module, function_name, None)
    if callable(tested_function):
        return tested_function, function_name

    tested_function = getattr(source_module, function_name.title(), None)
    if callable(tested_function):
        return tested_function, function_name.title()

    module_callables = {
        name: obj for name, obj in inspect.getmembers(source_module, callable)
        if not name.startswith("_") and _has_single_required_argument(obj)
    }
    close_match = difflib.get_close_matches(function_name, module_callables.keys(), n=1, cutoff=0.72)
    if close_match:
        matched_name = close_match[0]
        return module_callables[matched_name], matched_name

    for _, cls in inspect.getmembers(source_module, inspect.isclass):
        class_method = getattr(cls, function_name, None)
        if callable(class_method):
            try:
                instance = cls()
            except Exception:
                continue

            bound_method = getattr(instance, function_name, None)
            if callable(bound_method):
                return bound_method, f"{cls.__name__}.{function_name}"

    return None, None


def set_codes_name_to_report(report, files):
    print("Setting code names into report...")
    number_of_columns = len(report[0])
    for file_path in files:
        file_name = os.path.basename(file_path)
        report.append([file_name] + [""] * (number_of_columns - 1))
    return report


def _ensure_report(folder_path, report=None):
    report_path = os.path.join(folder_path, "report.csv")
    if os.path.exists(report_path):
        if report is None:
            import csv
            with open(report_path, newline="", encoding="utf-8") as csv_file:
                rows = list(csv.reader(csv_file))
            if rows and rows[0] != HEADER:
                rows = [HEADER[:]]
                rows = set_codes_name_to_report(rows, _iter_candidate_files(folder_path))
                fm.save_file_to_folder(folder_path, "report.csv", rows)
                return rows
            return rows
        return report

    if report is None:
        report = [HEADER[:]]
    else:
        report = [report[0]] if report else [HEADER[:]]

    files = _iter_candidate_files(folder_path)
    report = set_codes_name_to_report(report, files)
    fm.save_file_to_folder(folder_path, "report.csv", report)
    return report


def _load_test_cases(folder_path):
    test_data, _ = _load_tests_data(folder_path)
    if not test_data:
        return None, None

    function_name = test_data.get("funcion") or test_data.get("function")
    if function_name is None:
        return None, None

    return function_name, [
        (_parse_test_value(key), _parse_test_value(value))
        for key, value in test_data.items()
        if key not in {"funcion", "function"}
    ]


def _format_score(value):
    return f"{max(0.0, min(1.0, float(value))):.2f}"


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _write_language_summary(language_folder):
    model_folders = fm.open_folder_return_folders(language_folder)
    summary_rows = [[
        "File_name",
        "Code_Identity",
        "AST_Structure",
        "Behavioral_Equivalence",
    ]]

    for model_folder in model_folders:
        model_name = os.path.basename(model_folder)
        report_path = os.path.join(model_folder, "report.csv")
        if not os.path.isfile(report_path):
            continue

        report_rows = fm.load_csv_file(report_path)
        if not report_rows or not report_rows[0]:
            continue

        header = report_rows[0]
        try:
            code_index = header.index("Code_Identity")
            ast_index = header.index("AST_Structure")
            behavior_index = header.index("Behavioral_Equivalence")
        except ValueError:
            continue

        data_rows = report_rows[1:]
        if not data_rows:
            continue

        code_values = [_safe_float(row[code_index] if len(row) > code_index else 0.0) for row in data_rows]
        ast_values = [_safe_float(row[ast_index] if len(row) > ast_index else 0.0) for row in data_rows]
        behavior_values = [_safe_float(row[behavior_index] if len(row) > behavior_index else 0.0) for row in data_rows]

        code_avg = sum(code_values) / len(code_values) if code_values else 0.0
        ast_avg = sum(ast_values) / len(ast_values) if ast_values else 0.0
        behavior_avg = sum(behavior_values) / len(behavior_values) if behavior_values else 0.0

        summary_rows.append([
            model_name,
            _format_score(code_avg),
            _format_score(ast_avg),
            _format_score(behavior_avg),
        ])

    language_name = os.path.basename(language_folder).lower()
    summary_name = f"report_{language_name}.csv"
    fm.save_file_to_folder(language_folder, summary_name, summary_rows)


def behavioral_test(folder_path, report=None):
    print(f"Running behavioral equivalence test in: {folder_path}")
    if not os.path.isdir(folder_path):
        return False

    report = _ensure_report(folder_path, report)
    function_name, test_cases = _load_test_cases(folder_path)
    if function_name is None or not test_cases:
        print(f"\033[93mNo valid tests_data.txt configuration found in {folder_path}\033[0m")
        return False

    behavioral_index = report[0].index("Behavioral_Equivalence")
    behavioral_details = [["File_name", "question", "Expect", "Get", "Test"]]
    for row_index, row in enumerate(report[1:], start=1):
        source_file_name = row[0]
        source_file_path = os.path.join(folder_path, source_file_name)
        if not os.path.isfile(source_file_path):
            continue

        if not source_file_name.lower().endswith(".py"):
            report[row_index][behavioral_index] = "0.00"
            for test_input, expected_output in test_cases:
                behavioral_details.append(
                    [source_file_name, test_input, str(expected_output), "N/A", "False"]
                )
            continue

        module_name = f"reviewed_{os.path.splitext(source_file_name)[0].replace('-', '_').replace('.', '_')}"
        module_spec = importlib.util.spec_from_file_location(module_name, source_file_path)
        if module_spec is None or module_spec.loader is None:
            report[row_index][behavioral_index] = "0.00"
            for test_input, expected_output in test_cases:
                behavioral_details.append(
                    [source_file_name, test_input, str(expected_output), "ImportSpecError", "False"]
                )
            continue

        source_module = importlib.util.module_from_spec(module_spec)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                module_spec.loader.exec_module(source_module)
        except Exception:
            report[row_index][behavioral_index] = "0.00"
            for test_input, expected_output in test_cases:
                behavioral_details.append(
                    [source_file_name, test_input, str(expected_output), "ModuleLoadError", "False"]
                )
            continue

        tested_function, resolved_name = _resolve_tested_function(source_module, function_name)
        if tested_function is None:
            report[row_index][behavioral_index] = "0.00"
            for test_input, expected_output in test_cases:
                behavioral_details.append(
                    [source_file_name, test_input, str(expected_output), "FunctionNotFound", "False"]
                )
            continue
        if resolved_name != function_name:
            print(f"\033[90mUsing function '{resolved_name}' in {source_file_name}\033[0m")

        correct_count = 0
        for test_input, expected_output in test_cases:
            actual_output, call_error = _invoke_tested_function(tested_function, test_input)
            if call_error is not None:
                actual_output = f"ERROR: {call_error}"
                passed = False
            else:
                passed = _is_correct_result(actual_output, expected_output)

            behavioral_details.append(
                [source_file_name, test_input, str(expected_output), str(actual_output), "True" if passed else "False"]
            )

            if passed:
                correct_count += 1

        score = correct_count / len(test_cases) if test_cases else 0.0
        report[row_index][behavioral_index] = _format_score(score)

    fm.save_file_to_folder(folder_path, "report.csv", report)
    fm.save_file_to_folder(folder_path, "report_Behavioral_Equivalence.csv", behavioral_details)
    return True


def Code_Identity_test(folder_path, report=None):
    print(f"Running code identity test in: {folder_path}")
    report = _ensure_report(folder_path, report)
    code_identity_index = report[0].index("Code_Identity")
    files = _iter_candidate_files(folder_path)
    if not files:
        return True

    normalized_contents = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file_obj:
            normalized_contents.append((os.path.basename(file_path), file_obj.read().strip()))

    total_files = len(normalized_contents)
    for row_index, row in enumerate(report[1:], start=1):
        file_name = row[0]
        current_content = next((text for name, text in normalized_contents if name == file_name), "")
        matches = 0
        for other_name, other_content in normalized_contents:
            if other_name == file_name:
                continue
            if other_content == current_content:
                matches += 1

        if total_files <= 1:
            score = 1.0
        else:
            score = matches / (total_files - 1)
        report[row_index][code_identity_index] = _format_score(score)

    fm.save_file_to_folder(folder_path, "report.csv", report)
    return True


def AST_Structure_test(folder_path, report=None):
    print(f"Running AST structure test in: {folder_path}")
    report = _ensure_report(folder_path, report)
    ast_index = report[0].index("AST_Structure")
    files = _iter_candidate_files(folder_path)
    parsed = []
    for file_path in files:
        if not file_path.lower().endswith(".py"):
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as source_file:
            source_code = source_file.read()
        normalized = _serialize_ast(source_code)
        parsed.append((os.path.basename(file_path), normalized))

    if not parsed:
        for row_index in range(1, len(report)):
            report[row_index][ast_index] = "0.00"
        fm.save_file_to_folder(folder_path, "report.csv", report)
        return True

    total_files = len(parsed)
    for row_index, row in enumerate(report[1:], start=1):
        file_name = row[0]
        current_ast = next((value for name, value in parsed if name == file_name), None)
        if current_ast is None:
            report[row_index][ast_index] = "0.00"
        else:
            matches = 0
            for other_name, other_ast in parsed:
                if other_name == file_name:
                    continue
                if other_ast == current_ast:
                    matches += 1
            if total_files <= 1:
                score = 1.0
            else:
                score = matches / (total_files - 1)
            report[row_index][ast_index] = _format_score(score)

    fm.save_file_to_folder(folder_path, "report.csv", report)
    return True


def Behavioral_Equivalence_test(folder_path, report=None):
    print(f"Running behavioral equivalence test in: {folder_path}")
    return behavioral_test(folder_path, report)


def run_all_tests(folder_path, report=None):
    print(f"Running all review tests for: {folder_path}")
    report = _ensure_report(folder_path, report)
    if not Code_Identity_test(folder_path, report):
        return False
    if not AST_Structure_test(folder_path, report):
        return False
    if not Behavioral_Equivalence_test(folder_path, report):
        return False
    return True


def test__folders(folder_path):
    print(f"\tProcessing folder: {folder_path}")
    folders = fm.open_folder_return_folders(folder_path)
    for language_folder in folders:
        for model_folder in fm.open_folder_return_folders(language_folder):
            report = _ensure_report(model_folder)
            if not run_all_tests(model_folder, report):
                print(f"\033[91mReview failed for folder: {model_folder}\033[0m")
            else:
                print(f"\033[92mReview passed for folder: {model_folder}\033[0m")
        _write_language_summary(language_folder)
    return True


if __name__ == "__main__":
    CODE_GENERATION_TASKS = str(PROJECT_ROOT / "Code_Generation_Tasks")
    print("Zacinam prechadzat testovaciu zlozk:")
    for folder in fm.open_folder_return_folders(CODE_GENERATION_TASKS):
        test__folders(folder)
