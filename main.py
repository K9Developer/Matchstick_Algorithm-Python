import algorithm
import time

if __name__ == "__main__":
    print("\n----------------------------------- SOLVES FOR 6+4=4 ----------------------------------\n")

    start = time.time()
    solve_data = algorithm.solve("6+4=4")
    end = time.time()

    for solution in solve_data["solutions"]:
        print(f"    {solution['new_equation']}: {solution['explanation']}")

    print(f"\n    Solve took {round(end-start, 5)} milliseconds")

    print("\n\n--------------------------------- GENERATED EQUATION ---------------------------------\n")

    start = time.time()
    eq_data = algorithm.create_equation(
        answer=None, min_num=1, max_num=20, divide=True, multiply=True)
    end = time.time()

    print(f"    Solutions for generated equation ({eq_data['equation']}):")

    for solution in eq_data["solutions"]:
        print(f"        {solution['new_equation']}: {solution['explanation']}")

    print(f"\n    Generation took {round(end-start, 5)} milliseconds")

    print("\n\n------------------------ POSSIBLE PROBLEMS FOR SOLUTION: 0+4=4 ------------------------\n")

    start = time.time()
    eq_data = algorithm.get_problems(eq="8-4=4")
    end = time.time()

    for solution in eq_data:
        print(f"        {solution['eq']}")

    print(f"\n    Problem generation took {round(end-start, 5)} milliseconds")
