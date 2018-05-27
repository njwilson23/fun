# fun - effects in Python

`fun` is an experimental set of types that allow chaining functions.

## Example: transformations and side-effects

```python
from fun import Just, Nothing

def get_username():
    s = input()
    if len(s) != 0:
        return Just(s)
    else:
        return Nothing

def sanitize(username):
    return "".join(char for char in username.lower() if str.isprintable(char))

def lookup_image(profile_id):
    # database logic that may raise an exception
    return image

profile_img = (get_username()
                .map(sanitize)                      # 1. Apply a transformation
                .flat_map(Try(lookup_image))        # 2. Inline a function that may
                            .on_failure(log.error)  #    raise an exception, logging
                            .to_option()            #    any errors
                )
                .otherwise(PLACEHOLDER)             # 3. Use a placeholder when no user
                .extract())                         #    image available
```
