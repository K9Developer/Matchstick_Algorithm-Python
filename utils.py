import json
from py_expression.core import Exp
from typing import Union

exp = Exp()

explanation_map = {
    "00": "top left",
    "01": "top",
    "02": "top right",
    "10": "bottom left",
    "11": "middle",
    "12": "bottom right",
    "13": "bottom"
}

number_format = list[list[int, int, int], list[int, int, int, int]]

with open('stickData.json') as f:
    number_data = json.load(f)


def get_match_sticks_count(num: Union[number_format, str]) -> int:
    """
    Gets the number of ones in the number

    Args:
        num (Union[number_format, str]): The number in the custom format or string for "plus" and "minus"

    Returns:
        int: The number of ones/sticks it found in the number
    """

    amount = 0

    if num == "plus":
        return 2
    elif num == "minus":
        return 1

    for row in num:
        for col in row:
            if col == 1:
                amount += col

    return amount


def decode_num(number: number_format) -> str:
    """
    Converts a number from the custom format to the number itself

    Args:
        number (number_format): The number to convert

    Returns:
        str: The converted number
    """

    for num in number_data["data"]:
        if number_data["data"][num] == number:
            return num


def encode_num(number: str) -> number_format:
    """
    Convert a number to the custom format

    Args:
        number (str): The number to convert

    Returns:
        number_format: The converted number in the custom format
    """

    return number_data["data"].get(number)


def evaluate_eq(eq: str) -> bool:
    """
    Evaluates an equation and returns if the equation is True

    Args:
        eq (str): The equation to evaluate

    Returns:
        bool: Whether the equation is true
    """

    # Splits the result and problem
    eq = eq.replace("x", "*")
    eq = eq.replace("X", "*")
    result = eq.split("=")[-1]
    problem = eq.split("=")[0]

    # Solves the two equations
    parsed_problem = exp.parse(problem)
    problem_sum = exp.eval(parsed_problem)
    parsed_result = exp.parse(result)
    result_sum = exp.eval(parsed_result)

    return problem_sum == result_sum


def create_eq(original: str) -> list[bool, str]:
    return [evaluate_eq(original), original]


def get_diff(num1: number_format, num2: number_format) -> str:
    """
    Returns the location of where num1 has gotten/removed a stick

    Args:
        num1 (number_format): The number that the operation was done on
        num2 (number_format): The number that was effected by the operation done on num1

    Returns:
        str: Returns the location of where num1 has gotten/removed a stick
    """

    for row_index, (row_org, row_new) in enumerate(zip(num1, num2)):
        for col_index, (col_org, col_new) in enumerate(zip(row_org, row_new)):
            if col_org == 1 and col_new == 0:

                return explanation_map[f"{row_index}{col_index}"]
    return ""


def explanation_generator(num1: number_format, num1_to: number_format, num2: number_format, num2_to: number_format, morph: bool = False) -> str:
    """
    Generates a detailed explanation on how to solve the equation

    Args:
        num1 (number_format): The original number from the equation that the operation was done on (remove/add)
        num1_to (number_format): What number the number in the place of num1 has become
        num2 (number_format): The original number from the equation that was effected by the action done on num1
        num2_to (number_format): What number the number in the place of num2 has become
        morph (bool, optional): Whether the the number has changed only within itself. Defaults to False.

    Returns:
        str: A detailed description of what to do to solve the equation
    """

    if morph:
        return f"moved {f'the {get_diff(num1, num2)} of ' if get_diff(num2, num1) else ''}{decode_num(num1)} to it's {get_diff(num2, num1)} to make a {decode_num(num2)}"

    # relative to new
    operation = "removed" if get_match_sticks_count(
        num1) < get_match_sticks_count(num2) else "got"

    if operation == "removed":
        return f"removed a matchstick from {f'the {get_diff(num2, num2_to)} of ' if get_diff(num2, num2_to) else ''}\"{decode_num(num2)}\" (to make a \"{decode_num(num2_to)}\") and put it into the {get_diff(num1_to, num1)} of \"{decode_num(num1)}\" (to make a \"{decode_num(num1_to)}\")."

    else:
        return f"added a matchstick to {f'the {get_diff(num2, num2_to)} of ' if get_diff(num2, num2_to) else ''}\"{decode_num(num2_to)}\" (to make a \"{decode_num(num2)}\") from the {get_diff(num1_to, num1)} of \"{decode_num(num1_to)}\" (to make a \"{decode_num(num1)}\")."
