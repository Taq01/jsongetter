class Node:
    def __init__(self, key=None, value=None, data_type=None):
        self.key = key
        self.value = value
        self.data_type = data_type
        self.children = []
        
    def add_child(self, child_node):
        self.children.append(child_node)
        
    def __str__(self):
        return f"Node(key={self.key}, value={self.value}, type={self.data_type})"
