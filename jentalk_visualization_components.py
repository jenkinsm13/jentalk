import tkinter as tk
from jentalk_parser import JentalkParser
from graphviz import Digraph

class JentalkVisualizationComponents:
    def __init__(self, text_widget, console_widget):
        self.text_widget = text_widget
        self.console_widget = console_widget
        self.jentalk_parser = JentalkParser()
        
        self.text_widget.bind('<Control-t>', self.visualize_tree_of_thought)
        self.text_widget.bind('<Control-r>', self.visualize_reasoning_graph)
    
    def visualize_tree_of_thought(self, event=None):
        text = self.text_widget.get('1.0', tk.END)
        parsed_expressions = self.jentalk_parser.parse(text)
        
        tree_diagram = Digraph(name='Tree of Thought', format='pdf')
        tree_diagram.attr(rankdir='LR')
        
        for i, parsed_expression in enumerate(parsed_expressions):
            for j, (token_type, token_value) in enumerate(parsed_expression):
                if token_type not in ['UNKNOWN', '']:
                    node_name = f'{i}_{j}'
                    node_label = self.get_node_label(token_type, token_value)
                    tree_diagram.node(node_name, label=node_label)
                    if j > 0:
                        prev_node_name = f'{i}_{j-1}'
                        tree_diagram.edge(prev_node_name, node_name)

        output_filename = 'tree_of_thought.pdf'
        tree_diagram.render(output_filename, view=True)
        self.console_widget.insert(tk.END, f'Tree of Thought visualization generated: {output_filename}\n')

    def get_node_label(self, token_type, token_value):
        return f'{token_type}: {token_value}'

    def visualize_reasoning_graph(self, event=None):
        text = self.text_widget.get('1.0', tk.END)
        parsed_expressions = self.jentalk_parser.parse(text)
        
        reasoning_graph = Digraph(name='Reasoning Graph', format='pdf')
        reasoning_graph.attr(rankdir='TB')
        
        node_counter = 0
        for parsed_expression in parsed_expressions:
            prev_node_name = None
            for token_type, token_value in parsed_expression:
                if token_type not in ['UNKNOWN', '']:
                    node_name = f'node{node_counter}'
                    node_label = self.get_node_label(token_type, token_value)
                    reasoning_graph.node(node_name, label=node_label)
                    if prev_node_name:
                        reasoning_graph.edge(prev_node_name, node_name)
                    prev_node_name = node_name
                    node_counter += 1

        output_filename = 'reasoning_graph.pdf'
        reasoning_graph.render(output_filename, view=True)
        self.console_widget.insert(tk.END, f'Reasoning Graph visualization generated: {output_filename}\n')
