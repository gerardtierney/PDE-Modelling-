# PDE-Modelling-

Solves and graphs three of the PDEs from MA2102 using Fourier series.

- **Heat equation** - a rod starting at one uniform temperature, both ends held at 0. Shows it cooling over time.
- **Wave equation** - a string plucked at one point and let go from rest, both ends tied down. Shows half a period of it moving.
- **Laplace equation** - a membrane stretched over a rectangular frame with one edge pushed up into a triangle. Shows slices across it and the full 3D shape.

## Running it

```
pip install -r requirements.txt
python -m pde_modelling
```

Or just run `main.py`. Pick a mode from the menu and type in the values it asks for.

## Layout

```
pde_modelling/
    __main__.py   menu
    heat.py       heat equation
    wave.py       wave equation
    laplace.py    laplace / membrane
main.py           runs the menu
```
