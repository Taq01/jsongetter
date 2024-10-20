<div align="center" style="text-align: center;">


# JSON GETTER
<p>
<b>
jsongetter a headache-free way for dynamic search&retrieve through large JSON datasets.
</p>
</div>

## Installation

You can install the library using pip:

```
pip install jsongetter
```


## Mehtods & Notes
```
my_data=jg.load(json_data) 
by_type_value=my_data.type("key", "value_type")
by_nearby_value = my_data.nearby("key", "value", ["key_1", "key_2"...])

```
Types:
-**object**
-**array**
-**string**
-**boolean**
-**integer**
-**float**
-**null**


### Note
You can always narrow the search scope for a given case by reloading data (object) through the load().<br>
However, the library currently cannot handle matching of multiple objects and only returns the first object it encounters, even if there are "nested".

given_object<br>
+--key_1<br>
  -----+----key_object_match_sub<br>
+--key_object_match<br>

#key_object_match_sub returned<br>

## Usage


```
import jsongetter as jg
import json


sample_data = {
    "flights": [
        {
            "plane": "Boeing 737",
            "depart": "New York",
            "arrive": "Los Angeles",
            "number": "FL001",
            "time": "14:30",
            "info":{"passengers":121,"available_seats":{"A":[30,35,49,66]}},
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

jg=jg.load(sample_data) #load json data

#Return all values that match key&value
depart_results = jg.type("depart", "string")
print(json.dumps(depart_results, indent=2))
#output:
# [
#   "New York",
#   "Chicago"
# ]

#Since the library uses tree structure, nearby is horizontal search at sub-keyParent level and lower
nearby_results = jg.nearby("depart", "New York", ["number", "time"])
print(json.dumps(nearby_results, indent=2))
#output:
# [
#   { 
#     "number": "FL001",
#     "time": "14:30"
#   }
# ]

date=jg.type("date","string")
print(date)#['2023-05-01']
how_many_flights=jg.type('flights',"array")[0]
print(len(how_many_flights))#2

first_flight=jg.load(how_many_flights[0]) #narrowing the search scope
print(first_flight.type("passengers","integer"))#[121]
print(first_flight.type("available_seats","object")[0]['A'])#[30, 35, 49, 66]
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

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