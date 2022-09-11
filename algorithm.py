import contextlib
import json
import utils
import random
import time


def _solution_exists(result_map: dict[list, list], equation: str) -> bool:
    """
    Function checks if the solution already exists in the result dictionary

    Args:
        result_map (dict): Stores all solutions and mutations
        equation (string): The new equation to check for

    Returns:
        bool: Whether the equation exists in the result_map
    """
    return any(solution["new_equation"] == equation for solution in result_map["solutions"])


def _get_equation_matchstick_count(equation: str) -> int:
    """
    Gets the total matchstick count to check if stick was removed
    without being placed or placed without being removed

    Args:
        equation (string): The equation to check the matchstick count

    Returns:
        int: The amount of ones/sticks in the equation
    """

    equation_matchstick_count = 0

    # Loops over all chars in the equation and check the
    # amount of matchsticks that every char is built with
    for char in equation:
        with contextlib.suppress(Exception):
            equation_matchstick_count += utils.get_match_sticks_count(
                utils.encode_num(char))

    return equation_matchstick_count


def solve(equation: str) -> dict[list, list]:
    """
    Solves the matchstick equation

    Args:
        equation (str): The equation to solve

    Returns:
        dict[list, list]: The results
    """

    # ---------- SETUP ----------#
    equation_matchstick_count = _get_equation_matchstick_count(equation)

    if utils.evaluate_eq(equation):
        return {"solutions": [{"new_equation": equation, "original_equation": equation, "explanation": "Expression was already true"}], "mutations": []}

    result_map = {"solutions": [], "mutations": []}
    transform_data = None

    solutions = []
    mutations = []

    # Opens the matchstick_transform_data file that contains
    # the numbers each number can become by removing/getting/moving one stick
    with open("./matchstick_transform_data.json") as f:
        transform_data = json.load(f)

    for index, num in enumerate(equation):

        # If the number exists then continue,
        # it will filter '=' or any other invalid char
        if transform_data.get(num):

            # Loops over all the options for the numbers:
            #    - "to" (numbers you get when removing a stick from the number)
            #    - "from" (numbers you get when getting a stick from a number)
            #    - "morph" (numbers you get when moving a stick within the number)

            for opt in transform_data[num]:

                for num_opt in transform_data[num][opt]:

                    # If the option is "to" which means the number after a stick was removed
                    # then it will check what number can get a stick and create a valid equation
                    if opt == "to":

                        # Now look through all numbers in equation to check if can add stick to them
                        for index2, num2 in enumerate(equation):

                            # Again, check if the number is valid
                            if transform_data.get(num2):

                                # Loop through the current number's options after getting another stick
                                for from_num in transform_data[num2]["from"]:

                                    # Test the equation's validity with the new numbers
                                    # (the one that a stick was removed from and the one a stick was added to)
                                    new_eq = list(equation)
                                    new_eq[index2] = from_num
                                    new_eq[index] = num_opt
                                    new_eq = ''.join(new_eq)
                                    solve = utils.create_eq(new_eq)

                                    # There are multiple checks that need to be verified:
                                    #    1. Check if the equation is true - it means that 1+1=4 wont go through
                                    #    2. Check if the solution wasn't added already - because numbers lead to each other, so there can be duplicates
                                    #    4. Check if there weren't extra/less sticks than the original one - So it wont remove a stick without placing it back somewhere
                                    if solve[0] and \
                                        not _solution_exists(result_map, solve[1]) and \
                                            _get_equation_matchstick_count(new_eq) == equation_matchstick_count:

                                        result_map["solutions"].append({
                                            "new_equation": solve[1],
                                            "original_equation": equation,
                                            "explanation": utils.explanation_generator(utils.encode_num(num), utils.encode_num(num_opt), utils.encode_num(num2), utils.encode_num(from_num))
                                        })

                                    else:
                                        mutations.append({
                                            "new_equation": solve[1],
                                            "original_equation": equation,
                                        })

                    # If the option is "from" which means the number after a stick was added
                    # then it will check what number can remove a stick and create a valid equation
                    elif opt == "from":
                        continue
                        # Now look through all numbers in equation to check if can add stick to them
                        for index2, num2 in enumerate(equation):

                            # Again, check if the number is valid
                            if transform_data.get(num2):

                                # Loop through the current number's options after removing another stick
                                for from_num in transform_data[num2]["to"]:

                                    # Test the equation's validity with the new numbers
                                    # (the one that a stick was removed from and the one a stick was added to)
                                    new_eq = list(equation)
                                    new_eq[index2] = from_num
                                    new_eq[index] = num_opt
                                    new_eq = ''.join(new_eq)
                                    solve = utils.create_eq(new_eq)

                                    # There are multiple checks that need to be verified:
                                    #    1. Check if the equation is true - it means that 1+1=4 wont go through
                                    #    2. Check if the solution wasn't added already - because numbers lead to each other, so there can be duplicates
                                    #    4. Check if there weren't extra/less sticks than the original one - So it wont remove a stick without placing it back somewhere
                                    if solve[0] and \
                                        not _solution_exists(result_map, solve[1]) and \
                                            _get_equation_matchstick_count(new_eq) == equation_matchstick_count:

                                        result_map["solutions"].append({
                                            "new_equation": solve[1],
                                            "original_equation": equation,
                                            "explanation": utils.explanation_generator(utils.encode_num(num), utils.encode_num(num_opt), utils.encode_num(num2), utils.encode_num(from_num))
                                        })

                                    else:
                                        mutations.append({
                                            "new_equation": solve[1],
                                            "original_equation": equation,
                                        })

                    # If the option is "morph" which means the number after moving a stick within it self,
                    # For example 6 to 0
                    else:

                        # Test the equation's validity with the new number
                        new_eq = list(equation)
                        original = new_eq[index]
                        new_eq[index] = num_opt
                        new_eq = ''.join(new_eq)
                        solve = utils.create_eq(new_eq)

                        # There are multiple checks that need to be verified:
                        #    1. Check if the equation is true - it means that 1+1=4 wont go through
                        #    2. Check if the solution wasn't added already - because numbers lead to each other, so there can be duplicates
                        #    4. Check if there weren't extra/less sticks than the original one - So it wont remove a stick without placing it back somewhere
                        if solve[0] and \
                            not _solution_exists(result_map, solve[1]) and \
                                _get_equation_matchstick_count(new_eq) == equation_matchstick_count:

                            result_map["solutions"].append({
                                "new_equation": solve[1],
                                "original_equation": equation,
                                "explanation": utils.explanation_generator(utils.encode_num(list(equation)[index]), None, utils.encode_num(num_opt), None, morph=True)
                            })

                        else:
                            mutations.append({
                                "new_equation": solve[1],
                                "original_equation": equation
                            })

    result_map["mutations"] = mutations
    return result_map


