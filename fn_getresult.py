import numpy as np

def get_result(result):
    result = np.array(result)
    result = float(result)

    if  0.5 <= result <= 1.4:
        return "Extrovert"
    elif 1.5 <= result <= 2.4:
        return "Introvert"
    elif 2.5 <= result <= 3.4:
        return "Neurotic"
    elif 3.5 <= result <= 4.4:
        return "Agreeable"
    else:
        return "Open"

print(get_result([4.2080507]))
# print(x)