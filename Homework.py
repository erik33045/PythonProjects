def name_track():
    number_of_names = int(raw_input("Enter total number of names: "))
    number_of_mistakes = 0
    name_dictionary = {}
    while number_of_names != len(name_dictionary):
        input_name = list(raw_input("Enter name: ").split())
        if len(input_name) != 2:
            number_of_mistakes += 1
            print_error("Wrong format... Should be Last, First", number_of_mistakes, False)
        elif input_name[0][-1] != ',':
            print_error("Wrong format... Should be Last, First", number_of_mistakes, True)
            name_dictionary[input_name[1]] = (input_name[0])
        else:
            name_dictionary[input_name[0][:-1]] = input_name[1]

    print "The sorted list (by last name) is: "

    sorted_keys = name_dictionary.keys()
    sorted(sorted_keys)

    for key in sorted_keys:
        print(name_dictionary[key] + " " + key)


def print_error(error_message, number_of_mistakes, auto_correct):
    print error_message

    if auto_correct:
        print "You have made {0} mistakes, fixing input.".format("string", number_of_mistakes + 1)
    else:
        print "You have made {0} mistakes, try again.".format("string", number_of_mistakes + 1)


def reverse_sentence():
    input_string = raw_input("Enter a Sentence: ")
    print ' '.join(reversed(input_string.split()))


def create_dictionary(int_list, string_list):
    print str(dict(zip(int_list, string_list)))


def input_information():
    food_dictionary = {}
    while True:
        name = raw_input("Name: ")
        if name == "":
            break
        food = raw_input("Food: ")
        if name in food_dictionary:
            food_dictionary[name].append(food)
        else:
            food_dictionary[name] = [food]
    return food_dictionary


def print_favorite_foods(food_dictionary):
    for name in food_dictionary:
        print name, " likes ",
        if len(food_dictionary[name]) == 1:
            print food_dictionary[name][0]
        else:
            print ', '.join(food_dictionary[name][:-1]) + " and " + food_dictionary[name][-1]
        print " "


def favorite_foods():
    print_favorite_foods(input_information())


def half_backwards(input_list):
    n = len(input_list) / 2
    return input_list[n:] + input_list[:n]


def one_to_one(d):
    return len(d.keys()) == len(set(d.values()))


def is_prefix_atom(l, a):
    return not [b for b in l if a.startswith(b) and a != b]


def prefix_atoms(l):
    return [a for a in l if is_prefix_atom(l, a)]


def is_prefix_dictionary(l):
    l.sort(key=len)
    d = {}
    [add_to_dictionary(d, a, l) for a in l if is_prefix_atom(l, a)]

    for item in d.items():
        print item[0] + " : " + str(item[1]),


def add_to_dictionary(d, a, l):
    d[a] = [b for b in l if b.startswith(a)]