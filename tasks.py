from invoke import task, exceptions

DIRECTORY = "model_zoo"


def isort(context, directory=DIRECTORY):
    """Run isort for check imports."""
    print("Isort run")
    try:
        context.run(f"isort {directory}")
    except exceptions.Failure as ex:
        return ex.streams_for_display()


def flake(context, directory=DIRECTORY):
    """Run flake for check style code."""
    print("Flake run")
    try:
        context.run(f"flake8 {directory}")
    except exceptions.Failure as ex:
        return ex.streams_for_display()


def pylint(context, directory=DIRECTORY):
    """Run pylint for check style code."""
    print("Pylint run")
    try:
        context.run(f"pylint {directory}")
    except exceptions.Failure as ex:
        return ex.streams_for_display()


@task()
def linters(context, directory=DIRECTORY):
    """Start linters pylint, flake8 and isort.

    This task started proccess pylint, flake for
    check your style code, and isort for check imports.

    Args:
        context (any): Context argument for run commands.
        :param context:
        :param directory:
    """
    errors = {"pylint": pylint(context, directory), "flake": flake(context, directory),
              "isort": isort(context, directory)}
    for key, value in errors.items():
        if value:
            raise exceptions.Failure(f"Linter {key} failed", "Bad code style")
