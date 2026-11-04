from pde_modelling import heat, wave, laplace


# main menu, pick which PDE to solve and graph
# run with: python -m pde_modelling   (or just run main.py)


def showInfo():
    print()
    print("  This is a PDE equation solver and grapher, based on the 1D Heat, Wave and Laplace equations.")
    print()
    print("  1 - Heat    : a rod starting at one temperature, cooling with both ends held at 0")
    print("  2 - Wave    : a string plucked at one point and let go")
    print("  3 - Laplace : a membrane on a frame with one edge pushed up into a triangle")
    print()
    print("  Every one is solved with a Fourier sine series, the upper limit you type in is")
    print("  how many terms get added up. Bigger is more accurate but slower.")
    print()


def main():
    mode = ""

    # mode is kept as text now. before it was int(input()) which crashed if you typed 'menu',
    # and the while mode == 1 loops never ended so it couldn't get back to the menu
    while mode != "q":
        print()

        # Ctrl+C or closing the input used to dump a big error, now it just quits
        try:
            mode = input("  Choose mode ('menu' - Info, 1 - Heat Equation, 2 - Wave Equation, 3 - Laplace Equation, q - Quit): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        print()

        if mode == "menu":
            showInfo()
        try:
            if mode == "1":
                heat.run()
            elif mode == "2":
                wave.run()
            elif mode == "3":
                laplace.run()
            elif mode != "q" and mode != "menu":
                print("  Not an option, try again")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C halfway through one of them goes back to the menu instead of crashing
            print()
            print("  Cancelled, back to the menu")


if __name__ == "__main__":
    main()
