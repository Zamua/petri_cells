import json
import string

# Generate the keys and values
keys = list(range(-10, -36, -1))
values = list(string.ascii_lowercase[:len(keys)])

# Create the JSON object
json_object = dict(zip(keys, values))

# Convert to JSON string
json_string = json.dumps(json_object, indent=4)

print(json_string)