def create_equation(answer: int = None, min_num: int = 1, max_num: int = 10, divide: bool = False, multiply: bool = False) -> dict[str, list]:
    """
    Creates a random valid equation by choosing random numbers and with them
    creating the equation

    Args:
        answer (int, optional): Set's the answer so the original's result would be the answer, example: (answer=4) 6+4=4. Defaults to None.
        min_num (int, optional): The minimum number that can show up in the equation. Defaults to 1.
        max_num (int, optional): The maximum number that can show up in the equation. Defaults to 10.
        divide (int, optional): Wether the function should generate an equation with the / sign. Defaults to False.
        multiply (int, optional): Wether the function should generate an equation with the * sign. Defaults to False.

    Returns:
        dict[str, list]: The random equation with it's answers
    """

    # Create a new equation until results in a valid one according to the equation's parameters
    while True:

        # Create the random equation
        random_num1 = random.randint(min_num, max_num)
        random_num2 = random.randint(min_num, max_num)
        random_num3 = random.randint(min_num, max_num)
        operation = random.choice(
            "+-" + '/' if divide else '' + '*' if multiply else '')
        eq = f"{random_num1}{operation}{random_num2}={answer or random_num3}"
        try:
            result = solve(eq)
        except Exception:
            continue
        if len(result["solutions"]) and not utils.evaluate_eq(eq):
            return {"equation": eq, "solutions": result["solutions"]}
