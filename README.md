# PyVISA GUI Application

A modern GUI application for communicating with measurement instruments such as oscilloscopes and function generators — built with Python, [PyVISA](https://pyvisa.readthedocs.io/), and `customtkinter`.

---

## 🔧 Features

- **Device Detection** – finds and configures connected VISA devices.
- **Data Plot in Display** – visual representation of measurement results.
- **Settings Management** – GUI for user preferences and application settings.
- **Integrated Terminal** – embedded console output.

---

## 📁 Project Structure

```
pyvisa/
├── main.py                  # Entry point of the application
├── UI/                      # GUI components (customtkinter)
│   ├── device_input.py      # Hardware configuration
│   ├── mainframe.py         # Main window
│   ├── output.py            # Data visualization
|   ├── plot_only.py         # Data visualization
│   ├── settings.py          # Application settings
│   └── terminal.py          # Terminal output
├── visa_py/                 # PyVISA-related modules
│   ├── __init__.py
│   ├── resources.py         # Resource management
│   ├── devices/             # Device-specific configurations (YAML)
│   │   ├── agilent_keysight.yaml
│   │   ├── rigol.yaml
│   │   └── siglent.yaml
│   └── instructionsets/     # Command sets for instruments
│       ├── functiongenerators/
|       |   ├── base_functiongenerator.py
│       |   └── ...
│       └── scopes/
│           ├── base_scope.py
│           └── ...
├── ven/                     # Virtual environment (optional, excluded from version control)
└── Programmingguides/       # Manufacturer documentation for devices
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/DioptasK/Bode-Plot-Pyvisa.git
cd Bode-Plot-Pyvisa
```

Set up a virtual environment:

```bash
python -m venv ven
source ven/bin/activate  # On Windows: ven\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure you have a VISA backend installed (e.g., NI-VISA or `pyvisa-py`).

---

## ▶️ Usage

### Run with GUI:

```bash
python3 main.py -u
```

### Run with CLI options:

```bash
python3 main.py [-options]
```

---

## 🧩 Functional Overview

- **Hardware Tab**: Connect and configure VISA devices.
- **Output Tab**: View measurement results.
- **Settings Tab**: Adjust application behavior and appearance.
- **Exit**: Application ensures all threads are cleanly terminated.

---

## 📦 Dependencies

- Python 3.10+
- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter)
- [`pyvisa`](https://pyvisa.readthedocs.io/)
- [`pyvisa-py`](https://github.com/pyvisa/pyvisa-py) *(optional backend)*

---

## 🙏 Acknowledgments

- **PyVISA** – for enabling communication with instruments
- **CustomTkinter** – for a modern, themable Python GUI

---
