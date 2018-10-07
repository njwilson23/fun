# fun - more functional Python

`fun` is a peculiar way of writing Python promoting functions, expressions, and
immutable data.

It provides:

- an `Option` monad for values that may not exist
- a `Result` monad for computations that may not be successful
- a `Lens` DSL for getting and modifying values in nested structures

## Example: Transformations and Errors

```python
from fun import Try, Just, Nothing

def get_username():         # This function returns an Option, which is
    s = input()             # a type with two subclasses, Just and Nothing.
    if len(s) != 0:
        return Just(s)
    else:
        return Nothing

def sanitize(username):
    return "".join(char for char in username.lower() if str.isprintable(char))

def lookup_image(profile_id):
    # database logic that may raise an exception
    return image

# We can chain operations over the Option returned by `get_username()` to handle
# a sequence of operations as a single expression
profile_img = (get_username()
                .map(sanitize)                      # 1. Apply a transformation
                .flat_map(Try(lookup_image))        # 2. Inline a function that may
                            .on_failure(log.error)  #    raise an exception, logging
                            .to_option()            #    any errors
                )
                .extract_or_else(PLACEHOLDER)       # 3. Use a placeholder when no user
```

## Example: Optics

```python
from fun import Lens

nested_dict = {
    "address": {
        "country": "foo",
        "street": {
            "name": "bar",
            "number": 123
        }
    }
}

lens = Lens["address"]["street"]["name"]
lens.set("baz")     # returns a modified copy

    {
        "address": {
            "country": "foo",
            "street": {
                "name": "baz",
                "number": 123
            }
        }
    }

people = [
    {"name": "alfonso", birthday: "April 1"},
    {"name": "brie", birthday: "Oct 17"},
    {"name": "clementine", birthday: "June 3"},
]

lens = Lens.for_all["birthday"]
lens.get(people)

    [
        "April 1",
        "Oct 17",
        "June 3",
    ]
```

## Limitations

- Sometimes the syntax is awkward
- If you're not careful, it's easy to blow through the recursion limit
