import re
def check(version):
    """
    Checks if a string is in the format x.y.z, AKA semantic versioning.
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))
def compare(a, b):
    """
    Compares semantic versions.
    Returns 1 if a is a higher version than b, -1 if b is a higher version than a, and 0 if both are the same.
    """
    def normalize(version):
        return [int(x) for x in version.split(".")]

    if not check(a) or not check(b):
        raise TypeError("Strings must be in the format x.y.z")

    version_a = normalize(a)
    version_b = normalize(b)

    for i in range(3):
        if version_a[i] < version_b[i]:
            return -1
        elif version_a[i] > version_b[i]:
            return 1

    return 0

