"""Nox sessions."""

from __future__ import annotations

import shutil
from pathlib import Path

import nox

try:
    import tomllib as tomli
except ImportError:
    import tomli


def get_deps() -> list[str]:
    """Get the main deps."""
    with Path("pyproject.toml").open("rb") as f:
        return tomli.load(f)["project"]["dependencies"]


def get_extras() -> list[str]:
    """Get the extra deps."""
    with Path("pyproject.toml").open("rb") as f:
        extras = tomli.load(f)["project"]["optional-dependencies"]
    return [e for e in extras if e not in ("test", "doc", "dev")]


python_version = ["3.12"]
nox.options.sessions = (
    "pre-commit",
    "type-check",
    "tests",
)


def install_deps(session: nox.Session, extra: str | None = None) -> None:
    """Install package dependencies."""
    deps = [f".[{extra}]"] if extra else ["."]
    session.install(*deps)
    dirs = [".pytest_cache", "build", "dist", ".eggs"]
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)

    patterns = ["*.egg-info", "*.egg", "*.pyc", "*~", "**/__pycache__"]
    for p in patterns:
        for f in Path.cwd().rglob(p):
            shutil.rmtree(f, ignore_errors=True)


@nox.session(name="pre-commit", python=python_version)
def pre_commit(session: nox.Session) -> None:
    """Lint using pre-commit."""
    session.install("pre-commit")
    session.run(
        "pre-commit",
        "run",
        "--all-files",
        "--hook-stage=manual",
        *session.posargs,
    )


@nox.session(name="type-check", python=python_version)
def type_check(session: nox.Session) -> None:
    """Run Pyright."""
    extras = get_extras()
    install_deps(session, ",".join(extras))
    session.install("pyright")
    session.run("pyright")


@nox.session(python=python_version)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    install_deps(session, "test")
    session.run("python", "-m", "pytest", "--doctest-modules", "--cov-report", "html", *session.posargs)
    session.notify("cover")


@nox.session(python=python_version)
def cover(session: nox.Session) -> None:
    """Coverage analysis."""
    session.install("coverage[toml]")
    session.run("coverage", "report")
    session.run("coverage", "erase")
