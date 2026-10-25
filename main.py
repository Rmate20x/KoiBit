import os
import sys
import json
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# --- Erőforrások elérésének kezelése (PyInstaller .exe miatt) ---
def get_resource_path(relative_path):
    """Visszaadja a fájl abszolút útvonalát, akár sima scriptként, akár .exe-ként fut."""
    try:
        # A PyInstaller ide csomagolja ki a fájlokat futáskor
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Betűtípus ideiglenes betöltése memóriába (Csak Windows) ---
def load_custom_font(font_path):
    if os.name == 'nt' and os.path.exists(font_path):
        FR_PRIVATE = 0x10
        ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

# Csomagolt betűtípus betöltése
font_file = get_resource_path("pixel_operator.ttf")
load_custom_font(font_file)

# --- Load / Create Theme ---
THEME_FILE = "theme.json"

DEFAULT_THEME = {
    "bg_color": "#1e1e1e",           
    "fg_color": "#d4d4d4",           
    "entry_bg": "#3c3c3c",           
    "entry_fg": "#ffffff",           
    "btn_bg": "#ac3232",             
    "btn_fg": "#ffffff",             
    "btn_active_bg": "#ac3232",      
    "font_family": "Pixel Operator 8", 
    "font_size": 10                  
}

def load_theme():
    if not os.path.exists(THEME_FILE):
        with open(THEME_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_THEME, f, indent=4)
        return DEFAULT_THEME
    try:
        with open(THEME_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_THEME

theme = load_theme()
font_main = (theme["font_family"], theme["font_size"])
font_bold = (theme["font_family"], theme["font_size"], "bold")

# --- Core Functions ---
def is_empty(image):
    if image.getbbox() is None:
        return True
    extrema = image.getextrema()
    if extrema:
        if isinstance(extrema[0], int):
            return extrema[0] == extrema[1]
        else:
            for band_min, band_max in extrema:
                if band_min != band_max:
                    return False
            return True
    return False

def select_image():
    file_path = filedialog.askopenfilename(
        title="Select a Sprite Sheet",
        filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*"))
    )
    if file_path:
        image_path_var.set(file_path)

def select_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_folder_var.set(folder)

def split_sprites():
    image_path = image_path_var.get()
    output_folder = output_folder_var.get()
    prefix = prefix_var.get().strip()
    
    if not prefix:
        prefix = "sprite"
        
    if not image_path:
        messagebox.showwarning("Warning", "Please select a source image!")
        return
        
    if not output_folder:
        original_dir = os.path.dirname(image_path)
        output_folder = os.path.join(original_dir, "extracted_sprites")

    try:
        tile_width = int(width_var.get())
        tile_height = int(height_var.get())
    except ValueError:
        messagebox.showerror("Error", "Width and height must be valid numbers!")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        img = Image.open(image_path).convert("RGBA")
        img_width, img_height = img.size
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image:\n{e}")
        return

    cols = img_width // tile_width
    rows = img_height // tile_height
    
    saved_count = 0
    skipped_count = 0

    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            top = row * tile_height
            right = left + tile_width
            bottom = top + tile_height

            tile = img.crop((left, top, right, bottom))
            
            if skip_empty_var.get() and is_empty(tile):
                skipped_count += 1
                continue

            filename = f"{prefix}_{saved_count:03d}.png"
            output_path = os.path.join(output_folder, filename)
            
            tile.save(output_path, "PNG")
            saved_count += 1

    message = f"Done!\n\nSaved sprites: {saved_count}\n"
    if skip_empty_var.get():
        message += f"Skipped empty tiles: {skipped_count}\n"
    message += f"\nSaved to:\n{output_folder}"

    messagebox.showinfo("Finished", message)

# --- GUI Setup ---
root = tk.Tk()
root.title("KoiBit")
root.geometry("550x380")
root.resizable(False, False)
root.configure(bg=theme["bg_color"])

try:
    # A get_resource_path biztosítja, hogy a PyInstaller temp mappájából is megtalálja az ikont
    icon_path = get_resource_path("icon.ico")
    root.iconbitmap(icon_path)
    
    # Windows tálca ikon megjelenítési hibák elkerüléséhez:
    if os.name == 'nt':
        myappid = 'koibit.app.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass # Ha nincs meg a képfájl, a program nem omlik össze, csak az alap ikont használja

# Variables
image_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
width_var = tk.StringVar(value="32")
height_var = tk.StringVar(value="32")
prefix_var = tk.StringVar(value="sprite")
skip_empty_var = tk.BooleanVar(value=True)

def create_label(parent, text):
    return tk.Label(parent, text=text, bg=theme["bg_color"], fg=theme["fg_color"], font=font_main)

def create_entry(parent, var, width=None):
    ent = tk.Entry(parent, textvariable=var, bg=theme["entry_bg"], fg=theme["entry_fg"], 
                   font=font_main, relief="flat", insertbackground=theme["fg_color"])
    if width:
        ent.config(width=width)
    return ent

def create_button(parent, text, command, bold=False):
    fnt = font_bold if bold else font_main
    return tk.Button(parent, text=text, command=command, bg=theme["btn_bg"], fg=theme["btn_fg"], 
                     activebackground=theme["btn_active_bg"], activeforeground=theme["btn_fg"],
                     font=fnt, relief="flat", cursor="hand2", padx=10, pady=3)

main_frame = tk.Frame(root, bg=theme["bg_color"])
main_frame.pack(fill="both", expand=True, padx=20, pady=15)
main_frame.columnconfigure(0, weight=0, minsize=110)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=0, minsize=100)

