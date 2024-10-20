# tests/jsongetter.py
import unittest
import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jsongetter import load



class TestJXF(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "employees": [
                {
                    "name": "John Doe",
                    "age": 30,
                    "position": "Developer",
                    "skills": ["Python", "JavaScript"],
                    "contact": {
                        "email": "john@example.com",
                        "phone": "1234567890"
                    }
                },
                {
                    "name": "Jane Smith",
                    "age": 28,
                    "position": "Designer",
                    "skills": ["Photoshop", "Illustrator"],
                    "contact": {
                        "email": "jane@example.com",
                        "phone": "0987654321"
                    }
                }
            ],
            "company": "Tech Co.",
            "founded": 2010
        }
        self.gtr = load(self.sample_data)

    def test_load(self):
        self.assertIsNotNone(self.gtr)
        self.assertEqual(self.gtr.root.key, "root")

    def test_type_string(self):
        results = self.gtr.type("name", "string")
        self.assertEqual(len(results), 2)
        self.assertIn("John Doe", results)
        self.assertIn("Jane Smith", results)

    def test_type_integer(self):
        results = self.gtr.type("age", "integer")
        self.assertEqual(len(results), 2)
        self.assertIn(30, results)
        self.assertIn(28, results)

    def test_type_array(self):
        results = self.gtr.type("skills", "array")
        self.assertEqual(len(results), 2)
        self.assertIn(["Python", "JavaScript"], results)
        self.assertIn(["Photoshop", "Illustrator"], results)

    def test_type_object(self):
        results = self.gtr.type("contact", "object")
        self.assertEqual(len(results), 2)
        self.assertIn({"email": "john@example.com", "phone": "1234567890"}, results)
        self.assertIn({"email": "jane@example.com", "phone": "0987654321"}, results)

    def test_type_nonexistent(self):
        results = self.gtr.type("nonexistent", "string")
        self.assertEqual(len(results), 0)

    def test_nearby_simple(self):
        results = self.gtr.nearby("name", "John Doe", ["age", "position"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], {"age": 30, "position": "Developer"})

    def test_nearby_nested(self):
        results = self.gtr.nearby("email", "jane@example.com", ["phone"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], {"phone": "0987654321"})

    def test_nearby_nonexistent(self):
        results = self.gtr.nearby("name", "Nonexistent", ["age", "position"])
        self.assertEqual(len(results), 0)

    def test_nearby_multiple_results(self):
        # Add another employee with the same position
        self.sample_data["employees"].append({
            "name": "Bob Johnson",
            "age": 35,
            "position": "Developer",
            "skills": ["Java", "C++"]
        })
        gtr = load(self.sample_data)
        results = gtr.nearby("position", "Developer", ["name", "age"])
        self.assertEqual(len(results), 2)
        self.assertIn({"name": "John Doe", "age": 30}, results)
        self.assertIn({"name": "Bob Johnson", "age": 35}, results)

    def test_empty_data(self):
        empty_gtr = load({})
        self.assertEqual(len(empty_gtr.root.children), 0)

    def test_nested_arrays(self):
        nested_data = {
            "matrix": [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]
        }
        nested_gtr = load(nested_data)
        results = nested_gtr.type("matrix_0", "array")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], [1, 2, 3])

    def test_deeply_nested_object(self):
        deep_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        deep_gtr = load(deep_data)
        results = deep_gtr.type("value", "string")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "deep")

    def test_type_with_multiple_types(self):
        mixed_data = {
            "values": [
                {"id": 1, "value": "string"},
                {"id": 2, "value": 100},
                {"id": 3, "value": True},
                {"id": 4, "value": 200}
            ]
        }
        mixed_gtr = load(mixed_data)
        string_results = mixed_gtr.type("value", "string")
        int_results = mixed_gtr.type("value", "integer")
        bool_results = mixed_gtr.type("value", "boolean")
        
        print("String results:", string_results)
        print("Integer results:", int_results)
        print("Boolean results:", bool_results)
        
        self.assertEqual(len(string_results), 1)
        self.assertEqual(len(int_results), 2)
        self.assertEqual(len(bool_results), 1)
        self.assertEqual(string_results[0], "string")
        self.assertIn(100, int_results)
        self.assertIn(200, int_results)
        self.assertEqual(bool_results[0], True)
    def test_type_order_maintained(self):
        ordered_data = {
            "values": [
                {"id": 1, "value": 100},
                {"id": 2, "value": "string"},
                {"id": 3, "value": 200},
                {"id": 4, "value": "another string"},
                {"id": 5, "value": 300}
            ]
        }
        ordered_gtr = load(ordered_data)
        int_results = ordered_gtr.type("value", "integer")
        string_results = ordered_gtr.type("value", "string")

        self.assertEqual(int_results, [100, 200, 300])
        self.assertEqual(string_results, ["string", "another string"])

    def test_nearby_order_maintained(self):
        ordered_data = {
            "employees": [
                {"name": "John", "age": 30, "position": "Developer"},
                {"name": "Jane", "age": 28, "position": "Designer"},
                {"name": "Bob", "age": 35, "position": "Manager"},
                {"name": "Alice", "age": 32, "position": "Developer"}
            ]
        }
        ordered_gtr = load(ordered_data)
        developer_results = ordered_gtr.nearby("position", "Developer", ["name", "age"])

        self.assertEqual(developer_results, [
            {"name": "John", "age": 30},
            {"name": "Alice", "age": 32}
        ])

if __name__ == '__main__':
    unittest.main(verbosity=2)