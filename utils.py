import json
from typing import Union
from PIL import Image, ImageDraw, ImageFont

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

im_data = {
    "1": "./1.png",
    "2": "./2.png",
    "3": "./3.png",
    "4": "./4.png",
    "5": "./5.png",
    "6": "./6.png",
    "7": "./7.png",
    "8": "./8.png",
    "9": "./9.png",
    "0": "./0.png",
    "+": "./+.png",
    "-": "./-.png",
    "*": "./x.png",
    "=": "./=.png",
    "/": "./divide.png"
}


def create_eq_img(eq: str, title: str = "Fix by moving one matchstick", subtitle: str = "", size_factor: float = 1.0):
    eq = eq.replace(" ", "")

    width = len(eq)*(90+10)-10
    height = 165

    equation = Image.new('RGBA', (width, height), color=(255, 255, 255, 255))

    x = 0
    for char in eq:
        stick_num = Image.open(im_data[char])

        equation.paste(
            stick_num, (x, height-int((height/2)+(stick_num.size[1]/2))))
        x += 90+10

    font = ImageFont.truetype("Rubik.ttf", 40)
    font_sub = ImageFont.truetype("Rubik.ttf", 16)

    d1 = ImageDraw.Draw(equation)

    image = Image.new('RGBA', (max(width, d1.textsize(
        title, font=font)[0], d1.textsize(
        subtitle, font=font_sub)[0]), height+120), color=(0, 0, 0, 0))

    draw = ImageDraw.Draw(image)

    image.paste(equation, (int((max(width, d1.textsize(
        title, font=font)[0], d1.textsize(
        subtitle, font=font_sub)[0])-equation.size[0])/2), height+60 -
        equation.size[1]))

    t_w, t_h = draw.textsize(title, font=font)
    draw.text(((max(width, d1.textsize(
        title, font=font)[0], d1.textsize(
        subtitle, font=font_sub)[0])-t_w)/2, 0), title,
        (0, 0, 0), font=font)

    if size_factor != 1:
        image = image.resize((
            int(image.size[0]/(1/size_factor)), int(image.size[1]/(1/size_factor))), resample=Image.Resampling.NEAREST)

    if subtitle:
        t_w2, t_h2 = draw.textsize(subtitle, font=font_sub)
        draw.text(((max(width, d1.textsize(
            title, font=font)[0], d1.textsize(
            subtitle, font=font_sub)[0])-t_w2)/2, height+120-10-d1.textsize(
            subtitle, font=font_sub)[1]), subtitle,
            (0, 0, 0), font=font_sub)

    return image


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
    problem_sum = eval(problem, {'__builtins__': None})
    result_sum = eval(result, {'__builtins__': None})

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

    return f"removed a matchstick from {f'the {get_diff(num1, num1_to)} of ' if get_diff(num1, num1_to) else ''}{decode_num(num1)} (to make a {decode_num(num1_to)}) and put it into {f'the {get_diff(num2_to, num2)} of ' if get_diff(num2_to, num2) else ''}{decode_num(num2)} (to make a {decode_num(num2_to)})."
