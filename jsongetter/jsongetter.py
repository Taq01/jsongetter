from .node import Node
import json

class JsonGetter:
    def __init__(self):
        self.root = Node(key="root", data_type="root")
        
    @staticmethod
    def load(data):
        jg = JsonGetter()
        jg._process_data(data, jg.root)
        return jg
        
    def _get_data_type(self, data):
        if isinstance(data, dict):
            return "object"
        elif isinstance(data, list):
            return "array"
        elif isinstance(data, str):
            return "string"
        elif isinstance(data, bool):  #
            return "boolean"
        elif isinstance(data, int):
            return "integer"
        elif isinstance(data, float):
            return "float"
        elif data is None:
            return "null"
        else:
            return str(type(data).__name__)

    def _process_data(self, data, parent_node, parent_key=None):
        data_type = self._get_data_type(data)
        
        if isinstance(data, dict):
            for key, value in data.items():
                value_type = self._get_data_type(value)
                node = Node(key=key, data_type=value_type, value=value)
                parent_node.add_child(node)
                self._process_data(value, node, key)
                
        elif isinstance(data, list):
            for index, item in enumerate(data):
                item_type = self._get_data_type(item)
                key = f"{parent_key}_{index}" if parent_key else str(index)
                node = Node(key=key, data_type=item_type, value=item)
                parent_node.add_child(node)
                self._process_data(item, node, key)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
            
        indent = "  " * level
        value_str = f", value={repr(node.value)}" if node.value is not None else ""
        type_str = f"[{node.data_type}]"
        print(f"{indent}- {node.key} {type_str}{value_str}")
        
        for child in node.children:
            self.print_tree(child, level + 1)

    def type(self, key, data_type):
        results = []
        self._type_recursive(self.root, key, data_type, results)
        return results

    def _type_recursive(self, node, key, data_type, results):
        if node.key == key and node.data_type == data_type:
            result = self._reconstruct_json(node)
            if result not in results:  # Avoid duplicates while maintaining order
                results.append(result)
        
        for child in node.children:
            self._type_recursive(child, key, data_type, results)

    def _reconstruct_json(self, node):
        if node.data_type == "object":
            return {child.key: self._reconstruct_json(child) for child in node.children}
        elif node.data_type == "array":
            return [self._reconstruct_json(child) for child in node.children]
        else:
            return node.value

    def nearby(self, search_key, search_value, nearby_keys):
        results = []
        self._nearby_recursive(self.root, search_key, search_value, nearby_keys, results)
        return results

    def _nearby_recursive(self, node, search_key, search_value, nearby_keys, results):
        if node.data_type == "object":
            found_node = None
            nearby_values = {}

            for child in node.children:
                if child.key == search_key and child.value == search_value:
                    found_node = child
                elif child.key in nearby_keys:
                    nearby_values[child.key] = child.value

            if found_node and nearby_values:
                if nearby_values not in results:  # Avoid duplicates while maintaining order
                    results.append(nearby_values)

        for child in node.children:
            self._nearby_recursive(child, search_key, search_value, nearby_keys, results)

