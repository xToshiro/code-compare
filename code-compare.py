import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import difflib
import math
import os
import subprocess
import tempfile
import json

class CodeComparatorApp:
    def __init__(self, root):
        self.root = root
        self.config_file = "config.json"
        
        # Configurações Padrão
        self.current_lang_code = "pt"
        self.ide_path = "" 
        self.current_theme_name = "Claro"

        # Tenta carregar configurações salvas
        self.load_config()
        
        self.path_a = None
        self.path_b = None
        
        # Dicionário de Traduções
        self.texts = {
            "pt": {
                "title": "Comparador de Código Pro - Dr. Jairo Brito",
                "btn_open_a": "📂 Abrir A",
                "btn_open_b": "📂 Abrir B",
                "btn_compare": "▶ COMPARAR",
                "btn_charts": "📊 Gráficos",
                "btn_clear": "🧹 Limpar",
                "lbl_lang": "Sintaxe:",
                "chk_sync": "🔗 Sync Scroll",
                "status_wait": "Aguardando...",
                "status_clean": "Status: Limpo",
                "frame_a": "Original (A)",
                "frame_b": "Modificado (B)",
                "btn_ide": "📝 Abrir na IDE",
                "menu_file": "Arquivo",
                "menu_load_a": "Carregar Original (A)...",
                "menu_load_b": "Carregar Modificado (B)...",
                "menu_save": "Salvar Relatório (.txt)",
                "menu_exit": "Sair",
                "menu_conf": "Configurações",
                "menu_theme": "Temas",
                "menu_ide": "Definir IDE Favorita...",
                "menu_lang": "Idioma / Language",
                "menu_help": "Ajuda",
                "menu_about": "Sobre",
                "msg_success": "Sucesso",
                "msg_saved": "Relatório salvo!",
                "msg_error": "Erro",
                "msg_warn": "Aviso",
                "msg_no_diff": "Execute uma comparação primeiro.",
                "chart_title": "Distribuição das Alterações",
                "chart_eq": "Iguais",
                "chart_add": "Adições",
                "chart_del": "Remoções",
                "chart_total": "Total Linhas Analisadas",
                "chart_rate": "Taxa de Alteração",
                "stats_simil": "Simil",
                "stats_blocks": "Δ Blocos"
            },
            "en": {
                "title": "Code Comparator Pro - Dr. Jairo Brito",
                "btn_open_a": "📂 Open A",
                "btn_open_b": "📂 Open B",
                "btn_compare": "▶ COMPARE",
                "btn_charts": "📊 Charts",
                "btn_clear": "🧹 Clear",
                "lbl_lang": "Syntax:",
                "chk_sync": "🔗 Sync Scroll",
                "status_wait": "Waiting...",
                "status_clean": "Status: Clean",
                "frame_a": "Original (A)",
                "frame_b": "Modified (B)",
                "btn_ide": "📝 Open in IDE",
                "menu_file": "File",
                "menu_load_a": "Load Original (A)...",
                "menu_load_b": "Load Modified (B)...",
                "menu_save": "Save Report (.txt)",
                "menu_exit": "Exit",
                "menu_conf": "Settings",
                "menu_theme": "Themes",
                "menu_ide": "Set Favorite IDE...",
                "menu_lang": "Language / Idioma",
                "menu_help": "Help",
                "menu_about": "About",
                "msg_success": "Success",
                "msg_saved": "Report saved!",
                "msg_error": "Error",
                "msg_warn": "Warning",
                "msg_no_diff": "Run a comparison first.",
                "chart_title": "Change Distribution",
                "chart_eq": "Equal",
                "chart_add": "Additions",
                "chart_del": "Deletions",
                "chart_total": "Total Analyzed Lines",
                "chart_rate": "Change Rate",
                "stats_simil": "Simil",
                "stats_blocks": "Δ Blocks"
            }
        }

        self.root.geometry("1300x850") # Aumentei um pouco a altura
        
        self.last_stats = {"equal": 0, "insert": 0, "delete": 0}
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # --- UI ELEMENTS ---
        # Toolbar Container
        toolbar = ttk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Armazenar referências para atualizar texto depois
        self.btn_open_a = ttk.Button(toolbar, command=lambda: self.load_file('A'))
        self.btn_open_a.pack(side=tk.LEFT, padx=2)
        
        self.btn_open_b = ttk.Button(toolbar, command=lambda: self.load_file('B'))
        self.btn_open_b.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        self.btn_compare = ttk.Button(toolbar, command=self.compare_code)
        self.btn_compare.pack(side=tk.LEFT, padx=2)
        
        self.btn_charts = ttk.Button(toolbar, command=self.show_charts)
        self.btn_charts.pack(side=tk.LEFT, padx=2)
        
        self.btn_clear = ttk.Button(toolbar, command=self.clear_all)
        self.btn_clear.pack(side=tk.LEFT, padx=2)

        self.lbl_lang_title = ttk.Label(toolbar)
        self.lbl_lang_title.pack(side=tk.LEFT, padx=(15, 5))
        
        self.lang_var = tk.StringVar(value="Python")
        langs = ["Python", "C/C++", "Java", "JavaScript", "Texto Puro", "HTML/CSS"]
        self.combo_lang = ttk.Combobox(toolbar, values=langs, textvariable=self.lang_var, state="readonly", width=10)
        self.combo_lang.pack(side=tk.LEFT)

        self.sync_val = tk.BooleanVar(value=True)
        self.chk_sync = ttk.Checkbutton(toolbar, variable=self.sync_val)
        self.chk_sync.pack(side=tk.LEFT, padx=15)

        self.lbl_stats = ttk.Label(toolbar, font=("Arial", 9, "bold"))
        self.lbl_stats.pack(side=tk.RIGHT, padx=10)

        # Panes
        paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame Left Container
        self.frame_left = ttk.LabelFrame(paned_window)
        paned_window.add(self.frame_left, weight=1)
        self.text_left, self.scroll_y_left, self.btn_ide_a = self.create_text_area(self.frame_left, 'A')

        # Frame Right Container
        self.frame_right = ttk.LabelFrame(paned_window)
        paned_window.add(self.frame_right, weight=1)
        self.text_right, self.scroll_y_right, self.btn_ide_b = self.create_text_area(self.frame_right, 'B')

        self.setup_sync_scroll()
        
        # Inicialização
        self.current_theme_data = {} 
        self.update_ui_text()
        self.apply_theme(self.current_theme_name) # Aplica o tema salvo

    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.current_lang_code = data.get("lang", "pt")
                    self.ide_path = data.get("ide_path", "")
                    self.current_theme_name = data.get("theme", "Claro")
            except Exception as e:
                print(f"Erro ao carregar config: {e}")

    def save_config(self):
        """Salva configurações no arquivo JSON"""
        data = {
            "lang": self.current_lang_code,
            "ide_path": self.ide_path,
            "theme": self.current_theme_name
        }
        try:
            with open(self.config_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    def t(self, key):
        return self.texts[self.current_lang_code].get(key, key)

    def set_language(self, lang):
        self.current_lang_code = lang
        self.save_config() # Salva ao mudar
        self.update_ui_text()
        self.create_menu(self.current_theme_data)

    def update_ui_text(self):
        """Atualiza todos os textos da interface"""
        self.root.title(self.t("title"))
        self.btn_open_a.config(text=self.t("btn_open_a"))
        self.btn_open_b.config(text=self.t("btn_open_b"))
        self.btn_compare.config(text=self.t("btn_compare"))
        self.btn_charts.config(text=self.t("btn_charts"))
        self.btn_clear.config(text=self.t("btn_clear"))
        self.lbl_lang_title.config(text=self.t("lbl_lang"))
        self.chk_sync.config(text=self.t("chk_sync"))
        self.frame_left.config(text=self.t("frame_a"))
        self.frame_right.config(text=self.t("frame_b"))
        self.btn_ide_a.config(text=self.t("btn_ide"))
        self.btn_ide_b.config(text=self.t("btn_ide"))
        
        if self.lbl_stats.cget("text") in ["Aguardando...", "Waiting...", "Status: Limpo", "Status: Clean"]:
             self.lbl_stats.config(text=self.t("status_wait"))

    def create_menu(self, theme_colors=None):
        menubar = tk.Menu(self.root)
        
        bg = theme_colors.get("bg", "#FFFFFF") if theme_colors else "#FFFFFF"
        fg = theme_colors.get("fg", "#000000") if theme_colors else "#000000"
        
        def make_menu():
            return tk.Menu(menubar, tearoff=0, bg=bg, fg=fg, activebackground=fg, activeforeground=bg)

        # Menu Arquivo
        file_menu = make_menu()
        file_menu.add_command(label=self.t("menu_load_a"), command=lambda: self.load_file('A'))
        file_menu.add_command(label=self.t("menu_load_b"), command=lambda: self.load_file('B'))
        file_menu.add_separator()
        file_menu.add_command(label=self.t("menu_save"), command=self.save_report)
        file_menu.add_separator()
        file_menu.add_command(label=self.t("menu_exit"), command=self.root.quit)
        menubar.add_cascade(label=self.t("menu_file"), menu=file_menu)

        # Menu Configurações
        conf_menu = make_menu()
        conf_menu.add_command(label=self.t("menu_ide"), command=self.set_ide_path)
        conf_menu.add_separator()
        
        theme_menu = make_menu()
        theme_menu.add_command(label="Claro (Default)", command=lambda: self.apply_theme("Claro"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.apply_theme("Dark"))
        theme_menu.add_command(label="Dracula", command=lambda: self.apply_theme("Dracula"))
        conf_menu.add_cascade(label=self.t("menu_theme"), menu=theme_menu)
        
        lang_menu = make_menu()
        lang_menu.add_command(label="Português", command=lambda: self.set_language("pt"))
        lang_menu.add_command(label="English", command=lambda: self.set_language("en"))
        conf_menu.add_cascade(label=self.t("menu_lang"), menu=lang_menu)
        
        menubar.add_cascade(label=self.t("menu_conf"), menu=conf_menu)

        # Menu Ajuda
        help_menu = make_menu()
        help_menu.add_command(label=self.t("menu_about"), command=self.show_about)
        menubar.add_cascade(label=self.t("menu_help"), menu=help_menu)

        try:
            menubar.config(bg=bg, fg=fg)
        except:
            pass 

        self.root.config(menu=menubar)

    def create_text_area(self, parent, side):
        # Frame para botão em baixo
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        btn_ide = ttk.Button(bottom_frame, text=self.t("btn_ide"), command=lambda: self.open_in_ide(side))
        btn_ide.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Área de texto
        text_widget = tk.Text(parent, wrap=tk.NONE, font=("Consolas", 10), undo=True)
        scroll_y = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=text_widget.xview)
        
        text_widget.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        return text_widget, scroll_y, btn_ide

    def set_ide_path(self):
        """Permite ao usuário escolher o executável da IDE"""
        path = filedialog.askopenfilename(title="Selecione o executável da sua IDE (code.exe, pycharm.exe...)", filetypes=[("Executáveis", "*.exe"), ("Todos", "*.*")])
        if path:
            self.ide_path = path
            self.save_config() # Salva ao mudar
            messagebox.showinfo(self.t("msg_success"), f"IDE definida: {os.path.basename(path)}")

    def open_in_ide(self, side):
        """Abre o conteúdo atual na IDE configurada ou padrão do sistema"""
        text_widget = self.text_left if side == 'A' else self.text_right
        original_path = self.path_a if side == 'A' else self.path_b
        
        current_content = text_widget.get("1.0", tk.END).strip()
        if not current_content: return

        target_file = None
        is_temp = False

        # Verifica se podemos usar o arquivo original (se não houve alteração)
        # Para simplificar, vamos salvar um temp se o conteúdo for diferente ou se não houver path
        need_temp = True
        if original_path and os.path.exists(original_path):
            with open(original_path, 'r', encoding='utf-8') as f:
                if f.read().strip() == current_content:
                    target_file = original_path
                    need_temp = False
        
        if need_temp:
            # Cria arquivo temporário com extensão baseada na linguagem
            ext_map = {"Python": ".py", "C/C++": ".cpp", "Java": ".java", "HTML/CSS": ".html", "JavaScript": ".js"}
            ext = ext_map.get(self.lang_var.get(), ".txt")
            
            fd, target_file = tempfile.mkstemp(suffix=ext, text=True)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(current_content)
            is_temp = True

        try:
            if self.ide_path and os.path.exists(self.ide_path):
                subprocess.Popen([self.ide_path, target_file])
            else:
                # Tenta abrir com o padrão do sistema
                if os.name == 'nt': # Windows
                    os.startfile(target_file)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open', target_file)) # Linux
                else:
                    subprocess.call(('open', target_file)) # Mac
        except Exception as e:
            messagebox.showerror(self.t("msg_error"), f"Erro ao abrir IDE: {e}")

    def setup_sync_scroll(self):
        self.scroll_y_left.config(command=lambda *a: self.sync_y(*a))
        self.scroll_y_right.config(command=lambda *a: self.sync_y(*a))
        
        for txt in [self.text_left, self.text_right]:
            txt.bind("<MouseWheel>", self.on_mousewheel)
            txt.bind("<Button-4>", self.on_mousewheel)
            txt.bind("<Button-5>", self.on_mousewheel)

    def sync_y(self, *args):
        if self.sync_val.get():
            self.text_left.yview(*args)
            self.text_right.yview(*args)
        else:
            self.text_left.yview(*args)
            self.text_right.yview(*args)

    def on_mousewheel(self, event):
        if not self.sync_val.get(): return
        amount = 1 if (event.num == 5 or (hasattr(event, 'delta') and event.delta < 0)) else -1
        self.text_left.yview_scroll(amount, "units")
        self.text_right.yview_scroll(amount, "units")
        return "break"

    def apply_theme(self, theme_name):
        themes = {
            "Claro": {"bg": "#FFFFFF", "fg": "#000000", "add": "#ccffcc", "del": "#ffcccc", "pad": "#f0f0f0", "menu_bg": "#f0f0f0"},
            "Dark":  {"bg": "#2b2b2b", "fg": "#dcdcdc", "add": "#2e4a2e", "del": "#4a2e2e", "pad": "#3c3f41", "menu_bg": "#3c3f41"},
            "Dracula": {"bg": "#282a36", "fg": "#f8f8f2", "add": "#50fa7b", "del": "#ff5555", "pad": "#44475a", "menu_bg": "#44475a"}
        }
        
        colors = themes.get(theme_name, themes["Claro"])
        self.current_theme_data = colors
        self.current_theme_name = theme_name # Atualiza o atual
        self.save_config() # Salva ao mudar
        
        self.create_menu(colors)

        for txt in [self.text_left, self.text_right]:
            txt.config(bg=colors["bg"], fg=colors["fg"], insertbackground=colors["fg"])
            txt.tag_configure("removed", background=colors["del"] if theme_name == "Claro" else "#5e2b2b")
            txt.tag_configure("added", background=colors["add"] if theme_name == "Claro" else "#2b5e34")
            txt.tag_configure("padding", background=colors["pad"], foreground=colors["pad"])
            
            if theme_name != "Claro":
                 txt.tag_configure("removed", foreground="#ffaaaa")
                 txt.tag_configure("added", foreground="#aaffaa")

    def load_file(self, side):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivos de Código", "*.py *.txt *.cpp *.java *.html"), ("Todos", "*.*")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                target = self.text_left if side == 'A' else self.text_right
                if side == 'A': self.path_a = filepath
                else: self.path_b = filepath
                
                target.delete("1.0", tk.END)
                target.insert(tk.END, content)
                self.compare_code() 
            except Exception as e:
                messagebox.showerror(self.t("msg_error"), f"Erro: {e}")

    def save_report(self):
        diff_text = f"Relatório de Diferenças / Diff Report - {self.lang_var.get()}\n"
        diff_text += f"{self.lbl_stats.cget('text')}\n"
        diff_text += "-" * 40 + "\n"
        lines_a = self.get_lines(self.text_left)
        lines_b = self.get_lines(self.text_right)
        diff = difflib.unified_diff(lines_a, lines_b, lineterm="")
        diff_text += "\n".join(diff)

        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(diff_text)
            messagebox.showinfo(self.t("msg_success"), self.t("msg_saved"))

    def get_lines(self, text_widget):
        return text_widget.get("1.0", tk.END).splitlines()

    def clear_all(self):
        self.text_left.delete("1.0", tk.END)
        self.text_right.delete("1.0", tk.END)
        self.path_a = None
        self.path_b = None
        self.lbl_stats.config(text=self.t("status_clean"))

    def show_about(self):
        messagebox.showinfo(self.t("menu_about"), "Code Comparator Pro v2.3\nDr. Jairo Brito.\n\nPython + Tkinter.")

    def show_charts(self):
        if self.last_stats["equal"] == 0 and self.last_stats["insert"] == 0 and self.last_stats["delete"] == 0:
            messagebox.showwarning(self.t("msg_warn"), self.t("msg_no_diff"))
            return

        win = tk.Toplevel(self.root)
        win.title(self.t("chart_title"))
        win.geometry("400x450")
        
        ttk.Label(win, text=self.t("chart_title"), font=("Arial", 12, "bold")).pack(pady=10)

        canvas = tk.Canvas(win, width=300, height=300, bg="white")
        canvas.pack()

        total = sum(self.last_stats.values())
        if total == 0: return

        data = {
            self.t("chart_eq"): (self.last_stats["equal"], "#cccccc"),
            self.t("chart_add"): (self.last_stats["insert"], "#90ee90"),
            self.t("chart_del"): (self.last_stats["delete"], "#ff9999")
        }

        start_angle = 0
        for label, (value, color) in data.items():
            extent = (value / total) * 360
            if extent > 0:
                canvas.create_arc(50, 50, 250, 250, start=start_angle, extent=extent, fill=color, outline="white")
                mid_angle = math.radians(start_angle + extent/2)
                x = 150 + 110 * math.cos(mid_angle)
                y = 150 + -110 * math.sin(mid_angle)
                if extent > 15:
                    canvas.create_text(x, y, text=f"{label}\n{value}", font=("Arial", 8))
                start_angle += extent
        
        summary = f"{self.t('chart_total')}: {total}\n"
        summary += f"{self.t('chart_rate')}: {((total - self.last_stats['equal'])/total)*100:.1f}%"
        ttk.Label(win, text=summary, justify=tk.CENTER).pack(pady=10)

    def compare_code(self):
        lines_a = self.get_lines(self.text_left)
        lines_b = self.get_lines(self.text_right)

        self.text_left.delete("1.0", tk.END)
        self.text_right.delete("1.0", tk.END)

        matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
        
        self.last_stats = {"equal": 0, "insert": 0, "delete": 0}
        changes = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            block_a = lines_a[i1:i2]
            block_b = lines_b[j1:j2]

            if tag == 'replace':
                max_len = max(len(block_a), len(block_b))
                for line in block_a: self.text_left.insert(tk.END, line + "\n", "removed")
                for _ in range(max_len - len(block_a)): self.text_left.insert(tk.END, " \n", "padding")
                
                for line in block_b: self.text_right.insert(tk.END, line + "\n", "added")
                for _ in range(max_len - len(block_b)): self.text_right.insert(tk.END, " \n", "padding")
                
                changes += 1
                self.last_stats["delete"] += len(block_a)
                self.last_stats["insert"] += len(block_b)

            elif tag == 'delete':
                for line in block_a:
                    self.text_left.insert(tk.END, line + "\n", "removed")
                    self.text_right.insert(tk.END, " \n", "padding")
                self.last_stats["delete"] += len(block_a)
                changes += 1

            elif tag == 'insert':
                for line in block_b:
                    self.text_left.insert(tk.END, " \n", "padding")
                    self.text_right.insert(tk.END, line + "\n", "added")
                self.last_stats["insert"] += len(block_b)
                changes += 1

            elif tag == 'equal':
                for line in block_a:
                    self.text_left.insert(tk.END, line + "\n")
                    self.text_right.insert(tk.END, line + "\n")
                self.last_stats["equal"] += len(block_a)

        ratio = matcher.ratio() * 100
        stats_msg = f"{self.t('stats_simil')}: {ratio:.1f}% | +{self.last_stats['insert']} | -{self.last_stats['delete']} | {self.t('stats_blocks')}: {changes}"
        self.lbl_stats.config(text=stats_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeComparatorApp(root)
    root.mainloop()