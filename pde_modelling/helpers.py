from math import isfinite


# shared bits used by all three solvers
# the ask functions keep asking until they get something valid, so a typo can't crash anything
#
# there are two kinds of limit:
#   low / high  are hard limits, the maths breaks or it makes no sense past them, so it won't let you
#   typical     is the range real stuff sits in. outside it you get a warning saying what goes
#               wrong, but you can still say yes and use it if you want to see what happens


def askYesNo(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False

        print("  Just y or n")


def warnAndConfirm(message):
    # prints a warning and asks if they want to keep going anyway
    # True means use it, False means go back and type something else
    print()
    print("  Heads up: " + message)
    ok = askYesNo("  Use it anyway? (y/n): ")
    print()

    return ok


def askFloat(prompt, low=None, high=None, notZero=False, typical=None, warning=""):
    # low and high are strict, so low=0 means it has to be bigger than 0, not 0 itself
    # typical is (smallest, biggest) and warning is what to tell them if they go outside it
    while True:
        text = input(prompt).strip()

        try:
            value = float(text)
        except ValueError:
            print("  That's not a number, try again")
            continue

        # float() will happily take 'inf' or 'nan', neither of those are any use here
        if not isfinite(value):
            print("  Needs to be an actual number, try again")
            continue

        if low is not None and value <= low:
            print(f"  Has to be bigger than {low:g}, try again")
            continue

        if high is not None and value >= high:
            print(f"  Has to be less than {high:g}, try again")
            continue

        if notZero and value == 0:
            print("  Can't be 0, try again")
            continue

        if typical is not None and (value < typical[0] or value > typical[1]):
            message = f"{value:g} is outside the usual range of {typical[0]:g} to {typical[1]:g}."
            if warning != "":
                message += "\n  " + warning

            if not warnAndConfirm(message):
                continue

        return value


def askInt(prompt, low, high, typical=None, warning=""):
    # low and high are both allowed here, typical works the same as in askFloat
    while True:
        text = input(prompt).strip()

        try:
            value = int(text)
        except ValueError:
            print("  Has to be a whole number, try again")
            continue

        if value < low or value > high:
            print(f"  Has to be between {low} and {high}, try again")
            continue

        if typical is not None and (value < typical[0] or value > typical[1]):
            message = f"{value} is outside the usual range of {typical[0]} to {typical[1]}."
            if warning != "":
                message += "\n  " + warning

            if not warnAndConfirm(message):
                continue

        return value


def askFourierTerms():
    # same question in all three, so it lives here
    # too few terms and the graph has ripples that aren't really there,
    # too many and you're just waiting for no visible difference

    return askInt("  Enter upper limit for Fourier sum: ", 1, 5000, typical=(100, 2000),
                  warning="Under 100 the series hasn't settled so you'll see wobbles near any sharp corner. "
                          "Over 2000 it gets slow (could be a minute or more) and looks the same anyway.")


def pickTimeUnit(tMax):
    # tMax comes in as seconds. this picks whatever unit makes the times on the graph
    # sensible numbers, so a guitar string shows ms and a big lump of steel shows hours
    # gives back the unit name and what to multiply the seconds by
    if tMax < 1e-3:
        return "µs", 1e6
    if tMax < 1:
        return "ms", 1e3
    if tMax < 120:
        return "s", 1
    if tMax < 2 * 3600:
        return "min", 1 / 60
    if tMax < 2 * 86400:
        return "h", 1 / 3600
    if tMax < 2 * 365 * 86400:
        return "days", 1 / 86400

    return "years", 1 / (365 * 86400)
