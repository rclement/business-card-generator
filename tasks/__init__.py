from invoke import task
from invoke.context import Context


app_path = "business_card_generator"
tests_path = "tests"


@task
def format(ctx: Context) -> None:
    ctx.run("ruff format .", echo=True, pty=True)


@task
def audit(ctx: Context) -> None:
    ignored_vulns = [
        "GHSA-4xh5-x5gv-qwph",  # pip<=25.2 affected, no resolution yet
    ]
    options = [f"--ignore-vuln {vuln}" for vuln in ignored_vulns]
    ctx.run(f"pip-audit {' '.join(options)}", echo=True, pty=True)


@task
def lint(ctx: Context) -> None:
    ctx.run("ruff check .", echo=True, pty=True)


@task
def static_check(ctx: Context):
    ctx.run(f"mypy --strict {app_path} {tests_path}", echo=True, pty=True)


@task
def security_check(ctx: Context):
    ctx.run(f"bandit -v -r {app_path}", echo=True, pty=True)


@task
def test(ctx: Context):
    ctx.run(
        f"py.test -v --cov={app_path} --cov={tests_path} --cov-branch --cov-report=term-missing {tests_path}",
        echo=True,
        pty=True,
    )


@task(audit, lint, static_check, security_check, test)
def qa(ctx: Context):
    pass
