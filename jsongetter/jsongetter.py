# jsongetter/jsongetter.py
from .node import Node


class JsonGetter:
    def __init__(self):
        self.root = Node(key="root", data_type="root")

    @staticmethod
    def _get_data_type(data):
        if isinstance(data, dict):
            return "object"
        elif isinstance(data, list):
            return "array"
        elif isinstance(data, str):
            return "string"
        elif isinstance(data, bool):
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

    @staticmethod
    def type_search(data, key, data_type):
        """
        Directly search through data for nodes with matching key and data_type
        without needing to load into JsonGetter first
        """
        def _type_recursive(current_data, results):
            if isinstance(current_data, dict):
                for k, v in current_data.items():
                    if k == key and JsonGetter._get_data_type(v) == data_type:
                        if v not in results:
                            results.append(v)
                    if isinstance(v, (dict, list)):
                        _type_recursive(v, results)
            elif isinstance(current_data, list):
                for item in current_data:
                    _type_recursive(item, results)

        results = []
        _type_recursive(data, results)
        return results


    @staticmethod
    def nearby_search(data, search_key, search_value=None, nearby_keys=None, search_general=False):
        """
        Enhanced nearby search with optional general search behavior
        
        Args:
            data: The data to search through
            search_key: The key to search for
            search_value: Optional value to match. If None, searches within the object/array at search_key
            nearby_keys: Keys to extract
            search_general: If True, searches for nearby keys in entire object hierarchy. 
                        If False (default), only searches in the immediate vicinity
        """
        def find_keys_in_object(obj, keys):
            """Helper function to find keys anywhere in an object hierarchy"""
            result = {}

            def _recursive_find(current_obj, current_path=[]):
                if isinstance(current_obj, dict):
                    for k, v in current_obj.items():
                        if k in keys and k not in result:
                            result[k] = v
                        if isinstance(v, (dict, list)):
                            _recursive_find(v, current_path + [k])
                elif isinstance(current_obj, list):
                    for i, item in enumerate(current_obj):
                        _recursive_find(item, current_path + [i])
            _recursive_find(obj)
            return result

        def _nearby_recursive(current_data, results, current_object=None):
            if isinstance(current_data, dict):
                # Keep track of the current object that contains our search_key
                if search_key in current_data:
                    if search_value is None or current_data[search_key] == search_value:
                        if search_general:
                            # For general search, look through the entire object hierarchy
                            nearby_values = find_keys_in_object(
                                current_data, nearby_keys)
                            if nearby_values and nearby_values not in results:
                                results.append(nearby_values)
                        else:
                            # For regular search, look only at immediate level
                            nearby_values = {}
                            for key in nearby_keys:
                                if key in current_data:
                                    nearby_values[key] = current_data[key]
                                elif isinstance(current_data[search_key], dict) and key in current_data[search_key]:
                                    nearby_values[key] = current_data[search_key][key]
                                elif isinstance(current_data[search_key], list):
                                    if key.isdigit() and int(key) < len(current_data[search_key]):
                                        nearby_values[key] = current_data[search_key][int(
                                            key)]
                                    else:
                                        for item in current_data[search_key]:
                                            if isinstance(item, dict) and key in item:
                                                nearby_values[key] = item[key]
                                                break
                            if nearby_values and nearby_values not in results:
                                results.append(nearby_values)

                # Continue searching in nested structures
                for value in current_data.values():
                    if isinstance(value, (dict, list)):
                        _nearby_recursive(
                            value, results, current_object if search_general else None)

            elif isinstance(current_data, list):
                for item in current_data:
                    _nearby_recursive(
                        item, results, current_object if search_general else None)

        results = []
        _nearby_recursive(data, results)
        return results
    def get_subtree(self, path):
        """
        Get a subtree as a new JsonGetter instance based on path.
        Path can be a list of keys or a dot-separated string.
        """
        if isinstance(path, str):
            path = path.split('.')

        current_node = self.root
        for key in path:
            found = False
            for child in current_node.children:
                # Handle array indices (keys like "0", "1", etc.)
                if child.key == key or (key.isdigit() and child.key.endswith(f"_{key}")):
                    current_node = child
                    found = True
                    break
            if not found:
                raise KeyError(f"Key '{key}' not found in path")

        # Create new JsonGetter with this node as root
        new_jg = JsonGetter()
        new_jg.root = current_node
        return new_jg

    def search_results(self, results):
        """
        Create a new JsonGetter instance from search results.
        Results should be a list of dictionaries or values from previous searches.
        """
        new_jg = JsonGetter()
        new_jg.root = Node(key="root", data_type="root")

        for result in results:
            if isinstance(result, (dict, list)):
                self._process_data(result, new_jg.root)
            else:
                # Handle single values by creating a simple node
                node = Node(key="result", value=result,
                            data_type=self._get_data_type(result))
                new_jg.root.add_child(node)

        return new_jg
