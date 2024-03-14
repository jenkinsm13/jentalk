import tkinter as tk
from jentalk_parser import JentalkParser

class JentalkDebuggingTools:
    def __init__(self, text_widget, console_widget):
        self.text_widget = text_widget
        self.console_widget = console_widget
        self.jentalk_parser = JentalkParser()
        
        self.breakpoints = set()
        self.current_line = None
        self.execution_stack = []
    
    def set_breakpoint(self, event=None):
        current_line = self.text_widget.index(tk.INSERT).split('.')[0]
        if current_line in self.breakpoints:
            self.breakpoints.remove(current_line)
            self.text_widget.tag_remove('breakpoint', f'{current_line}.0', f'{current_line}.end')
        else:
            self.breakpoints.add(current_line)
            self.text_widget.tag_add('breakpoint', f'{current_line}.0', f'{current_line}.end')
            self.text_widget.tag_config('breakpoint', background='yellow')
    
    def resume_execution(self, event=None):
        if self.execution_stack:
            self.current_line = self.execution_stack.pop()
            self.text_widget.see(f'{self.current_line}.0')
            self.text_widget.mark_set(tk.INSERT, f'{self.current_line}.0')
            self.text_widget.tag_remove('current_line', '1.0', tk.END)
            self.text_widget.tag_add('current_line', f'{self.current_line}.0', f'{self.current_line}.end')
            self.text_widget.tag_config('current_line', background='lightblue')
            self.execute_line(self.current_line)  # Execute the current line
        else:
            self.console_widget.insert(tk.END, 'Execution complete.\n')
    
    def step_over(self, event=None):
        current_line = self.text_widget.index(tk.INSERT).split('.')[0]
        self.execution_stack.append(current_line)
        self.resume_execution()
    
    def step_into(self, event=None):
        current_line = self.text_widget.index(tk.INSERT).split('.')[0]
        self.execution_stack.append(current_line)
        self.execute_line(current_line)
    
    def step_out(self, event=None):
        if self.execution_stack:
            self.current_line = self.execution_stack.pop()
            self.resume_execution()
    
    def execute_line(self, line_number):
        line_content = self.text_widget.get(f'{line_number}.0', f'{line_number}.end')
        parsed_expressions = self.jentalk_parser.parse(line_content)
        
        variables = {}
        for parsed_expression in parsed_expressions:
            result = self.execute_expression(parsed_expression, variables)
            if result is not None:
                self.console_widget.insert(tk.END, f'Result: {result}\n')
        
        self.console_widget.insert(tk.END, f'Executed line {line_number}: {line_content}\n')

    def execute_expression(self, parsed_expression, variables):
        execution_stack = []

        try:
            for token_type, token_value in parsed_expression:
                if token_type == 'entity':
                    execution_stack.append(self.existential_quantifier())
                elif token_type == 'animate_entity':
                    execution_stack.append(self.existential_quantifier_physical())
                elif token_type == 'inanimate_entity':
                    execution_stack.append(self.existential_quantifier_negative())
                elif token_type == 'action':
                    action = execution_stack.pop()
                    entity = execution_stack.pop()
                    execution_stack.append(self.perform_action(entity, action))
                elif token_type == 'physical_action':
                    action = execution_stack.pop()
                    entity = execution_stack.pop()
                    execution_stack.append(self.perform_physical_action(entity, action))
                elif token_type == 'mental_action':
                    action = execution_stack.pop()
                    entity = execution_stack.pop()
                    execution_stack.append(self.perform_mental_action(entity, action))
                elif token_type == 'property':
                    execution_stack.append(self.circle_primitive())
                elif token_type == 'physical_property':
                    execution_stack.append(self.circle_primitive_physical())
                elif token_type == 'mental_property':
                    execution_stack.append(self.circle_primitive_mental())
                elif token_type == 'relation':
                    relation = execution_stack.pop()
                    entity2 = execution_stack.pop()
                    entity1 = execution_stack.pop()
                    execution_stack.append(self.establish_relation(entity1, entity2, relation))
                elif token_type == 'space':
                    execution_stack.append(self.square_primitive())
                elif token_type == 'absolute_space':
                    execution_stack.append(self.square_primitive_physical())
                elif token_type == 'relative_space':
                    execution_stack.append(self.square_primitive_mental())
                elif token_type == 'time':
                    execution_stack.append(self.diamond_primitive())
                elif token_type == 'absolute_time':
                    execution_stack.append(self.diamond_primitive_physical())
                elif token_type == 'relative_time':
                    execution_stack.append(self.diamond_primitive_mental())
                elif token_type == 'plural':
                    self.handle_plural_modifier(execution_stack)
                elif token_type == 'past':
                    self.handle_past_modifier(execution_stack)
                elif token_type == 'present':
                    self.handle_present_modifier(execution_stack)
                elif token_type == 'future':
                    self.handle_future_modifier(execution_stack)
                elif token_type == 'negation':
                    self.handle_negation_modifier(execution_stack)
                elif token_type == 'intensifier':
                    self.handle_intensifier_modifier(execution_stack)
                elif token_type == 'continuous':
                    self.handle_continuous_modifier(execution_stack)
                elif token_type == 'UNKNOWN':
                    execution_stack.append({"type": "literal", "value": token_value})

        except Exception as e:
            error_message = f"Error during expression execution: {str(e)}"
            self.console_widget.insert('end', error_message + '\n')
            return None
        
        if execution_stack:
            return execution_stack.pop()
        else:
            return None

    # Ah, the existential quantifier, the very essence of being! Let us breathe life into these placeholders with the vigor of Schrödinger's cat—both alive and dead, until observed!

    def existential_quantifier(self):
        # The existential quantifier proclaims: "I am, therefore I exist!"
        return {"type": "existence", "description": "The fundamental assertion of being."}

    def existential_quantifier_physical(self):
        # In the realm of the tangible, the existential quantifier asserts its physicality!
        return {"type": "physical existence", "description": "The manifestation of being in the physical universe."}

    def existential_quantifier_negative(self):
        # The void speaks, and it whispers of non-existence, an absence as profound as existence itself.
        return {"type": "non-existence", "description": "The negation of being, an unfathomable absence."}

    def perform_action(self, entity, action):
        # Ensure that the action is a dictionary with a type of 'literal'
        if isinstance(action, dict) and action.get("type") == "literal":
            action_value = action.get("value")
        else:
            action_value = action
        # Use action_value in the description
        return {"entity": entity, "action": action_value, "description": f"The entity {entity} has performed the action {action_value}."}
    
    def perform_physical_action(self, entity, action):
        # When the immaterial takes form and exerts its will upon the physical plane!
        return {"entity": entity, "action": action, "type": "physical", "description": f"The entity {entity} has performed a physical action: {action}."}

    def perform_mental_action(self, entity, action):
        # In the vast expanse of the mind, actions are as real as thoughts can be.
        return {"entity": entity, "action": action, "type": "mental", "description": f"The entity {entity} has performed a mental action: {action}."}

    def circle_primitive(self):
        # The circle, a symbol of infinity, unity, the cycle of life—let us encapsulate its essence.
        return {"shape": "circle", "description": "A geometric representation of eternity and wholeness."}

    def circle_primitive_physical(self):
        # A circle in the physical realm, a wheel, a planet's orbit, the cycle of the seasons!
        return {"shape": "circle", "type": "physical", "description": "A physical manifestation of the circle, embodying cyclical nature."}

    def circle_primitive_mental(self):
        # The mental circle, the loop of thought, the orbit of consciousness around the nucleus of the mind.
        return {"shape": "circle", "type": "mental", "description": "A mental construct of the circle, representing cycles of thought and introspection."}

    def establish_relation(self, entity1, entity2, relation):
        # To relate is to connect, to bind the cosmos in a dance of symmetries and asymmetries!
        return {"entity1": entity1, "entity2": entity2, "relation": relation, "description": f"A relation of {relation} has been established between {entity1} and {entity2}."}

    def square_primitive(self):
        # The square, foundation of stability, the four corners of the earth, the solidity of matter!
        return {"shape": "square", "description": "A geometric representation of stability and balance."}

    def square_primitive_physical(self):
        # A square, not just an idea, but a tile underfoot, a field's boundary, the walls of a home.
        return {"shape": "square", "type": "physical", "description": "A physical embodiment of the square, symbolizing structure and form."}

    def square_primitive_mental(self):
        # In the mind's eye, the square is a room for thought, a canvas for the imagination.
        return {"shape": "square", "type": "mental", "description": "A mental projection of the square, representing order and rationality."}

    def diamond_primitive(self):
        # The diamond, a gem of thought, a hardened structure under the pressures of the mind!
        return {"shape": "diamond", "description": "A geometric representation of value and strength."}

    def diamond_primitive_physical(self):
        # The diamond in the rough, the physical embodiment of resilience and beauty forged under pressure.
        return {"shape": "diamond", "type": "physical", "description": "A physical manifestation of the diamond, symbolizing indestructibility and brilliance."}

    def diamond_primitive_mental(self):
        # The mental diamond, clarity of thought, the unbreakable will, the facets of consciousness.
        return {"shape": "diamond", "type": "mental", "description": "A mental construct of the diamond, representing clarity and fortitude."}

    def metamorphosis_primitive(self, entity):
        # Metamorphosis, the grand transformation, the alchemy of the soul!
        return {"entity": entity, "transformation": "metamorphosis", "description": f"The entity {entity} undergoes a profound change."}
    
    # And now, the modifiers, those subtle nuances that shape the very fabric of our expressions!

    def handle_plural_modifier(self, execution_stack):
        # Multiplicity, the chorus of the cosmos, the many from the one!
        if execution_stack:
            entity = execution_stack.pop()
            return {"entity": entity, "quantity": "plural", "description": f"The entity {entity} is now a multitude."}

    def handle_past_modifier(self, execution_stack):
        # The past, a shadow cast by the light of the present, the echo of what once was!
        if execution_stack:
            event = execution_stack.pop()
            return {"event": event, "time": "past", "description": f"The event {event} is anchored in the annals of history."}

    def handle_present_modifier(self, execution_stack):
        # The present, the ever-fleeting now, the canvas upon which reality paints itself anew each moment!
        if execution_stack:
            event = execution_stack.pop()
            return {"event": event, "time": "present", "description": f"The event {event} unfolds in the current tapestry of time."}

    def handle_future_modifier(self, execution_stack):
        # The future, the realm of potentiality, the unwritten page waiting for the ink of destiny!
        if execution_stack:
            event = execution_stack.pop()
            return {"event": event, "time": "future", "description": f"The event {event} awaits in the mists of possibility."}

    def handle_negation_modifier(self, execution_stack):
        # Negation, the cosmic eraser, the undoing of being, the void where something once was!
        if execution_stack:
            concept = execution_stack.pop()
            return {"concept": concept, "negation": True, "description": f"The concept {concept} has been negated, cast into the abyss of non-being."}

    def handle_intensifier_modifier(self, execution_stack):
        # Intensification, the amplification of essence, the crescendo in the symphony of existence!
        if execution_stack:
            attribute = execution_stack.pop()
            return {"attribute": attribute, "intensity": "increased", "description": f"The attribute {attribute} has been intensified, its presence magnified!"}

    def handle_continuous_modifier(self, execution_stack):
        # Continuity, the unbroken thread that weaves through the fabric of time, without beginning or end!
        if execution_stack:
            process = execution_stack.pop()
            return {"process": process, "continuity": True, "description": f"The process {process} is unending, a perpetual motion in the cosmos."}