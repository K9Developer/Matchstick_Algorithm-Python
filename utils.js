
const explanation_map = {
    "00": "top left",
    "01": "top",
    "02": "top right",
    "10": "bottom left",
    "11": "middle",
    "12": "bottom right",
    "13": "bottom"
};

let number_data = {
    "data": { "1": [[1, 0, 0], [1, 0, 0, 0]], "2": [[0, 1, 1], [1, 1, 0, 1]], "3": [[0, 1, 1], [0, 1, 1, 1]], "4": [[1, 0, 1], [0, 1, 1, 0]], "5": [[1, 1, 0], [0, 1, 1, 1]], "6": [[1, 1, 0], [1, 1, 1, 1]], "7": [[0, 1, 1], [0, 0, 1, 0]], "8": [[1, 1, 1], [1, 1, 1, 1]], "9": [[1, 1, 1], [0, 1, 1, 1]], "0": [[1, 1, 1], [1, 0, 1, 1]], "+": "plus", "-": "minus" }
};

const ordinal = (n) => {
    let s = ["th", "st", "nd", "rd"],
        v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

const get_count_of_num = (num, num_to, eq_before, eq_after) => {
    /*Gets the count number of the edited number.
    example (eq="6+4=4", our target is the last 4). it would return 2nd.
    It does that by checking whether the number at the index of the original equation (`eq_before`) is `num`
    and checks if at the same index the edited number (`num_to`) is equal to the value at index of the edited equation (`eq_after`)

    Args:
        num (int): The original number of the equation
        num_to (int): The number the original number changed to
        eq_before (str): The original equation
        eq_after (str): The edited equation

    Returns:
        str: The ordinal (1st, 2nd, etc) number of the edited number
    */

    let num_count = 0

    for (let [index, [n_before, n_after]] in zip([eq_before, eq_after]).entries()) {
        if (n_before == num) {
            num_count += 1
        }

        if (len(num) > 1 && index > 0 && num == eq_before[index - 1] + n_before && len(num_to) > 1 && num_to == eq_after[index - 1] + n_after || n_before == num && n_after == num_to) {
            return num_count
        }
    }
}

const draw_eq = async (eq, canvas, title = "Can You Fix This By Moving Only One Matchstick?", subtitle = "Created By K9Dev (KingOfTNT10.github.io)") => {


    const ctx = canvas.getContext('2d');
    ctx.font = '30px Arial';

    let width = Math.max(eq.length * (90 + 20), ctx.measureText(title).width + 100)
    ctx.font = '17px Arial';
    width = Math.max(width, ctx.measureText(subtitle).width)
    canvas.width = width
    canvas.height = 300
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    eq = eq.replace("*", "x").replace("X", "x")
    const eq_list = eq.split("")


    for (let i of eq.split("")) {
        let image = document.getElementById(i == "/" ? "divide" : i);
        ctx.drawImage(image, ((canvas.width - (eq.length * (90 + 10))) / 2) + 10 + eq_list.indexOf(i) * image.width + 10, canvas.height / 2 - image.height / 2)
        eq_list[eq_list.indexOf(image.id)] = null
    }
    if (title) {
        ctx.font = '30px Arial';
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center'
        ctx.fillText(title, canvas.width / 2, 50);
    }
    if (subtitle) {
        ctx.font = '15px Arial';
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center'
        ctx.fillText(subtitle, canvas.width / 2, canvas.height - 10);
    }

}

// draw_eq("6+4=4", document.getElementById("c-img"))

const get_match_sticks_count = (num) => {
    /*
    Gets the number of ones in the number
 
    Args:
        num (Union[number_format, str]): The number in the custom format or string for "plus" and "minus"
 
    Returns:
        int: The number of ones/sticks it found in the number
    */

    let amount = 0

    if (num == "plus") {
        return 2
    }
    else if (num == "minus") {
        return 1
    }

    for (let row of num) {
        for (let col of row) {
            if (col == 1) {
                amount += col
            }
        }
    }

    return amount
}

const decode_num = async (number) => {
    /*
    Converts a number from the custom format to the number itself
    
    Args:
        number (number_format): The number to convert
    
    Returns:
        str: The converted number
    */

    if (typeof number != "object") {
        return number
    }

    for (let num in number_data.data) {
        if (number_data.data[num] == number) {
            return num
        }
    }
}

const encode_num = async (number) => {
    /*
    Convert a number to the custom format
    
    Args:
        number (str): The number to convert
    
    Returns:
        number_format: The converted number in the custom format
        */

    return number_data.data[number]
}

const evaluate_eq = (eq) => {
    /*
    Evaluates an equation and returns if the equation is True
    
    Args:
        eq (str): The equation to evaluate
    
    Returns:
        bool: Whether the equation is true
    */

    // Splits the result and problem
    eq = eq.replace("x", "*")
    eq = eq.replace("X", "*")
    let result = eq.split("=")[eq.split("=").length - 1]
    let problem = eq.split("=")[0]

    // Solves the two equations
    let problem_sum = math.evaluate(problem)
    let result_sum = math.evaluate(result)

    return problem_sum == result_sum
}

const create_eq = (original) => {
    return [evaluate_eq(original.replace("--", "+")), original.replace("--", "+")]
}

const zip = (arrays) => {
    // console.log(arrays)
    return arrays[0].map(function (_, i) {
        return arrays.map(function (array) { return array[i] })
    });
}

const get_diff = (num1, num2) => {
    /*
    Returns the location of where num1 has gotten/removed a stick
    
    Args:
        num1 (number_format): The number that the operation was done on
        num2 (number_format): The number that was effected by the operation done on num1
    
    Returns:
        str: Returns the location of where num1 has gotten/removed a stick
    */

    // // console.log(num1)

    if (num1 == "plus" || num1 == "minus") {
        return ''
    }

    for (const [row_index, [row_org, row_new]] of zip([num1, num2]).entries()) {
        for (const [col_index, [col_org, col_new]] of zip([row_org, row_new]).entries()) {
            if (col_org == 1 && col_new == 0) {
                // // console.log(explanation_map[`${row_index}${col_index}`])
                return explanation_map[`${row_index}${col_index}`]
            }
        }
    }
    return ""
}

const explanation_generator = async (num1, num1_to, num2, num2_to, morph = false) => {
    /*
    Generates a detailed explanation on how to solve the equation
    
    Args:
        num1 (number_format): The original number from the equation that the operation was done on (remove/add)
        num1_to (number_format): What number the number in the place of num1 has become
        num2 (number_format): The original number from the equation that was effected by the action done on num1
        num2_to (number_format): What number the number in the place of num2 has become
        morph (bool, optional): Whether the the number has changed only within itself. Defaults to False.
    
    Returns:
        str: A detailed description of what to do to solve the equation
    */
    // console.log(num1, num1_to, num2, num2_to)
    if (morph) {
        return `moved ${get_diff(num2, num1) ? 'the ' + get_diff(num1, num2) + ' of ' : ''}${await decode_num(num1)} to it's ${get_diff(num2, num1)} to make a ${await decode_num(num2)}.`
    }

    return `removed a matchstick from ${get_diff(num2, num2_to) ? 'the ' + get_diff(num2, num2_to) + ' of ' : ''} ${await decode_num(num2)} (to make a ${await decode_num(num2_to)}) and put it into the ${get_diff(num1_to, num1)} of ${await decode_num(num1)} (to make a ${await decode_num(num1_to)}).`

}

export {
    explanation_generator, create_eq, decode_num, encode_num, get_match_sticks_count, evaluate_eq, draw_eq
}
