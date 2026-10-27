import csv
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
TASKS_DIR = PROJECT_ROOT / "Code_Generation_Tasks"

METRICS = (
    ("Code_Identity", "Code Identity"),
    ("AST_Structure", "AST Structure"),
    ("Behavioral_Equivalence", "Behavioral Equivalence"),
)

LANGUAGE_OPTIONS = {
    "Python": "py",
    "JavaScript": "js",
    "Java": "java",
    "C++": "cpp",
    "C#": "cs",
    "Go": "go",
    "Ruby": "rb",
    "PHP": "php",
}

MODEL_OPTIONS = [
    "Gemini_gemini-3.1-flash-lite",
    "Gemini_gemini-3.1-flash",
    "Ollama_qwen2.5-coder:14b",
    "Ollama_gemma4:e4b",
    "Ollama_qwen3:8b",
    "Ollama_qwen3.5:9b",
]


def esc(value):
    return str(value if value is not None else "")


def project_config_path(project_name: str) -> Path:
    return TASKS_DIR / project_name / ".dashboard.json"


def load_project_config(project_name: str) -> dict:
    config_path = project_config_path(project_name)
    if not config_path.exists():
        return {"include_in_averages": True}
    try:
        with config_path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        if isinstance(loaded, dict):
            return {
                "include_in_averages": bool(loaded.get("include_in_averages", True)),
            }
    except (json.JSONDecodeError, OSError):
        pass
    return {"include_in_averages": True}


def save_project_config(project_name: str, include_in_averages: bool) -> None:
    project_dir = TASKS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    config_path = project_config_path(project_name)
    with config_path.open("w", encoding="utf-8") as handle:
        json.dump({"include_in_averages": bool(include_in_averages)}, handle, indent=2)


def list_projects() -> list[str]:
    if not TASKS_DIR.exists():
        return []
    return sorted(
        project.name for project in TASKS_DIR.iterdir() if project.is_dir() and not project.name.startswith(".")
    )


def normalize_report_row(row: dict) -> dict:
    normalized = {
        (key or "").strip(): (value or "").strip() for key, value in row.items()
    }
    metrics = {}
    for key, _label in METRICS:
        raw = normalized.get(key, "")
        try:
            metrics[key] = float(raw) if raw else None
        except ValueError:
            metrics[key] = None
    return {
        "file_name": normalized.get("File_name", "Unknown"),
        "metrics": metrics,
    }


def read_reports() -> list[dict]:
    reports = []
    if not TASKS_DIR.exists():
        return reports

    for project_name in list_projects():
        project_dir = TASKS_DIR / project_name
        for language_dir in sorted(project_dir.iterdir()):
            if not language_dir.is_dir():
                continue
            csv_candidates = sorted(language_dir.glob("report_*.csv"))
            for csv_path in csv_candidates:
                rows = []
                try:
                    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            asset = normalize_report_row(row)
                            if not any(asset["metrics"].values()) and not asset["file_name"]:
                                continue
                            rows.append(asset)
                    reports.append(
                        {
                            "project": project_name,
                            "language": language_dir.name,
                            "path": str(csv_path.relative_to(TASKS_DIR)),
                            "rows": rows,
                            "error": None,
                            "modified": datetime.fromtimestamp(csv_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                            "include_in_averages": load_project_config(project_name).get("include_in_averages", True),
                        }
                    )
                except (OSError, csv.Error, UnicodeError) as exc:
                    reports.append(
                        {
                            "project": project_name,
                            "language": language_dir.name,
                            "path": str(csv_path.relative_to(TASKS_DIR)),
                            "rows": [],
                            "error": str(exc),
                            "modified": "",
                            "include_in_averages": load_project_config(project_name).get("include_in_averages", True),
                        }
                    )
    return reports


def fmt_metric(value) -> str:
    if isinstance(value, (int, float)):
        return f"{value:.2f}"
    return "—"


def metric_class(value) -> str:
    if not isinstance(value, (int, float)):
        return "missing"
    if value >= 0.8:
        return "high"
    if value >= 0.5:
        return "medium"
    return "low"


def project_summary_rows(reports: list[dict]) -> list[tuple]:
    buckets = {}
    for report in reports:
        if not report.get("include_in_averages", True):
            continue
        for row in report["rows"]:
            model_name = row.get("file_name") or "Unknown"
            bucket = buckets.setdefault(
                model_name,
                {
                    "samples": 0,
                    "all_values": [],
                    "metric_values": {key: [] for key, _label in METRICS},
                },
            )
            bucket["samples"] += 1
            for key, _label in METRICS:
                value = row["metrics"].get(key)
                if isinstance(value, (int, float)):
                    bucket["metric_values"][key].append(value)
                    bucket["all_values"].append(value)

    rows = []
    for model_name, bucket in buckets.items():
        metric_avg = {}
        for key, _label in METRICS:
            values = bucket["metric_values"][key]
            metric_avg[key] = (sum(values) / len(values)) if values else None
        overall_avg = sum(bucket["all_values"]) / len(bucket["all_values"]) if bucket["all_values"] else None
        rows.append((model_name, bucket["samples"], metric_avg, overall_avg))

    rows.sort(key=lambda item: (item[3] if isinstance(item[3], (int, float)) else -1, item[0].lower()), reverse=True)
    return rows


def average_values(reports: list[dict]) -> dict:
    values = {}
    for key, _label in METRICS:
        collected = []
        for report in reports:
            if not report.get("include_in_averages", True):
                continue
            for row in report["rows"]:
                value = row["metrics"].get(key)
                if isinstance(value, (int, float)):
                    collected.append(value)
        values[key] = sum(collected) / len(collected) if collected else None
    return values


def project_overview() -> list[dict]:
    project_names = list_projects()
    project_rows = []
    for project_name in project_names:
        config = load_project_config(project_name)
        project_rows.append({
            "name": project_name,
            "include_in_averages": bool(config.get("include_in_averages", True)),
            "report_count": len([report for report in read_reports() if report["project"] == project_name]),
        })
    return project_rows


def create_project_files(project_name: str, prompt_text: str, tests_data_text: str, setup_text: str) -> dict:
    clean_name = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in project_name).strip(" -_") or "Project"
    project_dir = TASKS_DIR / clean_name
    if project_dir.exists():
        raise FileExistsError(f"Projekt '{clean_name}' už existuje.")

    project_dir.mkdir(parents=True, exist_ok=False)
    (project_dir / "promp.txt").write_text(prompt_text, encoding="utf-8")
    (project_dir / "tests_data.txt").write_text(tests_data_text, encoding="utf-8")
    (project_dir / "setup.txt").write_text(setup_text, encoding="utf-8")
    save_project_config(clean_name, True)
    return {"project_name": clean_name, "path": str(project_dir)}


def build_setup_content(selected_models, language, num_generations, extra_lines):
    base_lines = [
        f"models={','.join(selected_models)}",
        f"language={language}",
        f"num_generations={int(num_generations)}",
        "temperature=0",
        "top_p=1",
        "top_k=40",
        "seed=0",
        "think=false",
        "max_output_tokens=5000",
        "frequency_penalty=0.0",
        "presence_penalty=0.0",
        "num_ctx=4096",
    ]
    if extra_lines:
        base_lines.extend([line.strip() for line in extra_lines.splitlines() if line.strip()])
    return "\n".join(base_lines) + "\n"
