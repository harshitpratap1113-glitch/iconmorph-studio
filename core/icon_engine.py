"""
IconMorph Pro - Core Icon Engine
Handles multi-resolution ICO conversion, desktop.ini manipulation,
shortcut/BAT/EXE wrapping, extension icon registry injection, and instant Windows Explorer reload.
"""

import os
import sys
import shutil
import ctypes
import subprocess
from pathlib import Path
from PIL import Image

def refresh_shell():
    """Notifies Windows Explorer to reload all icons immediately without restarting Explorer."""
    try:
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_FLUSH = 0x1000
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, 0, 0)
        return True
    except Exception as e:
        print(f"Shell refresh error: {e}")
        return False

def convert_to_ico(input_path, output_path=None):
    """
    Converts any PNG, JPG, WEBP, or BMP image into a crisp,
    multi-resolution Windows .ico file with all standard sizes.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    if output_path is None:
        output_path = input_file.with_suffix(".ico")
    else:
        output_path = Path(output_path)
        
    img = Image.open(input_file)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(str(output_path), format="ICO", sizes=sizes)
    return str(output_path)

def set_folder_icon(folder_path, icon_path):
    """
    Applies a custom icon to any Windows folder.
    Creates desktop.ini, sets Read-Only flag on folder, and triggers instant shell refresh.
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {folder_path}")
        
    icon_src = Path(icon_path)
    if not icon_src.exists():
        raise FileNotFoundError(f"Icon file not found: {icon_path}")
        
    dest_ico = folder / "folder_icon.ico"
    dest_ini = folder / "desktop.ini"
    
    # Unhide existing files if present
    if dest_ini.exists():
        subprocess.run(["attrib", "-h", "-s", str(dest_ini)], capture_output=True)
    if dest_ico.exists():
        subprocess.run(["attrib", "-h", "-s", str(dest_ico)], capture_output=True)
        
    # Convert image to ICO if not already an ICO
    if icon_src.suffix.lower() != ".ico":
        convert_to_ico(str(icon_src), str(dest_ico))
    else:
        shutil.copy2(str(icon_src), str(dest_ico))
        
    # Generate desktop.ini
    ini_content = (
        "[.ShellClassInfo]\n"
        f"IconResource={str(dest_ico)},0\n"
        "[ViewState]\n"
        "Mode=\n"
        "Vid=\n"
        "FolderType=Generic\n"
    )
    with open(dest_ini, "w", encoding="ansi") as f:
        f.write(ini_content)
        
    # Apply Windows system attributes
    subprocess.run(["attrib", "+h", "+s", str(dest_ini)], capture_output=True)
    subprocess.run(["attrib", "+h", "+s", str(dest_ico)], capture_output=True)
    subprocess.run(["attrib", "+r", str(folder)], capture_output=True)
    
    refresh_shell()
    return True

def reset_folder_icon(folder_path):
    """Resets a folder back to the default Windows folder icon."""
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {folder_path}")
        
    dest_ico = folder / "folder_icon.ico"
    dest_ini = folder / "desktop.ini"
    
    if dest_ini.exists():
        subprocess.run(["attrib", "-h", "-s", str(dest_ini)], capture_output=True)
        dest_ini.unlink()
    if dest_ico.exists():
        subprocess.run(["attrib", "-h", "-s", str(dest_ico)], capture_output=True)
        dest_ico.unlink()
        
    subprocess.run(["attrib", "-r", str(folder)], capture_output=True)
    refresh_shell()
    return True

def set_shortcut_icon(shortcut_path, icon_path):
    """Changes the icon of any Windows shortcut (.lnk)."""
    lnk = Path(shortcut_path)
    if not lnk.exists():
        raise FileNotFoundError(f"Shortcut not found: {shortcut_path}")
        
    icon_src = Path(icon_path)
    if not icon_src.exists():
        raise FileNotFoundError(f"Icon not found: {icon_path}")
        
    # Ensure icon is ICO
    final_ico = icon_src
    if icon_src.suffix.lower() != ".ico":
        final_ico = icon_src.with_suffix(".ico")
        convert_to_ico(str(icon_src), str(final_ico))
        
    ps_cmd = (
        f"$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{str(lnk)}'); "
        f"$s.IconLocation = '{str(final_ico)},0'; "
        f"$s.Save()"
    )
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to update shortcut icon: {res.stderr}")
        
    refresh_shell()
    return True

