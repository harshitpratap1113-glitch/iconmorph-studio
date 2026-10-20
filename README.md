# ⚡ IconMorph Studio Pro

> **Universal Windows Folder Icon Customizer, BAT-to-EXE Compiler & Multi-Resolution ICO Morph Engine.**  
> Built with Python, Tkinter, Pillow, and Native Windows Roslyn (`csc.exe`).  
> **Author:** [Harshit Pratap (@harshitpratap1113-glitch)](https://github.com/harshitpratap1113-glitch)

---

## 🌟 Features

* 📁 **1-Click Folder Icon Transformation:** Apply any PNG, JPG, or ICO to any Windows folder. Automatically generates and injects `desktop.ini`, applies Windows system attributes (`attrib +r`, `attrib +h +s`), and dispatches instant shell refresh notifications without needing to restart Windows Explorer.
* ⚡ **Native BAT-to-EXE Compiler:** Compiles any `.bat` or `.cmd` script into a native standalone Windows `.exe` executable with the specified custom icon compiled directly into the binary's Win32 PE resource table.
* 🔗 **Custom BAT Launcher Shortcuts:** Instantly generates `.lnk` shortcuts with custom visual icons linked to batch files.
* 🖼️ **Multi-Resolution ICO Converter:** Automatically converts standard raster images (PNG, WEBP, JPEG) into multi-layered Windows `.ico` files containing all standard dimensions (`256x256`, `128x128`, `64x64`, `48x48`, `32x32`, `16x16`).
* 🎨 **File Extension Icon Association:** Assign default visual icons to file extensions directly in `HKCU\Software\Classes`.
* 🔄 **Instant Windows Shell Refresh:** Flushes the icon cache and triggers `SHChangeNotify` (`SHCNE_ASSOCCHANGED`) so icons show up immediately.
* 🖥️ **Dual Interface:** Modern Dark Cyberpunk GUI Studio + Full-Featured Command Line Interface (CLI).

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/harshitpratap1113-glitch/iconmorph-studio.git
cd iconmorph-studio
pip install -r requirements.txt
```

### 2. Launch GUI Studio
Double-click `LAUNCH_ICONMORPH_STUDIO.bat` or run:
```bash
python main.py
```

### 3. Command Line Interface (CLI) Usage

#### Apply Custom Icon to a Folder:
```bash
python main.py --folder "C:\MyFolder" --icon "C:\Assets\logo.png"
```

#### Compile .BAT to Native .EXE with Custom Icon:
```bash
python main.py --compile-bat "C:\Scripts\run.bat" --icon "C:\Assets\logo.png"
```

#### Convert Image to Multi-Resolution .ICO:
```bash
python main.py --convert-image "C:\Assets\logo.png"
```

#### Reset Folder to Windows Default Icon:
```bash
python main.py --reset-folder "C:\MyFolder"
```

#### Force Shell Icon Refresh:
```bash
python main.py --refresh-shell
```

---

## 🛠️ Architecture & Under the Hood

* **`core/icon_engine.py`**: Handles low-level Windows API bindings (`ctypes.windll.shell32.SHChangeNotify`), `.ini` file generation, registry manipulation, and `.NET Framework` Roslyn compilation.
* **`gui/app.py`**: Asynchronous Tkinter UI featuring high-contrast dark theme, image preview thumbnailing, file dialogs, and real-time execution log.
* **`main.py`**: Dual-mode entry point automatically switching between GUI and CLI based on arguments.

---

## 📜 License
MIT License. Open source and free for personal and commercial automation.
