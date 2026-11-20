
import ast
import contextlib
import io
from pathlib import Path
import Experiment_Framework.funcion.file_manager as fm
import Experiment_Framework.funcion.report_manager as rm


def _read_code(code_file):
    try:
        return Path(code_file).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def _comparison_files(code_file, code_files):
    target = Path(code_file).resolve()
    return [
        Path(other)
        for other in code_files
        if Path(other).resolve() != target
    ]


def Code_Identity(code_file, code_files):
    # funkcija porovna code_file s ostatnymi subormi v code_files
    # returne hodnotu 0.0 az 1 na zaklade podobnosti suborov, 1-kod je indenticky so vsetkimi ostatnymi subormi
    source = _read_code(code_file)
    if source is None:
        return 0.0

    other_files = _comparison_files(code_file, code_files)
    if not other_files:
        return 1.0

    identical_count = 0
    for other_file in other_files:
        other_source = _read_code(other_file)
        if other_source is not None and source == other_source:
            identical_count += 1

    return round(identical_count / len(other_files), rm.ROUND_TO)


class _IdentifierNormalizer(ast.NodeTransformer):
    def __init__(self):
        self._identifiers = {}

    def _normalize_identifier(self, identifier):
        if identifier not in self._identifiers:
            self._identifiers[identifier] = (
                f"identifier_{len(self._identifiers)}"
            )
        return self._identifiers[identifier]

    def visit_Name(self, node):
        node.id = self._normalize_identifier(node.id)
        return node

    def visit_arg(self, node):
        node.arg = self._normalize_identifier(node.arg)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = "function"
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        node.name = "async_function"
        return self.generic_visit(node)


def _ast_signature(source):
    tree = ast.parse(source)
    normalized_tree = _IdentifierNormalizer().visit(tree)
    return ast.dump(normalized_tree, include_attributes=False)


def AST_Structure(code_file, code_files):
    # funkcija porovna strukturu AST code_file s ostatnymi subormi v code_files
    # returne hodnotu 0.0 az 1 na zaklade podobnosti AST, 1-kod ma identicku strukturu AST so vsetkimi ostatnymi subormi
    source = _read_code(code_file)
    if source is None:
        return 0.0

    try:
        target_ast = _ast_signature(source)
    except SyntaxError:
        return 0.0

    other_files = _comparison_files(code_file, code_files)
    if not other_files:
        return 1.0

    identical_count = 0
    for other_file in other_files:
        other_source = _read_code(other_file)
        if other_source is None:
            continue
        try:
            other_ast = _ast_signature(other_source)
        except SyntaxError:
            continue
        if target_ast == other_ast:
            identical_count += 1

    return round(identical_count / len(other_files), rm.ROUND_TO)


def _literal_value(value):
    if not isinstance(value, str):
        return value

    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value


def _load_function(code_file, function_name):
    source = _read_code(code_file)
    if source is None:
        raise ValueError(f"Could not read code file: {code_file}")

    namespace = {
        "__file__": str(code_file),
        "__name__": "__generated_code__",
    }
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
        io.StringIO()
    ):
        exec(compile(source, str(code_file), "exec"), namespace)

    function = namespace.get(function_name)
    if not callable(function):
        raise AttributeError(f"Function '{function_name}' was not found")
    return function


def _display_value(value):
    try:
        return repr(value)
    except Exception:
        return f"<unrepresentable {type(value).__name__}>"


def _results_equal(actual, expected):
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    return actual == expected


def Behavioral_Equivalence(code_file, tests_data):
    # funkcija porovna spravanie code_file s testami v tests_data
    # returne hodnotu 0.0 az 1 na zaklade toho, ako dobre code_file prechadza testami
    # a nasledne zapise vysledok do reportu 

    function_name = tests_data.get("function", tests_data.get("funcion"))
    test_cases = [
        (question, expected)
        for question, expected in tests_data.items()
        if question not in {"function", "funcion"}
    ]
    if not function_name or not test_cases:
        return 0.0

    try:
        function = _load_function(code_file, str(function_name))
        load_error = None
    except Exception as error:
        function = None
        load_error = error

    report_rows = []
    passed_count = 0
    for question, expected_value in test_cases:
        expected = _literal_value(expected_value)
        arguments = _literal_value(question)
        args = arguments if isinstance(arguments, tuple) else (arguments,)

        if load_error is not None:
            actual_text = (
                f"{type(load_error).__name__}: {load_error}"
            )
            passed = False
        else:
            try:
                with contextlib.redirect_stdout(
                    io.StringIO()
                ), contextlib.redirect_stderr(io.StringIO()):
                    actual = function(*args)
                actual_text = _display_value(actual)
                passed = _results_equal(actual, expected)
            except Exception as error:
                actual_text = f"{type(error).__name__}: {error}"
                passed = False

        if passed:
            passed_count += 1
        report_rows.append(
            [
                Path(code_file).name,
                str(question),
                _display_value(expected),
                actual_text,
                "PASS" if passed else "FAIL",
            ]
        )

    rm.write_behavioral_equivalence_report(
        Path(code_file).parent, report_rows
    )
    return round(passed_count / len(test_cases), rm.ROUND_TO)

def run_all_tests(folder_path, tests_data):
    #print(f"python testy folder: {Path(folder_path).name}")

    report_files = Path(folder_path).name + ".csv"
    #print(f"Report files: {report_files}")
    rm.delete_all_reports(folder_path) # odstrani vsetke stare reporty

    code_files = fm.get_codes_files(folder_path)
    for code in code_files:
        print(f"Running test for code file: {Path(code).name}")
        row = [Path(code).name]
        row[1:] = [Code_Identity(code, code_files)]
        row[2:] = [AST_Structure(code, code_files)]
        row[3:] = [Behavioral_Equivalence(code, tests_data)]
        print(row)
        rm.write_report(Path(folder_path) / report_files, [row])

    
    return True
