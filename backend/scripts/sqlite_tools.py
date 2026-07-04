import argparse
import shutil
from datetime import datetime
from pathlib import Path


def resolve_db_path(db_url: str, backend_dir: Path) -> Path:
    prefix = "sqlite:///"
    if not db_url.startswith(prefix):
        raise ValueError(f"Expected sqlite URL, got: {db_url}")

    raw_path = db_url[len(prefix):]
    path = Path(raw_path)
    if not path.is_absolute():
        path = (backend_dir / path).resolve()
    return path


def backup_db(db_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{db_path.stem}_{timestamp}{db_path.suffix}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def reset_db(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()


def load_db_url(env_file: Path) -> str:
    if not env_file.exists():
        return "sqlite:///./energem.db"

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("DATABASE_URL="):
            return line.split("=", 1)[1].strip()

    return "sqlite:///./energem.db"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backup/reset/status helper for prototype SQLite database."
    )
    parser.add_argument(
        "action",
        choices=["status", "backup", "reset"],
        help="Operation to perform on the SQLite DB",
    )
    parser.add_argument(
        "--db-url",
        help="Override DB URL (defaults to DATABASE_URL from ../.env)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip reset confirmation prompt",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    backend_dir = script_dir.parent
    repo_dir = backend_dir.parent

    db_url = args.db_url or load_db_url(repo_dir / ".env")
    db_path = resolve_db_path(db_url, backend_dir)
    backup_dir = backend_dir / "db" / "backups"

    if args.action == "status":
        print(f"DATABASE_URL: {db_url}")
        print(f"DB path: {db_path}")
        print(f"Exists: {db_path.exists()}")
        if db_path.exists():
            print(f"Size bytes: {db_path.stat().st_size}")
        return

    if args.action == "backup":
        if not db_path.exists():
            raise FileNotFoundError(f"Database file not found: {db_path}")
        backup_path = backup_db(db_path, backup_dir)
        print(f"Backup created: {backup_path}")
        return

    if args.action == "reset":
        if not args.yes:
            answer = input(
                f"Delete SQLite DB at '{db_path}'? Type 'yes' to continue: "
            ).strip()
            if answer.lower() != "yes":
                print("Reset cancelled.")
                return

        reset_db(db_path)
        print(f"Database reset complete. Removed: {db_path}")


if __name__ == "__main__":
    main()
