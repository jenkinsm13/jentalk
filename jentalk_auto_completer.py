import tkinter as tk
from jentalk_parser import JentalkParser

class JentalkAutoCompleter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.jentalk_parser = JentalkParser()
        
        self.completion_listbox = tk.Listbox(self.text_widget, width=30, height=5)
        self.completion_listbox.place(x=0, y=0)
        self.completion_listbox.bind('<Double-1>', self.complete_token)
        self.completion_listbox.bind('<Escape>', self.hide_completion_listbox)
        
        self.text_widget.bind('<KeyRelease>', self.debounce_update_completions)
        
        self.debounce_delay = 100  # Adjust the delay as needed
        self.debounce_timer = None

    def debounce_update_completions(self, event):
        if self.debounce_timer is not None:
            self.text_widget.after_cancel(self.debounce_timer)
        self.debounce_timer = self.text_widget.after(self.debounce_delay, self.update_completions, event)
    
    def update_completions(self, event):
        self.completion_listbox.delete(0, tk.END)
        
        current_token = self.get_current_token()
        if not current_token:
            self.hide_completion_listbox()
            return
        
        completions = self.generate_completions(current_token)
        
        if completions:
            for completion in completions:
                self.completion_listbox.insert(tk.END, completion)
            self.show_completion_listbox()
        else:
            self.hide_completion_listbox()
    
    def get_current_token(self):
        current_position = self.text_widget.index(tk.INSERT)
        start_index = self.text_widget.search(r'\S+$', f'{current_position} linestart', regexp=True, backwards=True)
        if start_index:
            return self.text_widget.get(start_index, current_position)
        return ''
    
    def complete_token(self, event):
        selected_token = self.completion_listbox.get(self.completion_listbox.curselection())
        current_token = self.get_current_token()
        self.text_widget.delete(f'{tk.INSERT} - {len(current_token)}c', tk.INSERT)
        self.text_widget.insert(tk.INSERT, selected_token)
        self.hide_completion_listbox()
    
    def show_completion_listbox(self):
        self.completion_listbox.lift()
        self.completion_listbox.place(x=self.text_widget.winfo_x(), y=self.text_widget.winfo_y() + self.text_widget.winfo_height())
    
    def hide_completion_listbox(self, event=None):
        self.completion_listbox.place_forget()

    def generate_completions(self, current_token):
        completions = []
        for primitive, regex in self.jentalk_parser.primitives.items():
            if primitive.startswith(current_token):
                completions.append(primitive)
        for modifier, regex in self.jentalk_parser.modifiers.items():
            if modifier.startswith(current_token):
                completions.append(modifier)
        if "[[" in current_token:
            completions.append("[[a,b,c,...]] - Continued Fraction")
        return completions
