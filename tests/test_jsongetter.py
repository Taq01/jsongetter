# test_jsongetter_demo.py
from jsongetter import JsonGetter
import unittest


class TestJsonGetterDemo(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "flights": [
                {
                    "plane": "Boeing 737",
                    "depart": "New York",
                    "arrive": "Los Angeles",
                    "number": "FL001",
                    "time": "14:30",
                    "info": {
                        "passengers": 121,
                        "available_seats": {"A": [30, 35, 49, 66]}
                    },
                },
                {
                    "plane": "Airbus A320",
                    "depart": "Chicago",
                    "arrive": "Miami",
                    "number": "FL002",
                    "time": "10:15"
                }
            ],
            "date": "2023-05-01"
        }

    def test_type_search_depart_cities(self):
        """Test getting all departure cities"""
        depart_cities = JsonGetter.type_search(
            self.sample_data, "depart", "string")
        self.assertEqual(len(depart_cities), 2)
        self.assertIn("New York", depart_cities)
        self.assertIn("Chicago", depart_cities)

    def test_nearby_search_specific_city(self):
        """Test getting related info for a specific departure city"""
        nearby_info = JsonGetter.nearby_search(
            self.sample_data, "depart", "New York", ["number", "time"])
        self.assertEqual(len(nearby_info), 1)
        self.assertEqual(nearby_info[0], {"number": "FL001", "time": "14:30"})

    def test_type_search_date(self):
        """Test getting the date"""
        date = JsonGetter.type_search(self.sample_data, "date", "string")
        self.assertEqual(len(date), 1)
        self.assertEqual(date[0], "2023-05-01")

    def test_flights_count(self):
        """Test getting number of flights"""
        flights = JsonGetter.type_search(
            self.sample_data, "flights", "array")[0]
        self.assertEqual(len(flights), 2)

    def test_passengers_count(self):
        """Test getting passenger count for first flight"""
        flights = JsonGetter.type_search(
            self.sample_data, "flights", "array")[0]
        passengers = JsonGetter.type_search(
            flights[0], "passengers", "integer")
        self.assertEqual(len(passengers), 1)
        self.assertEqual(passengers[0], 121)

    def test_available_seats(self):
        """Test getting available seats"""
        flights = JsonGetter.type_search(
            self.sample_data, "flights", "array")[0]
        seats = JsonGetter.type_search(flights[0], "available_seats", "object")
        self.assertEqual(len(seats), 1)
        self.assertEqual(seats[0]["A"], [30, 35, 49, 66])

    def test_seat_info_nearby(self):
        """Test getting seat info using nearby search"""
        flights = JsonGetter.type_search(
            self.sample_data, "flights", "array")[0]
        seat_info = JsonGetter.nearby_search(
            flights[0], "available_seats", None, ["A"])
        self.assertEqual(len(seat_info), 1)
        self.assertEqual(seat_info[0], {"A": [30, 35, 49, 66]})

    def test_nearby_search_nested_info(self):
        """Test getting nested info structure"""
        nearby_info = JsonGetter.nearby_search(
            self.sample_data, "depart", "New York", ["info"])
        self.assertEqual(len(nearby_info), 1)
        expected = {
            "info": {
                "passengers": 121,
                "available_seats": {"A": [30, 35, 49, 66]}
            }
        }
        self.assertEqual(nearby_info[0], expected)

    def test_general_search(self):
        """Test using search_general flag to find deeply nested structures"""
        info = JsonGetter.nearby_search(
            self.sample_data, "depart", "New York", ["available_seats"], search_general=True)
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0], {"available_seats": {"A": [30, 35, 49, 66]}})

    def test_nearby_search_without_value(self):
        """Test nearby search with None value to search within the object"""
        nearby_info = JsonGetter.nearby_search(
            self.sample_data, "depart", None, ["number", "time"])
        self.assertEqual(len(nearby_info), 2)
        self.assertIn({"number": "FL001", "time": "14:30"}, nearby_info)
        self.assertIn({"number": "FL002", "time": "10:15"}, nearby_info)


if __name__ == '__main__':
    unittest.main(verbosity=2)
