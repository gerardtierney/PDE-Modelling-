import matplotlib.pyplot as plt
from math import pi, sin, e
import numpy as np
from pde_modelling.helpers import askFloat, askFourierTerms, warnAndConfirm


# Laplace equation on a rectangular membrane: d2u/dx2 + d2u/dy2 = 0
# membrane stretched over a frame, a wide (x) and b tall (y)
# left, bottom and top edges are flat at 0
# the right edge x = a gets pushed up into a triangle with its peak halfway up at y = b/2
# same setup as the membrane example in PDE 8 and 9
# no time in this one, it's just the shape the membrane settles into


def fourierConstant(n, height):
    # Cn for the triangle edge, from the PDE 9 example but with a peak of any height
    # sin(n pi / 2) is 0 for every even n so those drop out
    Cn = (8 * height) / (n ** 2 * pi ** 2) * sin((n * pi) / 2)

    return Cn


def sinhRatio(k, x, a):
    # this is sinh(kx) / sinh(ka) written out with exponentials
    # doing the two sinh's straight up breaks once n gets past about 200
    # because sinh(710) is too big to fit in a float
    # taking e^(k(x-a)) out the front keeps everything between 0 and 1 so it never blows up
    return e ** (k * (x - a)) * (1 - e ** (-2 * k * x)) / (1 - e ** (-2 * k * a))


def run():
    print("=" * 55)
    print("   Laplace Equation Solver - Rectangular Membrane")
    print("=" * 55)
    print()
    print("  Problem Setup:")
    print("  - Membrane a wide (x) by b tall (y)")
    print("  - Edges x = 0, y = 0, y = b : u = 0")
    print("  - Edge x = a : triangle, peak at y = b/2")
    print("  - Solution via Fourier sine series in y")
    print("  - Units : metres (no time, it's a resting shape)")
    print()
    print("=" * 55)
    print()

    # everything gets checked as it's typed in, see helpers.py
    print("  Typical values:")
    print("  - Width a, height b : 0.1 to 10 m, and not more than about 10 times longer one way")
    print("  - Peak height       : small compared to b, under about b/20")
    print("  - Fourier terms     : 100 to 2000")
    print()

    while True:
        a = askFloat("  Enter width of the membrane a in m: ", low=0, typical=(0.1, 10),
                     warning="The maths is fine, it's just a strange size for a membrane.")
        b = askFloat("  Enter height of the membrane b in m: ", low=0, typical=(0.1, 10),
                     warning="The maths is fine, it's just a strange size for a membrane.")

        # the bump from the raised edge dies off over a distance of about b,
        # so if a is way bigger than b almost the whole membrane is flat and the graph shows nothing
        if a / b <= 10 and b / a <= 10:
            break

        if warnAndConfirm(f"the membrane is {max(a / b, b / a):.3g} times longer one way than the other.\n"
                          "  The raised edge only lifts the membrane for about a distance b in from the edge,\n"
                          "  so if a is much bigger than b nearly all of it is flat, and if b is much bigger the\n"
                          "  51 points across won't pick up the shape properly."):
            break

    # same small slope idea as the wave one, the membrane equation in PDE 8 uses sin(theta) ~ theta
    # the raised edge climbs from 0 to the peak over b/2, so its slope is about 2h/b
    while True:
        height = askFloat("  Enter how high the peak of the raised edge is in m: ", notZero=True)

        slope = 2 * abs(height) / b

        if slope <= 0.1:
            break

        if warnAndConfirm(f"the raised edge has a slope of {slope:.2f}.\n"
                          "  The Laplace equation for a membrane assumes small slopes (under about 0.1),\n"
                          "  past that a real membrane wouldn't sit in this shape. A smaller peak fixes it."):
            break

    upper = askFourierTerms()

    print()
    print("  Computing solution...")
    print()

    points = 51
    Xaxis = np.linspace(0, a, points)
    Yaxis = np.linspace(0, b, points)

    value = 0

    # rows are y, columns are x, that's the way round plot_surface wants it later
    u = np.zeros((points, points))

    for i in range(0, points):
        y = Yaxis[i]
        for j in range(0, points):
            x = Xaxis[j]

            for n in range(1, upper + 1, 2):  # sum of sines per point, odd n only
                k = (n * pi) / b
                value += fourierConstant(n, height) * sin(k * y) * sinhRatio(k, x, a)

            u[i, j] = value
            value = 0

    print("  Done! Displaying graphs...")
    print()

    # plotting

    # first graph works like the heat and wave ones, except instead of stepping through time
    # it steps across the membrane in x. each line is a slice going up the membrane in y
    # and they grow from flat at x = 0 to the full triangle at x = a
    plt.figure(figsize=(11, 6))

    plt.xlabel("Position y (m)", fontsize=12)
    plt.ylabel("Displacement u(x,y) (m)", fontsize=12)
    plt.title("Laplace Equation Solution - Slices Across x", fontsize=14, fontweight="bold", pad=15)
    plt.grid(True, linestyle="--", alpha=0.3)
    # works out the limits either way round so a peak pushed down instead of up still fits
    plt.ylim(min(0, height) - 0.1 * abs(height), max(0, height) + 0.1 * abs(height))
    plt.tight_layout()

    slices = np.linspace(0, points - 1, 8).astype(int)

    for j in slices:
        plt.plot(Yaxis, u[:, j], label=f"x={Xaxis[j]:.3g} m", linewidth=2)
        plt.pause(0.8)

    plt.legend(fontsize=10, framealpha=0.8)

    # second graph is the whole membrane in 3D
    X, Y = np.meshgrid(Xaxis, Yaxis)

    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(X, Y, u, cmap="viridis", edgecolor="none")

    ax.set_xlabel("x (m)", fontsize=12)
    ax.set_ylabel("y (m)", fontsize=12)
    ax.set_zlabel("u(x,y) (m)", fontsize=12)
    ax.set_title("Membrane Shape", fontsize=14, fontweight="bold", pad=15)

    plt.show()


if __name__ == "__main__":
    run()
