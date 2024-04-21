def image_size_type(size: str) -> tuple[int, int]:
    try:
        parts = size.split("x")
        if len(parts) != 2:
            raise ValueError()
        width = int(parts[0])
        height = int(parts[1])
        if width <= 0 or height <= 0:
            raise ValueError("Image width and height must be positive integers.")
        return width, height
    except ValueError:
        raise ValueError(
            "Invalid image size format. Please provide two positive integers separated by an 'x' (e.g. 320x240).")


def complex_type(r: str, i: str = None) -> complex:
    try:
        return complex(
            float(r),
            float(i) if i is not None else 0
        )
    except ValueError:
        raise ValueError(
            'Invalid complex number format. Please provide complex number in format <real>+<imaginary>j or <real>-<imaginary>j.')
