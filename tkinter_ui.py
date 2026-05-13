import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
import os

# ── Theme ─────────────────────────────────────────────────────────────────────
BG       = "#0f1117"
BG2      = "#1e2130"
ACCENT   = "#00d4aa"
FG       = "#cdd6f4"
FG_DIM   = "#6c7086"
ERR      = "#f38ba8"
FONT     = ("Courier New", 11)
FONT_BIG = ("Courier New", 14, "bold")
FONT_SM  = ("Courier New", 9)


class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🗂️ File Manager")
        self.geometry("900x620")
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build_ui()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Left sidebar
        sidebar = tk.Frame(self, bg=BG2, width=220)
        sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="FILE MANAGER", bg=BG2, fg=ACCENT,
                 font=FONT_BIG).pack(pady=(20, 5))
        tk.Label(sidebar, text="─" * 22, bg=BG2, fg=FG_DIM,
                 font=FONT_SM).pack()

        self.ops = [
            ("📋 View Files & Folders",       self._view),
            ("➕ Create File",                 self._create_file_ui),
            ("📖 Read File",                   self._read_file_ui),
            ("✏️  Update File",                self._update_file_ui),
            ("🗑️  Delete File",                self._delete_file_ui),
            ("🔤 Rename File",                 self._rename_file_ui),
            ("📁 Create Folder",              self._create_folder_ui),
            ("❌ Delete Folder",              self._delete_folder_ui),
            ("📁➕ Folder + File",            self._folder_file_ui),
        ]

        for label, cmd in self.ops:
            btn = tk.Button(
                sidebar, text=label, bg=BG2, fg=ACCENT,
                activebackground=ACCENT, activeforeground=BG,
                relief="flat", bd=0, font=FONT, anchor="w",
                padx=14, pady=6, cursor="hand2",
                command=cmd,
            )
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2a3050"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG2))

        # Right main area
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Default view
        self._view()

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ── Reusable Widgets ──────────────────────────────────────────────────────

    def _header(self, text):
        tk.Label(self.main, text=text, bg=BG, fg=ACCENT,
                 font=FONT_BIG, anchor="w").pack(fill="x", pady=(0, 8))

    def _label(self, text):
        tk.Label(self.main, text=text, bg=BG, fg=FG_DIM,
                 font=FONT_SM, anchor="w").pack(fill="x")

    def _entry(self, placeholder=""):
        e = tk.Entry(self.main, bg=BG2, fg=FG, insertbackground=ACCENT,
                     relief="flat", font=FONT, bd=6)
        e.pack(fill="x", pady=(0, 8))
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=FG_DIM)
            def on_focus_in(ev, entry=e, ph=placeholder):
                if entry.get() == ph:
                    entry.delete(0, "end")
                    entry.config(fg=FG)
            def on_focus_out(ev, entry=e, ph=placeholder):
                if not entry.get():
                    entry.insert(0, ph)
                    entry.config(fg=FG_DIM)
            e.bind("<FocusIn>", on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
        return e

    def _textarea(self, height=6):
        ta = tk.Text(self.main, bg=BG2, fg=FG, insertbackground=ACCENT,
                     relief="flat", font=FONT, bd=6, height=height)
        ta.pack(fill="x", pady=(0, 8))
        return ta

    def _btn(self, text, cmd, danger=False):
        color = ERR if danger else ACCENT
        tk.Button(
            self.main, text=text, command=cmd,
            bg=color, fg=BG, activebackground=FG, activeforeground=BG,
            relief="flat", font=FONT, padx=10, pady=6, cursor="hand2",
        ).pack(anchor="w", pady=(4, 0))

    def _file_tree(self):
        """Scrollable file tree panel."""
        frame = tk.Frame(self.main, bg=BG2, bd=0)
        frame.pack(fill="both", expand=True, pady=(8, 8))

        sb = tk.Scrollbar(frame, bg=BG2, troughcolor=BG2)
        sb.pack(side="right", fill="y")

        lb = tk.Listbox(
            frame, bg=BG2, fg=FG, selectbackground=ACCENT, selectforeground=BG,
            relief="flat", font=FONT_SM, bd=8,
            yscrollcommand=sb.set, activestyle="none",
        )
        lb.pack(side="left", fill="both", expand=True)
        sb.config(command=lb.yview)

        items = list(Path('').rglob('*'))
        if items:
            for item in items:
                icon = "📁 " if item.is_dir() else "📄 "
                lb.insert("end", icon + str(item))
        else:
            lb.insert("end", "  (empty)")
        return lb

    def _result(self, text, ok=True):
        color = ACCENT if ok else ERR
        lbl = tk.Label(self.main, text=text, bg=BG, fg=color,
                       font=FONT, anchor="w", wraplength=600, justify="left")
        lbl.pack(fill="x", pady=(6, 0))

    # ── Operations ────────────────────────────────────────────────────────────

    def _view(self):
        self._clear_main()
        self._header("📋 Files & Folders")
        self._file_tree()

    # Create File
    def _create_file_ui(self):
        self._clear_main()
        self._header("➕ Create File")
        self._file_tree()
        self._label("File name")
        name_e = self._entry("e.g. notes.txt")
        self._label("Content")
        content_ta = self._textarea()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            name = name_e.get().strip()
            if not name or name == "e.g. notes.txt":
                res.config(text="⚠ Enter a file name.", fg=ERR); return
            p = Path(name)
            if p.exists():
                res.config(text="⚠ File already exists!", fg=ERR)
            else:
                try:
                    p.write_text(content_ta.get("1.0", "end"))
                    res.config(text=f"✅ '{name}' created!", fg=ACCENT)
                except Exception as e:
                    res.config(text=str(e), fg=ERR)

        self._btn("Create File", do)

    # Read File
    def _read_file_ui(self):
        self._clear_main()
        self._header("📖 Read File")
        self._file_tree()
        self._label("File name")
        name_e = self._entry()
        out = scrolledtext.ScrolledText(
            self.main, bg=BG2, fg=FG, insertbackground=ACCENT,
            relief="flat", font=FONT_SM, bd=6, height=8, state="disabled"
        )
        out.pack(fill="both", expand=True, pady=6)

        def do():
            name = name_e.get().strip()
            p = Path(name)
            if not name:
                return
            if p.exists():
                try:
                    text = p.read_text()
                    out.config(state="normal")
                    out.delete("1.0", "end")
                    out.insert("1.0", text)
                    out.config(state="disabled")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Not Found", "File not found!")

        self._btn("Read File", do)

    # Update File
    def _update_file_ui(self):
        self._clear_main()
        self._header("✏️ Update File")
        self._file_tree()
        self._label("File name")
        name_e = self._entry()
        mode_var = tk.StringVar(value="Overwrite")
        row = tk.Frame(self.main, bg=BG)
        row.pack(fill="x", pady=4)
        for m in ("Overwrite", "Append"):
            tk.Radiobutton(row, text=m, variable=mode_var, value=m,
                           bg=BG, fg=FG, selectcolor=BG2,
                           activebackground=BG, activeforeground=ACCENT,
                           font=FONT).pack(side="left", padx=6)
        self._label("New content")
        content_ta = self._textarea()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            name = name_e.get().strip()
            p = Path(name)
            if not p.exists():
                res.config(text="⚠ File does not exist!", fg=ERR); return
            try:
                mode = 'w' if mode_var.get() == "Overwrite" else 'a'
                with open(name, mode) as f:
                    f.write(content_ta.get("1.0", "end"))
                res.config(text=f"✅ File updated ({mode_var.get()})!", fg=ACCENT)
            except Exception as e:
                res.config(text=str(e), fg=ERR)

        self._btn("Update File", do)

    # Delete File
    def _delete_file_ui(self):
        self._clear_main()
        self._header("🗑️ Delete File")
        self._file_tree()
        self._label("File name")
        name_e = self._entry()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            name = name_e.get().strip()
            p = Path(name)
            if p.exists():
                if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
                    try:
                        os.remove(p)
                        res.config(text=f"✅ '{name}' deleted!", fg=ACCENT)
                    except Exception as e:
                        res.config(text=str(e), fg=ERR)
            else:
                res.config(text="⚠ File not found!", fg=ERR)

        self._btn("Delete File", do, danger=True)

    # Rename File
    def _rename_file_ui(self):
        self._clear_main()
        self._header("🔤 Rename File")
        self._file_tree()
        self._label("Current file name")
        old_e = self._entry()
        self._label("New file name")
        new_e = self._entry()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            old = old_e.get().strip()
            new = new_e.get().strip()
            p = Path(old)
            if p.exists():
                try:
                    p.rename(new)
                    res.config(text=f"✅ Renamed → '{new}'!", fg=ACCENT)
                except Exception as e:
                    res.config(text=str(e), fg=ERR)
            else:
                res.config(text="⚠ File not found!", fg=ERR)

        self._btn("Rename File", do)

    # Create Folder
    def _create_folder_ui(self):
        self._clear_main()
        self._header("📁 Create Folder")
        self._file_tree()
        self._label("Folder name")
        name_e = self._entry()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            name = name_e.get().strip()
            p = Path(name)
            if p.exists():
                res.config(text="⚠ Folder already exists!", fg=ERR)
            else:
                try:
                    p.mkdir()
                    res.config(text=f"✅ Folder '{name}' created!", fg=ACCENT)
                except Exception as e:
                    res.config(text=str(e), fg=ERR)

        self._btn("Create Folder", do)

    # Delete Folder
    def _delete_folder_ui(self):
        self._clear_main()
        self._header("❌ Delete Folder")
        self._file_tree()
        self._label("Folder name")
        name_e = self._entry()
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            name = name_e.get().strip()
            p = Path(name)
            if p.exists():
                if messagebox.askyesno("Confirm", f"Delete folder '{name}'?"):
                    try:
                        p.rmdir()
                        res.config(text=f"✅ Folder '{name}' deleted!", fg=ACCENT)
                    except Exception as e:
                        res.config(text=str(e), fg=ERR)
            else:
                res.config(text="⚠ Folder not found!", fg=ERR)

        self._btn("Delete Folder", do, danger=True)

    # Create Folder + File
    def _folder_file_ui(self):
        self._clear_main()
        self._header("📁➕ Create Folder + File")
        self._file_tree()
        self._label("Folder name")
        folder_e = self._entry()
        self._label("File name inside folder")
        file_e = self._entry()
        self._label("File content")
        content_ta = self._textarea(height=4)
        res = tk.Label(self.main, text="", bg=BG, font=FONT, anchor="w")
        res.pack(fill="x")

        def do():
            folder = folder_e.get().strip()
            fname  = file_e.get().strip()
            if not folder or not fname:
                res.config(text="⚠ Fill in both fields.", fg=ERR); return
            try:
                p = Path(folder)
                if not p.exists():
                    p.mkdir()
                file_path = p / fname
                file_path.write_text(content_ta.get("1.0", "end"))
                res.config(
                    text=f"✅ '{fname}' created inside '{folder}'!", fg=ACCENT
                )
            except Exception as e:
                res.config(text=str(e), fg=ERR)

        self._btn("Create Folder + File", do)


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()