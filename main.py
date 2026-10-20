#!/usr/bin/env python3
"""
IconMorph Studio - Universal Icon Morph & Customization CLI / GUI Engine
Author: Harshit Pratap (@harshitpratap1113-glitch)
GitHub: https://github.com/harshitpratap1113-glitch/iconmorph-studio
"""

import sys
import argparse
from pathlib import Path
from core import icon_engine

def main():
    parser = argparse.ArgumentParser(
        description="IconMorph Studio - Universal Folder Icon Changer & BAT-to-EXE Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch GUI Studio:
  python main.py

  # Apply Custom Icon to Folder:
  python main.py --folder "C:\\Projects\\MyFolder" --icon "C:\\Assets\\logo.png"

  # Compile BAT script to standalone EXE with embedded icon:
  python main.py --compile-bat "C:\\Tools\\run.bat" --icon "C:\\Assets\\logo.png"

  # Convert Image to Multi-Resolution Windows ICO:
  python main.py --convert-image "C:\\Assets\\logo.png"

  # Reset Folder Icon to Windows Default:
  python main.py --reset-folder "C:\\Projects\\MyFolder"
        """
    )
    
    parser.add_argument("--folder", help="Target folder path to apply icon to")
    parser.add_argument("--icon", help="Icon image path (.ico, .png, .jpg, .webp)")
    parser.add_argument("--compile-bat", help="Compile a .bat script to a standalone native .exe with embedded icon")
    parser.add_argument("--create-shortcut", help="Create a .lnk shortcut with custom icon for a file")
    parser.add_argument("--convert-image", help="Convert an image file to multi-resolution Windows .ico")
    parser.add_argument("--reset-folder", help="Reset a folder back to Windows default icon")
    parser.add_argument("--refresh-shell", action="store_true", help="Force Windows Explorer to refresh its icon cache")
    parser.add_argument("--cli", action="store_true", help="Force CLI mode even if no operation args provided")

    # If no arguments provided, launch the GUI
    if len(sys.argv) == 1:
        from gui.app import IconMorphApp
        app = IconMorphApp()
        app.mainloop()
        return

    args = parser.parse_args()

    if args.refresh_shell:
        print("[*] Refreshing Windows Explorer shell icon cache...")
        icon_engine.refresh_shell()
        print("[OK] Windows Shell refreshed.")

    if args.convert_image:
        print(f"[*] Converting {args.convert_image} to multi-resolution ICO...")
        out = icon_engine.convert_to_ico(args.convert_image)
        print(f"[SUCCESS] Created: {out}")

    if args.folder and args.icon:
        print(f"[*] Applying icon {args.icon} to folder {args.folder}...")
        icon_engine.set_folder_icon(args.folder, args.icon)
        print(f"[SUCCESS] Folder icon successfully updated!")

    if args.reset_folder:
        print(f"[*] Resetting folder icon for {args.reset_folder}...")
        icon_engine.reset_folder_icon(args.reset_folder)
        print(f"[SUCCESS] Folder icon reset to default.")

    if args.compile_bat:
        if not args.icon:
            print("[ERROR] Please provide --icon along with --compile-bat.")
            sys.exit(1)
        print(f"[*] Compiling {args.compile_bat} to standalone EXE with icon {args.icon}...")
        out = icon_engine.compile_bat_to_exe(args.compile_bat, args.icon)
        print(f"[SUCCESS] Native executable compiled: {out}")

    if args.create_shortcut:
        if not args.icon:
            print("[ERROR] Please provide --icon along with --create-shortcut.")
            sys.exit(1)
        print(f"[*] Creating customized shortcut for {args.create_shortcut}...")
        out = icon_engine.set_bat_icon(args.create_shortcut, args.icon)
        print(f"[SUCCESS] Shortcut created: {out}")

if __name__ == "__main__":
    main()
