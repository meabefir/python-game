def sign(x):
    return x >= 0


def clamp(var, minn, maxx):
    return min(maxx, max(var, minn))