import sys
import os
import inspect
import importlib

# Add project root directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_functions_and_classes(module):
    """Returns a dictionary of classes and their methods/functions."""
    functions_and_classes = {}

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            methods = [func for func in dir(obj) if callable(getattr(obj, func)) and not func.startswith("__")]
            functions_and_classes[obj.__name__] = methods
        elif inspect.isfunction(obj):
            functions_and_classes[name] = []

    return functions_and_classes

def generate_graph(module_name):
    """Generates a Graphviz DOT representation of the classes and functions in the module."""
    print(f"Module path: {module_name}")
    module = importlib.import_module(module_name)
    functions_and_classes = get_functions_and_classes(module)

    dot_output = "digraph G {\n"
    dot_output += "    node [shape=box];\n"
    dot_output += "    rankdir=LR;\n"

    for class_name, methods in functions_and_classes.items():
        dot_output += f"    {class_name} [label=\"{class_name}\"];\n"
        for method in methods:
            dot_output += f"    {class_name} -> {method};\n"

    dot_output += "}\n"
    return dot_output

def write_to_rst(dot_output, rst_file):
    """Writes the DOT output to an RST file for Sphinx."""
    with open(rst_file, 'w') as f:
        f.write(".. _function_class_relationships:\n\n")
        f.write("Function and Class Relationships\n")
        f.write("===============================\n\n")
        f.write("This graph shows the relationships between functions and their parent classes/modules.\n\n")
        f.write(".. graphviz::\n\n")
        f.write(f"    {dot_output}\n")

if __name__ == "__main__":

    module_name = "core.data.data_models.front_api_booking_object_data_model"
    rst_file = f"../docs_/source/_static/diagrams/rst_diagrams/{str(module_name).replace('.', '__')}.rst"

    dot_output = generate_graph(module_name)
    write_to_rst(dot_output, rst_file)

    print(f"Graph generated and written to {rst_file}")
