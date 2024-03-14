import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog, messagebox
from jentalk_parser import JentalkParser
from jentalk_syntax_highlighter import JentalkSyntaxHighlighter
from jentalk_auto_completer import JentalkAutoCompleter
from jentalk_debugging_tools import JentalkDebuggingTools
from jentalk_visualization_components import JentalkVisualizationComponents

class JentalkIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jentalk IDE")
        self.geometry("1900x1080")
        self.breakpoints = set()

        # Define the base font size and calculate 4x size
        base_font_size = 12  # Assuming 12 is the base size, adjust this value as needed
        bigger_font_size = base_font_size * 4

        # Define the font to be used in the editor and console
        self.custom_font = font.Font(family="Helvetica", size=bigger_font_size)

        self.create_toolbar()
        self.create_editor()
        self.create_console()
        self.create_status_bar()

        self.jentalk_parser = JentalkParser()
        self.syntax_highlighter = JentalkSyntaxHighlighter(self.editor)
        self.auto_completer = JentalkAutoCompleter(self.editor)
        self.debugging_tools = JentalkDebuggingTools(self.editor, self.console)
        self.visualization_components = JentalkVisualizationComponents(self.editor, self.console)
        
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Set Breakpoint", command=self.debugging_tools.set_breakpoint)
        tools_menu.add_command(label="Resume", command=self.debugging_tools.resume_execution)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menu_bar)

    def create_toolbar(self):
        toolbar = ttk.Frame(self)
        new_button = ttk.Button(toolbar, text="New", command=self.new_file)
        new_button.pack(side=tk.LEFT, padx=2, pady=2)
        open_button = ttk.Button(toolbar, text="Open", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=2, pady=2)
        save_button = ttk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_editor(self):
        editor_frame = ttk.Frame(self)
        self.editor = tk.Text(editor_frame, font=self.custom_font)  # Apply the custom font
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(editor_frame, command=self.editor.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=scrollbar.set)
        editor_frame.pack(fill=tk.BOTH, expand=True)

    def create_console(self):
        console_frame = ttk.Frame(self)
        self.console = tk.Text(console_frame, height=10, font=self.custom_font)  # Apply the custom font
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)
        console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  # Change the pack side to BOTTOM

    def create_status_bar(self):
        self.status_bar = ttk.Label(self, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self):
        self.editor.delete('1.0', tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor.delete('1.0', tk.END)
                self.editor.insert('1.0', content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jtk")
        if file_path:
            content = self.editor.get('1.0', tk.END)
            with open(file_path, 'w') as file:
                file.write(content)

    def cut(self):
        self.editor.event_generate("<<Cut>>")

    def copy(self):
        self.editor.event_generate("<<Copy>>")

    def paste(self):
        self.editor.event_generate("<<Paste>>")

    def show_about(self):
        messagebox.showinfo("About Jentalk IDE", "Jentalk IDE\nVersion 1.0")    

if __name__ == "__main__":
    ide = JentalkIDE()
    ide.mainloop()