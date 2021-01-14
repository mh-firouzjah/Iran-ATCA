def oc(x: int):
    if x > 0:
        return oc(x // 10) + ((x % 10) % 2)
    return 0


print(oc(12345))
