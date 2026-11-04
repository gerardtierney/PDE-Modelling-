import matplotlib.pyplot as plt
from math import pi, sin, e, log
import numpy as np
from pde_modelling.helpers import askFloat, askFourierTerms, pickTimeUnit


# 1D heat equation on a rod: du/dt = alpha^2 * d2u/dx2
# both ends held at 0 the whole time, u(0,t) = u(L,t) = 0
# the rod starts at one uniform temperature everywhere
# solved with the Fourier sine series from MA2102


def fourierConstant(n, initial):
    # Bn for a uniform starting temperature
    # the even ones all come out as 0, so the sum below only goes through odd n
    Bn = (4 * initial) / (n * pi)

    return Bn


def time_to_near_zero(length, alphaSqr, epsilon=0.01):
    # n = 1 is the slowest term to die off, so once e^(-alpha^2 pi^2 t / L^2) gets down
    # to epsilon the rod is basically cold. this is that rearranged for t
    return (length ** 2 / (alphaSqr * pi ** 2)) * log(1 / epsilon)


def run():
    print("=" * 55)
    print("   1D Heat Equation Solver - Finite Rod")
    print("=" * 55)
    print()
    print("  Problem Setup:")
    print("  - Rod of length L")
    print("  - Initial temperature : uniform")
    print("  - Boundary conditions : u(0,t) = u(L,t) = 0")
    print("  - Solution via Fourier sine series")
    print("  - Units : metres, seconds, °C")
    print()
    print("=" * 55)
    print()

    # everything gets checked as it's typed in, see helpers.py
    print("  Typical values:")
    print("  - Rod length   : 0.01 to 10 m")
    print("  - Temperature  : -50 to 1500 °C (nothing goes below -273.15, absolute zero)")
    print("  - alpha² (m²/s): copper 1.11e-4, aluminium 9.7e-5, steel 1.2e-5,")
    print("                   glass 3.4e-7, water 1.4e-7, wood 1e-7")
    print("  - Fourier terms: 100 to 2000")
    print()

    length = askFloat("  Enter length of the rod in m: ", low=0, typical=(0.01, 10),
                      warning="Fine for the maths, but a really long rod can take days or years to cool, "
                              "and a really short one cools in a blink.")

    # the ends are held at 0 °C so u is the actual temperature, and that can't go under absolute zero
    initial = askFloat("  Enter initial uniform temperature of the rod in °C: ", low=-273.15, notZero=True,
                       typical=(-50, 1500),
                       warning="Most metals have melted by about 1500 °C, and the model assumes alpha² "
                               "stays the same at every temperature which stops being true at the extremes.")

    # people tend to type 1 or 111 here forgetting the e-4, which makes it cool insanely fast
    alphaSqr = askFloat("  Enter thermal diffusivity alpha² in m²/s: ", low=0, typical=(1e-8, 2e-3),
                        warning="Nothing real is outside this (even diamond is about 1e-3). "
                                "If you meant copper it's 0.000111, not 111 or 1.")

    upper = askFourierTerms()

    print()
    print("  Computing solution...")
    print()

    # x used to be range(0, length + 1) which only works for whole number lengths
    # and gives you about 4 points on a short rod, so now it's always 101 points along it
    points = 101
    Xaxis = np.linspace(0, length, points)

    tMax = time_to_near_zero(length, alphaSqr)
    unit, scale = pickTimeUnit(tMax)

    print(f"  The rod should be basically cold after about {tMax * scale:.3g} {unit}, graphing up to then")
    print()

    value = 0
    T = 0  # next free column in u, only moves on when a time gets kept
    # abs so a rod starting below 0 doesn't make the threshold negative and keep every single time
    deltaThresh = abs(initial) / 10
    deltaT = False
    times_kept = []

    u = np.zeros((points, 101))

    for i in range(0, 101):
        t = (tMax / 100.0) * i
        for j in range(0, points):  # keep t the same, go along the rod
            x = Xaxis[j]

            for n in range(1, upper + 1, 2):  # sum of sines per x
                value += fourierConstant(n, initial) * sin((n * pi * x) / length) * e ** (-alphaSqr * ((n ** 2 * pi ** 2) / length ** 2) * t)

            u[j, T] = value
            value = 0

        # only keep this time if the rod has changed enough since the last one we kept,
        # otherwise the end of the graph is just a load of lines stacked on top of each other
        if T == 0:
            deltaT = True
        else:
            change = []
            for j in range(0, points):
                change.append(abs(u[j, T - 1] - u[j, T]))

            if sum(change) / len(change) >= deltaThresh:
                deltaT = True

        if deltaT == True:
            times_kept.append(t)
            T += 1
            deltaT = False

    print("  Done! Displaying graph...")
    print()

    # plotting

    plt.figure(figsize=(11, 6))

    plt.xlabel("Position x (m)", fontsize=12)
    plt.ylabel("Temperature u(x,t) (°C)", fontsize=12)
    plt.title("Heat Equation Solution", fontsize=14, fontweight="bold", pad=15)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()

    for i in range(T):
        plt.plot(Xaxis, u[:, i], label=f"t={times_kept[i] * scale:.3g} {unit}", linewidth=2)
        plt.pause(0.8)

    plt.legend(fontsize=10, framealpha=0.8)
    plt.show()


if __name__ == "__main__":
    run()
