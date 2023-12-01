# This is less robust but avoids the click import, which should cut down the
# benchmark times. There is no proper error handling for invalid ENV.
import os


def run():
    input = os.getenv("AOC_INPUT")
    day = int(os.getenv("AOC_DAY"))
    # we're going to always assume json
    # json = os.getenv("AOC_JSON")
    json = True

    name = "aoc.day{:02d}".format(day)

    try:
        # Lazily loading the modules prevents the overhad of loading _every_
        # module for every day just to get the solution for one of the days.
        # This, in theory, improves startup times and therefore runtimes.
        #
        # This is "safe" because we explicitly format the day param as a digit
        # and we control the lookup path. Click should also prevent non-integers
        # from being accepted for the DAY argument.
        import importlib
        solver = importlib.import_module(name)
    except ModuleNotFoundError:
        import sys

        # for a better experience, distinguish between "a day we haven't
        # implemented yet," and "a day that is invalid."
        if day < 1 or day > 25:
            print(f"invalid day: {day}")
            sys.exit(1)

        msg = "not implemented"

        import json
        print(json.dumps(msg))

        # this is nonzero for a day that we just haven't implemented yet
        # (according to the spec).
        sys.exit(0)

    with open(input) as f:
        # alwasy True for json rendering
        print(solver.Solver.solve(f.read()).to_string(True))


if __name__ == "__main__":
    run()
