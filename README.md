# fun - effects in Python

`fun` is an experimental set of types that allow chaining functions.

## Example: transformations and side-effects

```python
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
                .map(sanitize)              # Apply a transformation
                .flat_map(Try(lambda name: lookup_image(name))                  # Inline a function that may
                            .handle_failure(lambda exc: log.error(str(exc)))    # raise an exception, logging
                            .to_option()                                        # any errors
                )
                .otherwise(PLACEHOLDER)     # Use a placeholder when no user image available
                .extract())
```