create_label(main_frame, "Source Image:").grid(row=0, column=0, sticky="e", pady=10)
entry_image = create_entry(main_frame, image_path_var)
entry_image.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
entry_image.configure(state="readonly", readonlybackground=theme["entry_bg"])
create_button(main_frame, "Browse...", select_image).grid(row=0, column=2, sticky="w", pady=10)

create_label(main_frame, "Size (W x H):").grid(row=1, column=0, sticky="e", pady=10)
size_frame = tk.Frame(main_frame, bg=theme["bg_color"])
size_frame.grid(row=1, column=1, sticky="w", padx=10, pady=10)
create_entry(size_frame, width_var, width=8).pack(side="left")
create_label(size_frame, " x ").pack(side="left", padx=5)
create_entry(size_frame, height_var, width=8).pack(side="left")
create_label(size_frame, " px").pack(side="left", padx=5)

create_label(main_frame, "Output Folder:").grid(row=2, column=0, sticky="e", pady=10)
entry_folder = create_entry(main_frame, output_folder_var)
entry_folder.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
entry_folder.configure(state="readonly", readonlybackground=theme["entry_bg"])
create_button(main_frame, "Browse...", select_folder).grid(row=2, column=2, sticky="w", pady=10)

create_label(main_frame, "File Prefix:").grid(row=3, column=0, sticky="e", pady=10)
create_entry(main_frame, prefix_var).grid(row=3, column=1, sticky="ew", padx=10, pady=10)
create_label(main_frame, "(e.g., 'player')").grid(row=3, column=2, sticky="w", pady=10)

chk_empty = tk.Checkbutton(
    main_frame, text="Skip empty (transparent/solid) sprites", variable=skip_empty_var,
    bg=theme["bg_color"], fg=theme["fg_color"], selectcolor=theme["entry_bg"],
    activebackground=theme["bg_color"], activeforeground=theme["fg_color"], font=font_main
)
chk_empty.grid(row=4, column=0, columnspan=3, pady=15)

btn_start = create_button(main_frame, "Start Splitting", split_sprites, bold=True)
btn_start.grid(row=5, column=0, columnspan=3, pady=5, ipadx=15, ipady=3)

root.mainloop()