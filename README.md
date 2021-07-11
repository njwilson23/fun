# fun - hipster Python

`fun` is a peculiar way of writing Python promoting expressions, composition,
and immutable data.

It provides:

- an `Option` monad for values that may not exist
- a `Result` type for computations that may not be successful
- a `Lens` DSL for getting and modifying values in nested structures
- a decorator for currying functions
- immutable `List` and `Chain` collections
- support for recursion to arbitrary depths through an `F` type

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

## Example: Recursion

Here's a memoized function to compute Fibonacci numbers:
```python
from fun import curry

@curry
def fibc(i, n, a, b):
    if i == n - 1: return b
    else: return fib(i + 1)(n)(b)(a + b)


fib(0)(2000)(0)(1) # Raises RecursionError
```
However, it'll fail with large numbers because the maximum stack depth is
exceeded. But if we use the `F` class from `fun`, we can compute arbitrarily
large numbers:
```python
from fun import curry, F

@curry
def fibf(i, n, a, b):
    if i == n - 1: return F.pure(b)
    else:
        def f(ab):
            a, b = ab
            return fibf(i + 1)(n)(b)(a + b)
        return F.pure((a, b)).bind(f)

fibf(0)(2000)(0)(1).evaluate()
# 4224696333392304878706725602341482782579852840250681098010280137314308584370130707224123599639141511088446087538909603607640194711643596029271983312598737326253555802606991585915229492453904998722256795316982874482472992263901833716778060607011615497886719879858311468870876264597369086722884023654422295243347964480139515349562972087652656069529806499841977448720155612802665404554171717881930324025204312082516817125
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
