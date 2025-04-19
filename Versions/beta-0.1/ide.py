from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.font as font
import ctypes
import re

from lexer import run
from parser import parse
from interpreter import interpret
from exception import *
def rgb(rgb_):
    """
    Преобразует кортеж RGB в строку цвета в формате HEX.
    :param rgb_: кортеж из 3 целых чисел, представляющих компоненты цвета (R, G, B).
    :return: строка цвета в формате HEX.
    """
    return "#%02x%02x%02x" % rgb_

class CodeEditor:
    """
    Класс редактора кода, который включает текстовую область редактирования, подсветку синтаксиса и вывод.
    """
    def __init__(self, root):
        """
        Инициализирует редактор кода, настраивает интерфейс и теги для подсветки синтаксиса.
        :param root: корневой виджет (обычно Tk).
        """
        self.root = root
        self.setup_ui()
        self.setup_tags()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс редактора: области для текста и вывода, панель прокрутки.
        """
        # Основная рамка
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Номера строк
        self.line_numbers = Text(self.main_frame, width=2, padx=8, pady=2,
                                 takefocus=0, border=0, background='#303030',
                                 foreground='#707070', state='disabled',
                                 font=fonts["Consolas"])
        self.line_numbers.pack(side=LEFT, fill=Y)

        # Текстовый редактор
        self.edit_area = Text(
            self.main_frame, background=background, foreground=normal,
            insertbackground=normal, relief=FLAT, wrap=NONE,
            borderwidth=0, font=fonts["Consolas"], undo=True
        )
        self.edit_area.pack(side=LEFT, fill=BOTH, expand=True)

        self.edit_area.bind('<<Modified>>', self.on_modified)
        self.edit_area.bind("<Tab>", self.on_tab)
        self.edit_area.bind("<MouseWheel>", self.on_mousewheel)
        self.edit_area.bind("<Button-4>", self.on_mousewheel)
        self.edit_area.bind("<Button-5>", self.on_mousewheel)
        self.edit_area.bind("<Escape>", exit)

        # Панель прокрутки
        self.scrollbar = ttk.Scrollbar(self.main_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.edit_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.on_scroll)

        # Вывод
        self.output_area = Text(
            self.root, height=8, background="#1e1e1e", foreground="#d4d4d4",
            insertbackground="white", font=fonts["Consolas"], state='disabled'
        )
        self.output_area.pack(side=BOTTOM, fill=X)

        self.update_highlight()
        self.update_line_numbers()

    def setup_tags(self):
        """
        Настраивает теги для подсветки синтаксиса (на основе правил `repl`).
        """
        for pattern, color in repl:
            self.edit_area.tag_configure(color, foreground=color)
    def on_modified(self, event=None):
        """
        Обрабатывает изменения в тексте, сбрасывает флаг модификации и обновляет подсветку и нумерацию строк.
        """
        self.edit_area.tk.call(self.edit_area._w, 'edit', 'modified', 0)
        self.update_line_numbers()
        self.update_highlight()

    def on_tab(self, event):
        """
        Обрабатывает нажатие клавиши Tab, вставляя 4 пробела.
        """
        self.edit_area.insert(INSERT, "    ")  # 4 spaces
        return "break"

    def on_scroll(self, *args):
        """
        Обрабатывает события прокрутки и синхронизирует прокрутку текстового редактора с номерами строк.
        """
        self.edit_area.yview(*args)
        self.line_numbers.yview(*args)

    def on_mousewheel(self, event):
        """
        Обрабатывает события прокрутки мыши и обновляет нумерацию строк в реальном времени.
        """
        direction = -1 if event.delta > 0 or event.num == 4 else 1
        self.edit_area.yview_scroll(direction, "units")
        self.update_line_numbers()
        return "break"

    def update_highlight(self):
        """
        Обновляет подсветку синтаксиса в редакторе, удаляя старые теги и применяя новые.
        """
        text = self.edit_area.get("1.0", "end-1c")

        # Удаляем старые теги
        for tag in self.edit_area.tag_names():
            if tag not in ('sel', 'insert'):
                self.edit_area.tag_remove(tag, "1.0", "end")

        # Применяем новые теги по шаблонам
        for pattern, color in repl:
            for start, end in self.search_re(pattern, text):
                self.edit_area.tag_add(color, start, end)

    def search_re(self, pattern, text):
        """
        Ищет все совпадения с регулярным выражением в тексте и возвращает их в виде списка кортежей (начало, конец).
        :param pattern: регулярное выражение.
        :param text: текст, в котором выполняется поиск.
        :return: список кортежей с диапазонами для каждого совпадения.
        """
        return [(f"{i + 1}.{m.start()}", f"{i + 1}.{m.end()}")
                for i, line in enumerate(text.splitlines())
                for m in re.finditer(pattern, line)]

    def update_line_numbers(self):
        """
        Обновляет номера строк в редакторе в реальном времени.
        """
        lines = self.edit_area.get("1.0", "end-1c").split("\n")
        self.line_numbers.config(state=NORMAL)
        self.line_numbers.delete("1.0", END)

        for i, _ in enumerate(lines, 1):
            self.line_numbers.insert(END, f"{i}\n")

        self.line_numbers.config(state=DISABLED)
        self.line_numbers.yview_moveto(self.edit_area.yview()[0])

    def print_to_output(self, text):
        """
        Выводит текст в область вывода внизу редактора.
        :param text: текст, который нужно вывести.
        """
        self.output_area.config(state=NORMAL)
        self.output_area.insert(END, str(text) + "\n")
        self.output_area.see(END)
        self.output_area.config(state=DISABLED)

# Инициализация DPI-aware приложения
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Константы
TITLE = "QuarkScript IDE"
font_size = 16
fonts = {"Consolas": ("Consolas", font_size)}

# Цвета
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((60, 179, 113))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
digits = rgb((204, 255, 255))
import_color = rgb((244, 164, 96))
# Правила подсветки синтаксиса
repl = [
    [r'\b(stdout|public|private|class|var|False|True|if|elif|else|trigger|func|extend|package|void|null|preload|return)\b', keywords],
    [r'".*?"', string],
    [r"'.*?'", string],
    [r'//.*?$', comments],
    [r'#.*?$', import_color],
    [r'(?<!")(?<!\')\b(-?\d+\.?\d*)\b(?!")', digits],
    [r'(?<!")(?<!\')\b(String|Int|Float|Bool|Object|MainStream|setTriggerActions|this|type|length|slice)\b(?!")', function],
]

# Создание и запуск приложения
root = Tk()
root.geometry("1000x700")
root.title(TITLE)

editor = CodeEditor(root)

def run_code(event=None):
    """
    Запускает код, компилирует, интерпретирует и выводит результат в область вывода.
    """
    editor.output_area.config(state=NORMAL)
    editor.output_area.delete("1.0", END)
    editor.output_area.config(state=DISABLED)
    nodes = list()
    code = editor.edit_area.get("1.0", END)
    # try:
    tokens = run(code)
    nodes = parse(tokens)
    result = interpret(nodes)
    for ex in result:
        editor.print_to_output(ex)
    # except Error as QuarkScriptError:
    #     editor.print_to_output(QuarkScriptError)
    # except Exception as InterpreterErrorORPythonError:
    #     editor.print_to_output(InterpreterErrorORPythonError)
    for node in nodes:
        print(node)

def save_file(event=None):
    """
    Сохраняет текущий код в файл.
    """
    code = editor.edit_area.get("1.0", END)
    filepath = asksaveasfilename(defaultextension=".qks",
                                  filetypes=[("QuarkScript files", "*.qs"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(code)

def open_file(event=None):
    """
    Открывает файл и загружает его содержимое в редактор.
    """
    filepath = askopenfilename(filetypes=[("QuarkScript files", "*.qs"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        editor.edit_area.delete("1.0", END)
        editor.edit_area.insert("1.0", content)
        editor.update_highlight()
        editor.update_line_numbers()

# События клавиш
root.bind("<F5>", run_code)
root.bind("<Control-s>", save_file)
root.bind("<Control-o>", open_file)

root.mainloop()
