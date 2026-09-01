import json

from dataclasses import dataclass

data = {
    "name": "John Doe",
    "age": 30,
    "dateOfBirth": "1993-05-15",
    "email": "john.doe@example.com"
}

# convert json to string
json_string = json.dumps(data)
# print(json_string)

# convert string to json
parsed = json.loads(json_string)
# print(parsed["name"])

data2 = {
    "persons": [
        {
            "name": "John Doe",
            "age": 30,
            "dateOfBirth": "1993-05-15",
            "email": "john.doe@example.com"
        },
        {
            "name": "Jane Smith",
            "age": 25,
            "dateOfBirth": "1998-02-20",
            "email": "jane.smith@example.com"
        }
    ]
}

# Scenario from API - Accessing nested data
json_string2 = json.dumps(data2)

## Accessing nested data - Risky way
# print(data2["persons"][1]["name"])

# Accessing nested data - Safe way
persons = json.loads(json_string2).get("persons", [])

for person in persons:
    print(person.get("name", "Unknown"))


## Class to represent a person
@dataclass
class Person:
    name: str
    age: int
    dateOfBirth: str
    email: str

person = Person(**parsed)
# print(person)
# print(person.name)

def to_api_format(person: Person) -> dict:
    return {
        "name": person.name,
        "age": person.age,
        "dateOfBirth": person.dateOfBirth,
        "email": person.email
    }

personTemp = to_api_format(person=person)
# print(personTemp)