import importlib

import click


# according to the specification, we accept the AOC_DAY, AOC_INPUT, and AOC_JSON
# environment variables as alternatives to specifying args.
@click.command()
@click.argument("day", type=int, envvar="AOC_DAY")
@click.argument("input", type=click.File("r"), envvar="AOC_INPUT")
@click.option(
    "-j",
    "--json",
    is_flag=True,
    default=False,
    envvar="AOC_JSON",
    help="display solution as JSON",
)
def run(day: int, input, json: bool) -> None:
    """Produces solutions for Advent of Code 2023

    This takes a DAY (1-25 inclusive) and a path to an INPUT and produces the
    solution for that input.

    \b
    Example:
        mattcl-aoc 3 my_input.txt
    """

    # we assume that every day has a module named day01, day02, day22, etc.
    # we further assume that the module defines a class named `Solver` that
    # derives from the utils Solver class.
    name = "aoc.day{:02d}".format(day)

    try:
        # Lazily loading the modules prevents the overhad of loading _every_
        # module for every day just to get the solution for one of the days.
        # This, in theory, improves startup times and therefore runtimes.
        #
        # This is "safe" because we explicitly format the day param as a digit
        # and we control the lookup path. Click should also prevent non-integers
        # from being accepted for the DAY argument.
        solver = importlib.import_module(name)
    except ModuleNotFoundError:
        import sys

        # for a better experience, distinguish between "a day we haven't
        # implemented yet," and "a day that is invalid."
        if day < 1 or day > 25:
            print(f"invalid day: {day}")
            sys.exit(1)

        msg = "not implemented"

        if json:
            # in the case that we're outputting json, let's print valid json
            import json

            print(json.dumps(msg))
        else:
            print(msg)

        # this is nonzero for a day that we just haven't implemented yet
        # (according to the spec).
        sys.exit(0)

    # We've gotten here so it means we should have a solution for this day.
    # Solve and render the solution
    print(solver.Solver.solve(input.read()).to_string(json))
