import tkinter as tk
import re
from jentalk_parser import JentalkParser

class JentalkSyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.jentalk_parser = JentalkParser()
        
        # Increase font size
        larger_font = ('Helvetica', 12 * 4)  # Assuming base font size is 12, making it 4x larger
        self.text_widget.configure(font=larger_font)
        
        # Define tag configurations for syntax highlighting
        self.define_tag_configs()

        # Bind the highlight_syntax method to text changes
        self.text_widget.bind('<<Modified>>', self.highlight_syntax, add='+')
        self.text_widget.bind('<KeyRelease>', self.highlight_syntax, add='+')

    def define_tag_configs(self):
        # Initialize text widget tags for primitives and modifiers with specific colors
        self.text_widget.tag_configure('primitive', foreground='#6A5ACD')  # Example color for primitives
        self.text_widget.tag_configure('modifier', foreground='#2E8B57')  # Example color for modifiers
        self.text_widget.tag_configure('modified_primitive', foreground='#FF6347')  # Example color for modified primitives
        self.text_widget.tag_configure('UNKNOWN', foreground='#A0522D')  # Example color for unknown tokens

    def highlight_syntax(self, event=None):
        # Prevent recursive triggering and handle only relevant key events
        if event and event.keysym in ("Left", "Right", "Up", "Down"):
            return
        
        # Remove existing highlighting
        for tag in ['primitive', 'modifier', 'modified_primitive', 'UNKNOWN']:
            self.text_widget.tag_remove(tag, '1.0', tk.END)

        content = self.text_widget.get("1.0", tk.END)
        self.apply_syntax_highlighting(content)

        # Reset the modified flag
        self.text_widget.edit_modified(False)

    def apply_syntax_highlighting(self, content):
        # Iterate through primitives and modifiers to apply highlighting
        for token_type, pattern in {**self.jentalk_parser.primitives, **self.jentalk_parser.modifiers}.items():
            for match in re.finditer(pattern, content):
                start, end = match.span()
                start_index = f'1.0+{start}c'
                end_index = f'1.0+{end}c'

                # Determine if the token is modified based on the presence of a modifier
                is_modified = any(modifier in match.group(0) for modifier in self.jentalk_parser.modifiers.values())
                tag = 'modified_primitive' if is_modified else 'primitive'

                self.text_widget.tag_add(tag, start_index, end_index)

# Example usage of JentalkSyntaxHighlighter within the IDE setup
if __name__ == "__main__":
    root = tk.Tk()
    editor = tk.Text(root)
    editor.pack(expand=True, fill='both')
    syntax_highlighter = JentalkSyntaxHighlighter(editor)
    root.mainloop()
