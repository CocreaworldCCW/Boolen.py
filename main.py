def NOT(a):
    return 1 if a == 0 else 0
def AND(a, b):
    return 1 if a == 1 and b == 1 else 0
def OR(a, b):
    return 1 if a == 1 or b == 1 else 0
def XOR(a, b):
    return 1 if a != b else 0
# Function to evaluate Boolean expressions with nested custom functions
def evaluate_expression(expression, functions):
    def precedence(op):
        if op == '~':
            return 3
        if op in ('&', '|', '^'):
            return 2
        return 0
    def apply_operation(operators, values):
        operator = operators.pop()
        if operator == '~':
            a = values.pop()
            values.append(NOT(a))
        else:
            b = values.pop()
            a = values.pop()
            if operator == '&':
                values.append(AND(a, b))
            elif operator == '|':
                values.append(OR(a, b))
            elif operator == '^':
                values.append(XOR(a, b))
    def parse_expression(expression):
        operators, values = [], []
        i = 0
        while i < len(expression):
            if expression[i] == ' ':
                i += 1
                continue
            if expression[i] == '(':
                operators.append('(')
            elif expression[i] == ')':
                while operators and operators[-1] != '(':
                    apply_operation(operators, values)
                operators.pop()  # Pop '('
            elif expression[i] in '01':
                values.append(int(expression[i]))
            elif expression[i] in ('&', '|', '^', '~'):
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(expression[i])):
                    apply_operation(operators, values)
                operators.append(expression[i])
            else:
                # Detect custom function names and parse inputs
                func_name = ""
                while i < len(expression) and expression[i].isalnum():
                    func_name += expression[i]
                    i += 1
                if func_name in functions:
                    # Parse nested function inputs
                    func_inputs = []
                    if expression[i] == '(':
                        i += 1
                        nested_input = ""
                        balance = 1
                        while balance != 0:
                            if expression[i] == '(':
                                balance += 1
                            elif expression[i] == ')':
                                balance -= 1
                            if balance > 0:
                                nested_input += expression[i]
                            i += 1
                        nested_input_values = parse_expression(nested_input)  # Recursively parse nested function input
                        func_inputs = [nested_input_values] if isinstance(nested_input_values, int) else nested_input_values
                    # Evaluate the custom function with parsed inputs
                    result = functions[func_name].evaluate(func_inputs)
                    if result == "undefined":
                        raise ValueError(f"Undefined input for function {func_name}")
                    values.append(int(result[0]))  # Use first output for nested expressions
                    continue
                else:
                    raise ValueError(f"Function '{func_name}' is not defined.")
            i += 1
        while operators:
            apply_operation(operators, values)
        return values[-1]
    return parse_expression(expression)
# Class for defining and evaluating multi-output custom Boolean functions
class CustomBooleanFunction:
    def __init__(self, definition):
        self.truth_table = {}
        definition = definition.split(";")
        for item in definition:
            input_val, output_vals = item.split("=")
            output_vals = output_vals.strip().split()
            self.truth_table[input_val.strip()] = output_vals
    def evaluate(self, inputs):
        inputs_str = ''.join(map(str, inputs))
        return self.truth_table.get(inputs_str, ["undefined"])
# Main program loop
functions = {}
while True:
    choice = input("Choose an option:\n1. Evaluate Boolean expression\n2. Define a custom Boolean function\n3. List defined functions\n4. Exit\nEnter choice: ")
    if choice == "1":
        # Evaluate Boolean expression or custom function directly
        expression = input("Enter Boolean expression (use ~ for NOT, & for AND, | for OR, ^ for XOR, with 0 and 1 as values or custom functions): ")
        try:
            result = evaluate_expression(expression, functions)
            print(f"Result: {result}")
        except Exception as e:
            print("Error evaluating expression:", e)
    elif choice == "2":
        # Define custom Boolean function
        func_name = input("Enter a name for the custom function (e.g., 'f'): ")
        if func_name in functions:
            print(f"Function '{func_name}' is already defined. Redefining will overwrite it.")
        definition = input(f"Enter truth table for {func_name} in the format '000=1 0; 001=0 1; ...': ")
        # Create the custom function and add it to the functions dictionary
        functions[func_name] = CustomBooleanFunction(definition)
        print(f"Function '{func_name}' defined and ready to use.")
    elif choice == "3":
        # List all defined functions
        if functions:
            print("Defined functions:")
            for func_name in functions:
                print(f" - {func_name}")
        else:
            print("No functions defined yet.")
    elif choice == "4":
        print("Exiting... Goodbye!") 
        break
    else:
        print("Invalid choice, please try again.")