def set_bat_icon(bat_path, icon_path, output_lnk_path=None):
    """
    Creates a customized launcher shortcut (.lnk) for any .bat or .cmd script
    with the specified custom icon attached.
    """
    bat = Path(bat_path)
    if not bat.exists():
        raise FileNotFoundError(f"Batch file not found: {bat_path}")
        
    icon_src = Path(icon_path)
    final_ico = icon_src
    if icon_src.suffix.lower() != ".ico":
        final_ico = icon_src.with_suffix(".ico")
        convert_to_ico(str(icon_src), str(final_ico))
        
    if output_lnk_path is None:
        output_lnk = bat.with_suffix(".lnk")
    else:
        output_lnk = Path(output_lnk_path)
        
    ps_cmd = (
        f"$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{str(output_lnk)}'); "
        f"$s.TargetPath = '{str(bat)}'; "
        f"$s.WorkingDirectory = '{str(bat.parent)}'; "
        f"$s.IconLocation = '{str(final_ico)},0'; "
        f"$s.Save()"
    )
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to create bat launcher: {res.stderr}")
        
    refresh_shell()
    return str(output_lnk)

def compile_bat_to_exe(bat_path, icon_path, output_exe_path=None):
    """
    Compiles any .bat script into a standalone native Windows .exe
    with the custom icon compiled directly into the binary resource table.
    Uses native Windows C# Roslyn compiler without needing third-party tools.
    """
    bat = Path(bat_path)
    if not bat.exists():
        raise FileNotFoundError(f"Batch script not found: {bat_path}")
        
    final_ico = Path(icon_path)
    if final_ico.suffix.lower() != ".ico":
        final_ico = final_ico.with_suffix(".ico")
        convert_to_ico(str(icon_path), str(final_ico))
        
    if output_exe_path is None:
        output_exe = bat.with_suffix(".exe")
    else:
        output_exe = Path(output_exe_path)
        
    # Read batch content and encode to avoid string escaping issues
    with open(bat, "rb") as f:
        bat_bytes = f.read()
    import base64
    b64_content = base64.b64encode(bat_bytes).decode("ascii")
    
    # C# wrapper source code
    csharp_source = f"""
using System;
using System.IO;
using System.Diagnostics;
using System.Text;

class Program {{
    static void Main(string[] args) {{
        string tempBat = Path.Combine(Path.GetTempPath(), "run_" + Guid.NewGuid().ToString("N") + ".bat");
        byte[] bytes = Convert.FromBase64String("{b64_content}");
        File.WriteAllBytes(tempBat, bytes);
        
        string passArgs = string.Join(" ", args);
        ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c \\"" + tempBat + "\\" " + passArgs);
        psi.WorkingDirectory = Directory.GetCurrentDirectory();
        psi.UseShellExecute = false;
        
        try {{
            Process p = Process.Start(psi);
            p.WaitForExit();
        }} finally {{
            if (File.Exists(tempBat)) {{
                try {{ File.Delete(tempBat); }} catch {{}}
            }}
        }}
    }}
}}
"""
    temp_cs = bat.parent / f"_temp_compile_{bat.stem}.cs"
    with open(temp_cs, "w", encoding="utf-8") as f:
        f.write(csharp_source)
        
    # Find CSC compiler
    framework_dirs = [
        r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
        r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
    ]
    csc_exe = None
    for d in framework_dirs:
        if os.path.exists(d):
            csc_exe = d
            break
            
    if not csc_exe:
        if temp_cs.exists():
            temp_cs.unlink()
        raise RuntimeError("Windows .NET C# compiler (csc.exe) not found on system.")
        
    compile_cmd = [
        csc_exe,
        "/nologo",
        "/target:exe",
        f"/win32icon:{str(final_ico)}",
        f"/out:{str(output_exe)}",
        str(temp_cs)
    ]
    
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    if temp_cs.exists():
        temp_cs.unlink()
        
    if res.returncode != 0:
        raise RuntimeError(f"Compilation failed: {res.stderr}\n{res.stdout}")
        
    refresh_shell()
    return str(output_exe)

def apply_extension_default_icon(extension, icon_path):
    """
    Sets the Windows Explorer default icon for any file extension (e.g. '.mypkg', '.custom').
    Injects into HKCU\\Software\\Classes.
    """
    ext = extension.strip()
    if not ext.startswith("."):
        ext = "." + ext
        
    final_ico = Path(icon_path)
    if final_ico.suffix.lower() != ".ico":
        final_ico = final_ico.with_suffix(".ico")
        convert_to_ico(str(icon_path), str(final_ico))
        
    prog_id = f"IconMorph_{ext.lstrip('.')}_file"
    
    import winreg
    try:
        # 1. Map extension to ProgID
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{ext}") as k:
            winreg.SetValue(k, "", winreg.REG_SZ, prog_id)
            
        # 2. Set ProgID DefaultIcon
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{prog_id}\DefaultIcon") as k:
            winreg.SetValue(k, "", winreg.REG_SZ, f"{str(final_ico)},0")
            
        refresh_shell()
        return True
    except Exception as e:
        raise RuntimeError(f"Registry operation failed: {e}")
