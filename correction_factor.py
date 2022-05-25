def get_correction(t1: int):
    if t1 >= 4:
        return 0
    elif t1 < 4 and t1 >= -4:
        return 0.1
    elif t1 < -4 and t1 >= -10:
        return 0.2
    elif t1 < -10 and t1 >= -17:
        return 0.3
    elif t1 < -17 and t1 >= -24:
        return 0.4
    else:
        return 0.5