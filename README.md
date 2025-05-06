<div align="center" style="text-align: center;">
# JSON GETTER
<p>
<b>
JsonGetter: A headache-free way for dynamic search & retrieve through large JSON datasets.
</b>
</p>
</div>

## Installation

install using pip:

```bash
pip install jsongetter
```

## Methods
JsonGetter provides two main static methods for searching through JSON data:

```python
from jsongetter import JsonGetter

# Search for values based on a specific key name and value type.
type_results = JsonGetter.type_search(data, "key", "value_type")

# Search for values that are nearby a specified key name. This method retrieves objects based on the key name.
nearby_results = JsonGetter.nearby_search(data, "key", "value", ["key_1", "key_2"...])

# When search_general=True is set, the search is not limited to nearby values in the JSON structure. 
# This allows for finding keys at any depth within the specified object.
nearby_results_deep = JsonGetter.nearby_search(data, "key", "value", ["key_1", "key_2"...], search_general=True)

```
## 

### Supported Types:
- **object**
- **array**
- **string**
- **boolean**
- **integer**
- **float**
- **null**

## Usage

```python
from jsongetter import JsonGetter

sample_data = {
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

# Retrieve all unique departure cities from the sample data.
depart_cities = JsonGetter.type_search(sample_data, "depart", "string")
print(depart_cities)  # Output: ["New York", "Chicago"]

# Get related flight information for a specific departure city.
nearby_info = JsonGetter.nearby_search(
    sample_data, "depart", "New York", ["number", "time"]
)
print(nearby_info)  # Output: [{"number": "FL001", "time": "14:30"}]

# Retrieve the date of the flights.
date = JsonGetter.type_search(sample_data, "date", "string")
print(date)  # Output: ['2023-05-01']

# Count the total number of flights available in the sample data.
flights = JsonGetter.type_search(sample_data, "flights", "array")[0]
print(len(flights))  # Output: 2

# Get the number of passengers for the first flight.
passengers = JsonGetter.type_search(flights[0], "passengers", "integer")
print(passengers)  # Output: [121]

# Retrieve the available seats for the first flight.
seats = JsonGetter.type_search(flights[0], "available_seats", "object")
print(seats[0]['A'])  # Output: [30, 35, 49, 66]

# Use nearby_search to get seat information.
seat_info = JsonGetter.nearby_search(
    flights[0], "available_seats", None, ["A"]
)
print(seat_info)  # Output: [{"A": [30, 35, 49, 66]}]

# Get flight information related to a specific departure city.
nearby_info = JsonGetter.nearby_search(
    sample_data, "depart", "New York", ["info"]
)
print(nearby_info)  # Output: [{"info": {"passengers": 121, "available_seats": {"A": [30, 35, 49, 66]}}}]

# Perform a deep search to find available seats, even if they are nested within other objects.
deep_seats = JsonGetter.nearby_search(
    sample_data, "depart", "New York", ["available_seats"], search_general=True
)
print(deep_seats)  # Output: [{"available_seats": {"A": [30, 35, 49, 66]}}]

```



## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# LICENSE
MIT License

Copyright (c) [2024] [Taq01]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.