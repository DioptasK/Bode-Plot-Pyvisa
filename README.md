# PyVISA GUI Application

A modern GUI application for communicating with measurement instruments such as oscilloscopes and function generators — built with Python, [PyVISA](https://pyvisa.readthedocs.io/) and [customtkinter](https://customtkinter.tomschimansky.com/).

---

## 🔧 Features

- **Device Detection** – finds and configures connected VISA devices.
- **Data Plot in Display** – visual representation of measurement results.
- **Settings Management** – GUI for application settings.
- **Integrated Terminal** – embedded console output.

---

## 📁 Project Structure

```
pyvisa/
├── main.py                  # Entry point of the application
├── requirements.txt          
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

### Run with CLI options:

```bash
python3 main.py [-options]
```

### Run with GUI:

```bash
python3 main.py -u
```

## Device Setup

### Enter Device IDs Manually
You can directly enter the VISA ID of your oscilloscope and/or function generator in the respective fields `Scope` and `Signagenerator`.

### Find Connected Devices
Alternatively, click the **"Get Devices"** button to scan for connected instruments.  
⚠️ Make sure your user account has access to the corresponding interface (e.g., USB, Ethernet, etc.).
**For USB devices**, you can check and adjust access permissions using:

```bash
lsusb
sudo chmod 666 /dev/bus/usb/003/019
```
> Replace `003` and `019` with the bus and device numbers from the `lsusb` output.

### Function Generator via Scope
If your scope has a built-in function generator, you may only need to enter the scope’s ID.  
The program will automatically use the internal generator if available.

### Select Manufacturer
⚠️ Choose the instrument manufacturer.  
**Default:** `Siglent`.

### Set Probe Attenuation
Adjust the probe attenuation according to your probe setup.  
**Default:** `10x`.

---

## Measurement Setup

### Sweep Type
- `"lin"`: Linear sweep – divides the frequency range into equal steps.  
- `"exp"`: Exponential sweep – steps grow exponentially over the range.

### Samples
Set the number of measurement points across the entire frequency range.

---

## Run the Measurement

1. Click **"Check"** to validate all input parameters.
2. If validation passes, click **"Start"** to begin the measurement.
3. Results will be:
   - Printed in the terminal.
   - Plotted in a new window after the sweep is completed.

---

## Exporting Results

After the measurement is complete, click **"Export CSV"** to save the results as a `.csv` file.


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
