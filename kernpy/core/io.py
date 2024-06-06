import os


def _write(path, content) -> None:
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w') as f:
        f.write(content)

