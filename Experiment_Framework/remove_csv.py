from pathlib import Path
import argparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CODE_GENERATION_TASKS = str(PROJECT_ROOT / "Code_Generation_Tasks")


def remove_csv_files(root_folder: str, dry_run: bool = False) -> int:
    root_path = Path(root_folder).resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_path}")

    removed_count = 0
    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() == ".csv":
            if dry_run:
                print(f"[DRY-RUN] Would remove: {file_path}")
            else:
                file_path.unlink()
                print(f"Removed: {file_path}")
            removed_count += 1

    return removed_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove all .csv files in CODE_GENERATION_TASKS recursively."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be removed without deleting them.",
    )
    args = parser.parse_args()

    removed = remove_csv_files(CODE_GENERATION_TASKS, dry_run=args.dry_run)
    action = "would be removed" if args.dry_run else "removed"
    print(f"Done. {removed} CSV file(s) {action}.")


if __name__ == "__main__":
    main()
