# Python Calculator

## GitHub Pages

Website: **https://bocchi5101.github.io/Calculator/**

The workflow in `.github/workflows/pages.yml` publishes `static/` after each
push to `main`. The web calculator performs arithmetic in JavaScript, so it
works on GitHub Pages without a Python server. Relative asset paths support
the `/Calculator/` URL, including the music player.

The Python terminal calculator and optional Python API are also included.

## Optional Render deployment

This directory is the repository root. A Render Blueprint is included in
`render.yaml` to host both the frontend and Python calculation API.

1. Push this directory to your GitHub repository.
2. In Render, create a Blueprint and select that repository.
3. Review the `orbit-calculator` web service and deploy it.

Render installs `requirements.txt` and starts the WSGI application using
Gunicorn. `/health` is the health check endpoint. Deployment configuration
follows the [Render Blueprint documentation](https://render.com/docs/blueprint-spec).
The local `server.py` command below still requires no extra packages.

The included `static/music.mp3` is served to visitors along with the website.

## Space-themed web interface

Run from the ScriptsPY directory:

```powershell
python .\Calculater\server.py
```

Then open **http://127.0.0.1:8000** in your browser. Keep the server running
while using the calculator; press Ctrl+C in the terminal to stop it.
No extra packages or internet connection are required.

Background music uses the local copy of **SKILLET - MONSTER.mp3** in
`static/music.mp3`. It attempts to play on opening the page at 35% volume and
loops. If your browser blocks autoplay with sound, click **Play music**.
Use **Pause music** to stop playback.

The responsive HTML/CSS interface includes a star field, a CSS planet, calculator
buttons, keyboard input, clear, backspace, and sign switching. Web calculations
run in the browser. Chained operations are
evaluated from left to right, like a basic pocket calculator.

## Terminal interface

A terminal calculator for addition, subtraction, multiplication, and division.
Supports negative numbers and decimals, checks invalid input, and handles division by zero.
Requires Python 3; no extra packages are needed.

From the ScriptsPY directory, run:

```powershell
python .\Calculater\calculator.py
```

Enter the first number, an operator (`+`, `-`, `*`, `/`), and the second number
when prompted. You can keep calculating or type `q` at any prompt to quit.

Example: enter `12`, then `*`, then `3` to get `36`.

Calculations use floating-point numbers, so some decimal results may be approximate.
