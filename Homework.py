def sentence_stats():
    word_list = list(raw_input("Enter Sentence:").split())
    word_count, vowel_count, consonant_count = len(word_list), 0, 0

    for word in word_list:
        for letter in word:
            if ord(letter) in [65, 69, 73, 79, 85, 97, 101, 105, 111, 117]:
                vowel_count += 1
            elif 65 <= ord(letter) <= 122:
                consonant_count += 1

    print "word count: {0}".format(word_count)
    print "vowel count: {0}".format(vowel_count)
    print "consonant count: {0}".format(consonant_count)


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


if '__main__' == __name__:
    sentence_stats()
    name_track()