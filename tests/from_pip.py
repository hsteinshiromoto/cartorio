from cartorio.log import fun


@fun
def divide(num1, num2):
    return num1 / num2

@fun
def multiply(num1, num2):
    return num1 * num2

divide(10, 0)
multiply(10, 1)
