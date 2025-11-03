import os
import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk

PAGES_DIR = "pages"
DIAGRAM_IMAGE = "diagram.png"
PETA_IMAGE = "peta.jpg"

TEXT_FILES = {
    "abstrak": "abstrak.txt",
    "masalah": "latar_masalah.txt",
    "signifikansi": "latar_signifikansi.txt",
    "desain": "desain_overview.txt",
    "chassis organism": "desain_chassis.txt",
    "vektor ekspresi": "konstruksi_vektor_ekspresi.txt",
    "gen target yang digunakan": "konstruksi_gen_target.txt",
    "komponen regulator": "konstruksi_komponen_regulator.txt",
    "kontrol ekspresi gen": "desain_kontrol_ekspresi.txt",
    "langkah-langkah konstruksi plasmid": "hasil_langkah_konstruksi.txt",
    "seleksi koloni bakteri": "hasil_seleksi_koloni.txt",
    "eksperimen lanjutan": "future_eksperimen_lanjutan.txt",
    "aplikasi potensial": "future_aplikasi_potensial.txt",
}

def load_text_file(filename: str) -> str:
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _resolve_image(path):
    if path is None:
        return None
    return path if os.path.exists(path) else None

def _load_and_resize_photo(path, max_width):
    img = Image.open(path)
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

class TextPage(tk.Frame):
    def __init__(self, parent, key, title, text, header_font, body_font, image_top=None, image_bottom=None, controller=None):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.key = key
        self.header_font = header_font
        self.body_font = body_font

        self.image_top = _resolve_image(image_top) if image_top else None
        self.image_bottom = _resolve_image(image_bottom) if image_bottom else None
        self._photo_refs = []

        self.column = tk.Frame(self, bg="#d9ffe3")
        self.column.place(relx=0.5, rely=0.025, anchor="n", width=900, height=640)

        tk.Label(self.column, text=title.title(), font=header_font, bg="#d9ffe3").pack(pady=(12, 8))

        if key == "langkah-langkah konstruksi plasmid":
            content_side = tk.Frame(self.column, bg="#d9ffe3")
            content_side.pack(fill="both", expand=True, padx=12, pady=(6, 12))

            left_col = tk.Frame(content_side, width=360, bg="#d9ffe3")
            left_col.pack(side="left", fill="y", padx=(0, 12))
            left_col.pack_propagate(False)

            left_img_label = tk.Label(left_col, bg="#d9ffe3")
            left_img_label.pack(anchor="n", pady=(0, 8))

            if self.image_top:
                try:
                    photo = _load_and_resize_photo(self.image_top, max_width=360)
                    self._photo_refs.append(photo)
                    left_img_label.config(image=photo)
                except Exception as e:
                    left_img_label.config(text=f"[error diagram: {e}]")
            else:
                left_img_label.config(text="[diagram error]")

            right_col = tk.Frame(content_side, bg="#d9ffe3")
            right_col.pack(side="left", fill="both", expand=True)
            self.text_widget = tk.Text(
                right_col, font=body_font, bg="#d9ffe3", fg="black",
                wrap="word", spacing1=4, spacing3=8, relief="flat"
            )
            self.text_widget.insert("1.0", text)
            self.text_widget.config(state="disabled")
            self.text_widget.pack(fill="both", expand=True, padx=(0,8), pady=(0,8))

        else:
            self.text_widget = tk.Text(
                self.column, font=body_font, bg="#d9ffe3", fg="black",
                wrap="word", spacing1=4, spacing3=8, relief="flat"
            )
            self.text_widget.configure(state="normal")
            self.text_widget.insert("1.0", text)
            if self.image_bottom:
                try:
                    photo = _load_and_resize_photo(self.image_bottom, max_width=560)
                    self._photo_refs.append(photo)
                    self.text_widget.insert("end", "\n\n")
                    self.text_widget.image_create("end", image=photo)
                except Exception as e:
                    self.text_widget.insert("end", f"\n\n[error bottom image: {e}]\n")
            self.text_widget.configure(state="disabled")
            self.text_widget.pack(fill="both", expand=True, padx=30, pady=(10, 40))

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50", width=220)
        self.controller = controller

        self._add_button("abstrak")
        self._add_section("LATAR BELAKANG")
        self._add_button("masalah", 1)
        self._add_button("signifikansi", 1)

        self._add_section("DESAIN")
        self._add_button("desain", 1)
        self._add_button("chassis organism", 1)
        self._add_section("KONSTRUKSI PLASMID REKOMBINAN")
        self._add_button("vektor ekspresi", 2)
        self._add_button("gen target yang digunakan", 2)
        self._add_button("komponen regulator", 2)
        self._add_button("kontrol ekspresi gen", 1)

        self._add_section("HASIL")
        self._add_button("langkah-langkah konstruksi plasmid", 1)
        self._add_button("seleksi koloni bakteri", 1)

        self._add_section("FUTURE WORK")
        self._add_button("eksperimen lanjutan", 1)
        self._add_button("aplikasi potensial", 1)

    def _add_section(self, title):
        lbl = tk.Label(self, text=title, bg="#2c3e50", fg="white",
                       font=("Calibri", 13, "bold"), anchor="w", padx=10)
        lbl.pack(fill="x", pady=(10, 0))

    def _add_button(self, text, indent=0):
        pad = 10 + indent * 12
        btn = tk.Button(self, text=text.title(), bg="#34495e", fg="white",
                        font=("DengXian Light", 12, "bold"), bd=0, relief="flat",
                        anchor="w", padx=pad,
                        command=lambda k=text.lower(): self.controller.show_page(k))
        btn.pack(fill="x", pady=2)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BIOS 2025")
        self.state("zoomed")

        self.header_font = font.Font(family="Calibri", size=24, weight="bold")
        self.body_font = font.Font(family="DengXian Light", size=14)

        self.topbar = tk.Frame(self, bg="#34495e", height=48)
        self.topbar.pack(side="top", fill="x")
        tk.Button(self.topbar, text="☰", bg="#34495e", fg="white",
                  font=("Arial", 16, "bold"), bd=0, command=self.toggle_sidebar).pack(side="left", padx=10, pady=6)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.sidebar = Sidebar(self.container, self)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.container, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        self.pages = {}
        self.load_pages()
        self.show_page("abstrak")

    def toggle_sidebar(self):
        if self.sidebar.winfo_ismapped():
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side="left", fill="y")

    def load_pages(self):
        resolved_diagram = _resolve_image(DIAGRAM_IMAGE)
        resolved_peta = _resolve_image(PETA_IMAGE)

        for key, fname in TEXT_FILES.items():
            text = load_text_file(fname)
            image_top = resolved_diagram if key == "langkah-langkah konstruksi plasmid" else None
            image_bottom = resolved_peta if key == "vektor ekspresi" else None

            page = TextPage(self.content, key, key, text, self.header_font, self.body_font,
                            image_top=image_top, image_bottom=image_bottom, controller=self)
            page.place(relwidth=1, relheight=1)
            self.pages[key.lower()] = page

    def show_page(self, key):
        key = key.lower()
        if key not in self.pages:
            messagebox.showerror("Missing", f"page error: {key}")
            return
        self.pages[key].lift()

if __name__ == "__main__":
    app = App()
    app.mainloop()