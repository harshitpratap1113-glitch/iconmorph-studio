"""
IconMorph Studio - Modern Cyberpunk / Dark GUI
Author: Harshit Pratap (@harshitpratap1113-glitch)
Allows changing folder/file icons, converting batch scripts to standalone exe, and converting images to multi-res ICO.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk

# Add parent directory to path to import core
sys.path.insert(0, str(Path(__file__).parent.parent))
from core import icon_engine

class IconMorphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IconMorph Studio - Universal Folder & Extension Icon Morph Engine")
        self.geometry("820x680")
        self.minsize(760, 600)
        self.configure(bg="#0F111A")
        
        # Colors
        self.bg_color = "#0F111A"
        self.card_bg = "#1A1D2B"
        self.input_bg = "#0D0E15"
        self.accent_cyan = "#00F0FF"
        self.accent_purple = "#8A2BE2"
        self.accent_green = "#00FF66"
        self.text_color = "#E0E6ED"
        self.text_dim = "#7E8B9B"
        
        self.target_path_var = tk.StringVar()
        self.icon_path_var = tk.StringVar()
        self.extension_var = tk.StringVar(value=".bat")
        self.preview_image = None
        
        self._setup_styles()
        self._build_ui()
        
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure("TLabel", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=self.bg_color, foreground=self.accent_cyan, font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", background=self.bg_color, foreground=self.text_dim, font=("Segoe UI", 9))
        
        style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        
    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self, bg=self.bg_color, pady=12, padx=20)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="⚡ ICONMORPH STUDIO PRO", font=("Segoe UI", 18, "bold"), fg=self.accent_cyan, bg=self.bg_color)
        title_label.pack(anchor="w")
        
        sub_label = tk.Label(header_frame, text="Universal Folder Icon Changer, BAT-to-EXE Compiler & Multi-Resolution ICO Converter", 
                             font=("Segoe UI", 10), fg=self.text_dim, bg=self.bg_color)
        sub_label.pack(anchor="w")
        
        # Main Container
        main_container = tk.Frame(self, bg=self.bg_color, padx=20, pady=5)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Input Card
        input_card = tk.LabelFrame(main_container, text=" 1. TARGET SELECTION ", font=("Segoe UI", 10, "bold"),
                                   bg=self.card_bg, fg=self.accent_cyan, padx=15, pady=12, bd=1, relief="solid")
        input_card.pack(fill=tk.X, pady=6)
        
        # Target Path Row
        target_row = tk.Frame(input_card, bg=self.card_bg)
        target_row.pack(fill=tk.X, pady=4)
        
        tk.Label(target_row, text="Target Folder / File:", font=("Segoe UI", 10), bg=self.card_bg, fg=self.text_color, width=18, anchor="w").pack(side=tk.LEFT)
        target_entry = tk.Entry(target_row, textvariable=self.target_path_var, font=("Consolas", 10), bg=self.input_bg, fg="#00FF66",
                                insertbackground="white", relief="flat", highlightthickness=1, highlightbackground="#2A3045")
        target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, ipady=4)
        
        btn_browse_folder = tk.Button(target_row, text="📁 Browse Folder", font=("Segoe UI", 9, "bold"), bg="#252A3D", fg="white",
                                      relief="flat", activebackground=self.accent_cyan, activeforeground="black", command=self._browse_folder, padx=10)
        btn_browse_folder.pack(side=tk.LEFT, padx=3)
        
        btn_browse_file = tk.Button(target_row, text="📄 Browse File", font=("Segoe UI", 9, "bold"), bg="#252A3D", fg="white",
                                    relief="flat", activebackground=self.accent_cyan, activeforeground="black", command=self._browse_file, padx=10)
        btn_browse_file.pack(side=tk.LEFT, padx=3)
        
        # Icon Input Card
        icon_card = tk.LabelFrame(main_container, text=" 2. CUSTOM ICON SELECTION ", font=("Segoe UI", 10, "bold"),
                                  bg=self.card_bg, fg=self.accent_cyan, padx=15, pady=12, bd=1, relief="solid")
        icon_card.pack(fill=tk.X, pady=6)
        
        icon_row = tk.Frame(icon_card, bg=self.card_bg)
        icon_row.pack(fill=tk.X, pady=4)
        
        tk.Label(icon_row, text="Icon Source (PNG/ICO):", font=("Segoe UI", 10), bg=self.card_bg, fg=self.text_color, width=18, anchor="w").pack(side=tk.LEFT)
        icon_entry = tk.Entry(icon_row, textvariable=self.icon_path_var, font=("Consolas", 10), bg=self.input_bg, fg="#00FF66",
                              insertbackground="white", relief="flat", highlightthickness=1, highlightbackground="#2A3045")
        icon_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, ipady=4)
        
        btn_browse_icon = tk.Button(icon_row, text="🎨 Browse Icon", font=("Segoe UI", 9, "bold"), bg="#252A3D", fg="white",
                                    relief="flat", activebackground=self.accent_cyan, activeforeground="black", command=self._browse_icon, padx=12)
        btn_browse_icon.pack(side=tk.LEFT, padx=3)
        
        # Thumbnail Preview Frame
        preview_row = tk.Frame(icon_card, bg=self.card_bg)
        preview_row.pack(fill=tk.X, pady=4)
        
        self.preview_label = tk.Label(preview_row, text="[No Icon Selected]", font=("Segoe UI", 9, "italic"), bg="#0D0E15", fg=self.text_dim, width=14, height=3)
        self.preview_label.pack(side=tk.LEFT, padx=5)
        
        self.preview_info = tk.Label(preview_row, text="Supports multi-res .ico, .png, .jpg, .webp (auto-converted to crisp 256x256 ICO)", 
                                     font=("Segoe UI", 9), bg=self.card_bg, fg=self.text_dim)
        self.preview_info.pack(side=tk.LEFT, padx=10)
        
        # Actions Card
        actions_card = tk.LabelFrame(main_container, text=" 3. SELECT OPERATION & EXECUTE ", font=("Segoe UI", 10, "bold"),
                                    bg=self.card_bg, fg=self.accent_cyan, padx=15, pady=12, bd=1, relief="solid")
        actions_card.pack(fill=tk.X, pady=6)
        
        btn_grid = tk.Frame(actions_card, bg=self.card_bg)
        btn_grid.pack(fill=tk.X, pady=4)
        
        btn_folder = tk.Button(btn_grid, text="📁 Apply Folder Icon", font=("Segoe UI", 10, "bold"), bg="#008080", fg="white",
                               relief="flat", activebackground=self.accent_cyan, activeforeground="black", command=self._action_set_folder_icon, padx=15, pady=8)
        btn_folder.grid(row=0, column=0, padx=6, pady=4, sticky="ew")
        
        btn_bat_exe = tk.Button(btn_grid, text="⚡ Compile BAT to EXE", font=("Segoe UI", 10, "bold"), bg="#8A2BE2", fg="white",
                                relief="flat", activebackground="#BA55D3", activeforeground="black", command=self._action_compile_bat_exe, padx=15, pady=8)
        btn_bat_exe.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
        
        btn_bat_lnk = tk.Button(btn_grid, text="🔗 Create BAT Shortcut", font=("Segoe UI", 10, "bold"), bg="#2E8B57", fg="white",
                                relief="flat", activebackground="#3CB371", activeforeground="black", command=self._action_create_bat_lnk, padx=15, pady=8)
        btn_bat_lnk.grid(row=0, column=2, padx=6, pady=4, sticky="ew")
        
        btn_img_ico = tk.Button(btn_grid, text="🖼️ Convert Image to .ICO", font=("Segoe UI", 10, "bold"), bg="#4169E1", fg="white",
                                relief="flat", activebackground="#6495ED", activeforeground="black", command=self._action_convert_image_ico, padx=15, pady=8)
        btn_img_ico.grid(row=1, column=0, padx=6, pady=4, sticky="ew")
        
        btn_reset = tk.Button(btn_grid, text="🔄 Reset Folder Icon", font=("Segoe UI", 10, "bold"), bg="#555B6E", fg="white",
                              relief="flat", activebackground="#778899", activeforeground="black", command=self._action_reset_folder_icon, padx=15, pady=8)
        btn_reset.grid(row=1, column=1, padx=6, pady=4, sticky="ew")
        
        btn_refresh = tk.Button(btn_grid, text="✨ Refresh Windows Shell", font=("Segoe UI", 10, "bold"), bg="#252A3D", fg=self.accent_cyan,
                                relief="flat", activebackground=self.accent_cyan, activeforeground="black", command=self._action_refresh_shell, padx=15, pady=8)
        btn_refresh.grid(row=1, column=2, padx=6, pady=4, sticky="ew")
        
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)
        btn_grid.columnconfigure(2, weight=1)
        
        # Activity Console Log
        log_frame = tk.LabelFrame(main_container, text=" 4. EXECUTION CONSOLE ", font=("Segoe UI", 10, "bold"),
                                  bg=self.card_bg, fg=self.accent_cyan, padx=10, pady=8, bd=1, relief="solid")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=6)
        
        self.log_text = tk.Text(log_frame, bg="#08090D", fg="#39FF14", font=("Consolas", 9), relief="flat", wrap=tk.WORD, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log("🚀 IconMorph Studio Engine Loaded. Ready for operations.")
        
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def _browse_folder(self):
        f = filedialog.askdirectory(title="Select Target Folder")
        if f:
            self.target_path_var.set(os.path.normpath(f))
            self.log(f"📁 Selected Folder: {f}")
            
    def _browse_file(self):
        f = filedialog.askopenfilename(title="Select Target File", filetypes=[("All Files", "*.*"), ("Batch Scripts", "*.bat;*.cmd"), ("Shortcuts", "*.lnk")])
        if f:
            self.target_path_var.set(os.path.normpath(f))
            self.log(f"📄 Selected File: {f}")
            
    def _browse_icon(self):
        f = filedialog.askopenfilename(title="Select Icon or Image", filetypes=[("Images & Icons", "*.ico;*.png;*.jpg;*.jpeg;*.webp;*.bmp"), ("Icon Files", "*.ico"), ("PNG Files", "*.png")])
        if f:
            self.icon_path_var.set(os.path.normpath(f))
            self.log(f"🎨 Selected Icon: {f}")
            self._update_icon_preview(f)
            
    def _update_icon_preview(self, icon_path):
        try:
            img = Image.open(icon_path)
            img.thumbnail((48, 48))
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_image, text="", width=48, height=48)
            self.preview_info.configure(text=f"Loaded: {Path(icon_path).name} ({img.size[0]}x{img.size[1]})")
        except Exception as e:
            self.preview_label.configure(image="", text="[Preview Error]")
            self.preview_info.configure(text=f"Preview error: {e}")
            
    def _run_async(self, func):
        threading.Thread(target=func, daemon=True).start()
        
    def _action_set_folder_icon(self):
        folder = self.target_path_var.get().strip()
        icon = self.icon_path_var.get().strip()
        if not folder or not icon:
            messagebox.showwarning("Missing Input", "Please provide both Target Folder and Icon Path.")
            return
            
        def task():
            try:
                self.log(f"[*] Applying custom icon to folder: {folder}...")
                icon_engine.set_folder_icon(folder, icon)
                self.log(f"✅ SUCCESS: Folder icon updated and Windows Shell refreshed!")
                messagebox.showinfo("Success", f"Folder icon successfully applied to:\n{folder}")
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                messagebox.showerror("Operation Failed", str(e))
        self._run_async(task)
        
    def _action_compile_bat_exe(self):
        target = self.target_path_var.get().strip()
        icon = self.icon_path_var.get().strip()
        if not target or not icon:
            messagebox.showwarning("Missing Input", "Please provide Target .BAT file and Icon Path.")
            return
        if not target.lower().endswith((".bat", ".cmd")):
            messagebox.showwarning("Invalid File", "Target must be a .bat or .cmd script for EXE compilation.")
            return
            
        def task():
            try:
                self.log(f"[*] Compiling BAT to standalone EXE with embedded icon...")
                out_exe = icon_engine.compile_bat_to_exe(target, icon)
                self.log(f"✅ SUCCESS: Compiled native executable created:\n{out_exe}")
                messagebox.showinfo("Success", f"Native EXE created successfully:\n{out_exe}")
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                messagebox.showerror("Compilation Failed", str(e))
        self._run_async(task)
        
    def _action_create_bat_lnk(self):
        target = self.target_path_var.get().strip()
        icon = self.icon_path_var.get().strip()
        if not target or not icon:
            messagebox.showwarning("Missing Input", "Please provide Target file and Icon Path.")
            return
            
        def task():
            try:
                self.log(f"[*] Creating launcher shortcut with custom icon...")
                out_lnk = icon_engine.set_bat_icon(target, icon)
                self.log(f"✅ SUCCESS: Shortcut created with custom icon:\n{out_lnk}")
                messagebox.showinfo("Success", f"Shortcut created successfully:\n{out_lnk}")
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                messagebox.showerror("Shortcut Failed", str(e))
        self._run_async(task)
        
    def _action_convert_image_ico(self):
        icon = self.icon_path_var.get().strip()
        if not icon:
            messagebox.showwarning("Missing Input", "Please select an image in Icon Source to convert to .ICO.")
            return
            
        def task():
            try:
                self.log(f"[*] Converting image to multi-resolution Windows .ICO...")
                out_ico = icon_engine.convert_to_ico(icon)
                self.log(f"✅ SUCCESS: Multi-resolution .ICO created at:\n{out_ico}")
                messagebox.showinfo("Success", f"Multi-resolution .ICO generated:\n{out_ico}")
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                messagebox.showerror("Conversion Failed", str(e))
        self._run_async(task)
        
    def _action_reset_folder_icon(self):
        folder = self.target_path_var.get().strip()
        if not folder:
            messagebox.showwarning("Missing Input", "Please select a Target Folder to reset.")
            return
            
        def task():
            try:
                self.log(f"[*] Resetting folder icon to default Windows view...")
                icon_engine.reset_folder_icon(folder)
                self.log(f"✅ SUCCESS: Folder reset to default.")
                messagebox.showinfo("Success", f"Folder reset to standard Windows icon:\n{folder}")
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                messagebox.showerror("Reset Failed", str(e))
        self._run_async(task)
        
    def _action_refresh_shell(self):
        self.log("[*] Forcing Windows Explorer to reload all icon caches...")
        icon_engine.refresh_shell()
        self.log("✅ Shell notification dispatched.")

if __name__ == "__main__":
    app = IconMorphApp()
    app.mainloop()
