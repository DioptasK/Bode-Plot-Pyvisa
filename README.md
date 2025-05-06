# PyVISA GUI Application

A modern GUI application for communicating with measurement instruments such as oscilloscopes and function generators — built with Python, [PyVISA](https://pyvisa.readthedocs.io/), and [customtkinter](https://customtkinter.tomschimansky.com/).

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
├── requirements.txt         # 
├── UI/                      # GUI components (customtkinter)
│   ├── device_input.py      # Hardware configuration
│   ├── mainframe.py         # Main window
│   ├── settings.py          # Measurement settings
│   └── terminal.py          # Terminal output
├── visa_py/                 # PyVISA-related modules
│   ├── inputs_check.py      # Input validation
│   ├── resources.py         # Resource management
│   ├── devices/             # Device-specific configurations (YAML)
│   │   ├── agilent_keysight.yaml
│   │   ├── rigol.yaml
│   │   └── siglent.yaml
│   └── instructionsets/     # Command sets for instruments
│       ├── functiongenerators/
│       |   ├── base_functiongenerator.py
│       |   └── ...
│       └── scopes/
│           ├── base_scope.py
│           └── ...
├── outputs/                 # Data outputs and exports
│   ├── export_output.py     # Export data to files
│   └── plot_output.py       # Plot the data
└── Programmingguides/       # Manufacturer documentation for devices
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/DioptasK/Bode-Plot-Pyvisa.git
```
```bash
cd Bode-Plot-Pyvisa
```

Set up a virtual environment:

```bash
python -m venv ven
```
```bash
source ven/bin/activate  # On Windows: ven\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

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

- **Hardware**: Connect and configure VISA devices.
- **Settings**: Adjust application behavior.

---

## 📦 Dependencies

- Python 3.10+
- [`customtkinter`](https://github.com/TomSchimansky/CustomTkinter)
- [`pyvisa`](https://pyvisa.readthedocs.io/)
- [`pyvisa-py`](https://github.com/pyvisa/pyvisa-py) *(optional backend)*

---

## Acknowledgments

- **PyVISA** – for enabling communication with instruments
- **CustomTkinter** – for a modern, themable Python GUI

---

## License

Copyright (c) 2025 Bode-Plot-Pyvisa

This software is provided free of charge for **non-commercial purposes** only.

You are permitted to:
- use the software for personal, educational, or academic purposes,
- modify, copy, and distribute the source code,
- include it in open-source projects, **as long as no commercial intent is involved**.

You are **not permitted** to:
- use the software for any commercial purpose, including but not limited to:
  - incorporating it into paid products or services,
  - using it in commercial platforms or client work,
  - selling or licensing the software or any derivative works.

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to fitness for a particular purpose.

---