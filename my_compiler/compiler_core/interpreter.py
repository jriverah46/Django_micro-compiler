class Interpreter:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.current_index = 0
        self.ast = []
        self.execution_steps = []

    def reset(self):
        self.variables = {}
        self.output = []
        self.current_index = 0
        self.execution_steps = []

    def execute(self, ast):
        self.reset()
        self.ast = ast
        print("AST recibido en intérprete:", ast)  # Debug
        
        while self.current_index < len(ast):
            try:
                stmt = ast[self.current_index]
                print("Ejecutando statement:", stmt)  # Debug
                
                self.execute_statement(stmt)
                
                self.execution_steps.append({
                    "line": self.current_index + 1,
                    "output": self.output.copy(),
                    "variables": self.variables.copy()
                })
                
                self.current_index += 1
            except Exception as e:
                self.output.append(f"Error en línea {self.current_index + 1}: {str(e)}")
                break
        
        print("Variables finales:", self.variables)  # Debug
        print("Salida final:", self.output)  # Debug
        return self.output

    def execute_statement(self, stmt):
        if not stmt:
            return

        try:
            if stmt[0] == 'ASSIGN':
                _, var_name, expr = stmt
                value = self.evaluate_expression(expr)
                self.variables[var_name] = value

            elif stmt[0] == 'WRITE':
                _, args = stmt
                output = []
                for arg in args:
                    if isinstance(arg, (list, tuple)) and arg[0] == 'STRING':
                        output.append(str(arg[1]))
                    else:
                        output.append(str(self.evaluate_expression(arg)))
                self.output.append(" ".join(output))

            elif stmt[0] == 'IF':
                _, condition, then_block = stmt
                if self.evaluate_condition(condition):
                    for statement in then_block:
                        self.execute_statement(statement)

            elif stmt[0] == 'WHILE':
                _, condition, body = stmt
                while self.evaluate_condition(condition):
                    for statement in body:
                        self.execute_statement(statement)
                    # Actualizar condición después de ejecutar el cuerpo
                    if not self.evaluate_condition(condition):
                        break

        except Exception as e:
            self.output.append(f"Error: {str(e)}")

            
    def evaluate_condition(self, condition):
        if condition[0] == 'LOGIC':
            op = condition[1]
            left = self.evaluate_condition(condition[2])
            right = self.evaluate_condition(condition[3])
            
            if op == 'and': return left and right
            elif op == 'or': return left or right
            
        elif condition[0] == 'NOT':
            return not self.evaluate_condition(condition[1])
            
        elif condition[0] == 'COMPARISON':
            op = condition[1]
            left = self.evaluate_expression(condition[2])
            right = self.evaluate_expression(condition[3])
            
            if op == '==': return left == right
            elif op == '!=': return left != right
            elif op == '<': return left < right
            elif op == '<=': return left <= right
            elif op == '>': return left > right
            elif op == '>=': return left >= right
        
        return False

    def evaluate_expression(self, expr):
        # Debug: mostrar la expresión que se está evaluando
        print(f"Evaluando expresión: {expr}")
        
        
        
        if isinstance(expr, (list, tuple)):
            node_type = expr[0]
            
            if node_type == 'NUM':
                return expr[1]  # Valor numérico
                
            elif node_type == 'VAR':
                var_name = expr[1]
                return self.variables.get(var_name, 0)  # Valor de variable
                
            elif node_type == 'STRING':
                return expr[1]  # Cadena de texto directamente
                
            elif node_type == 'BINOP':
                op = expr[1]
                left = self.evaluate_expression(expr[2])
                right = self.evaluate_expression(expr[3])
                
                if op == '+': 
                    # Concatenación si son strings
                    if isinstance(left, str) or isinstance(right, str):
                        return str(left) + str(right)
                    return left + right
                elif op == '-': return left - right
                elif op == '*': return left * right
                elif op == '/': return left / right
        
        # Si es un número directamente
        elif isinstance(expr, (int, float)):
            return expr
            
        # Si es un string que representa un número
        elif isinstance(expr, str) and expr.isdigit():
            return int(expr)
            
        # Si es un nombre de variable
        elif isinstance(expr, str):
            return self.variables.get(expr, 0)
            
        return 0  # Valor por defecto
    def get_variables(self):
        return self.variables.copy()