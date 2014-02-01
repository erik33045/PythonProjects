import random


def fibonacci(n):
    a, b = 0, 1
    for i in range(0, n):
        a, b = b, a + b
    return a


def find_greatest_common_fibonacci_divisor(number):
    common_divisor, fibonacci_number, iterator = 1, 1, 1

    while True:
        if fibonacci_number > number:
            break
        elif number % fibonacci_number is 0:
            common_divisor = fibonacci_number

        iterator += 1
        fibonacci_number = fibonacci(iterator)

    return common_divisor


def rotate_words(word_list, decrypting):
    if len(word_list) > 127:
        amount_to_rotate = len(word_list) % 127
    else:
        amount_to_rotate = 127 % len(word_list)

    if amount_to_rotate == 0:
        amount_to_rotate = 1

    if decrypting:
        amount_to_rotate = amount_to_rotate * -1

    for i in range(len(word_list)):
        new_word = ""
        for letter in word_list[i]:
            new_letter = ord(letter) + amount_to_rotate
            if new_letter > 126:
                new_word = new_word + chr((ord(letter) + amount_to_rotate) - 94)
            elif new_letter < 33:
                new_word = new_word + chr((ord(letter) + amount_to_rotate) + 94)
            else:
                new_word = new_word + chr((ord(letter) + amount_to_rotate))
        word_list[i] = new_word

    return word_list


def modify_word_length(word_list, number_of_letters_to_change, adding_letters):
    if adding_letters:
        for i in range(len(word_list)):
            for n in range(number_of_letters_to_change):
                if n % 2 == 0:
                    word_list[i] = chr(random.randint(33, 126)) + word_list[i]
                else:
                    word_list[i] = word_list[i] + chr(random.randint(33, 126))
    else:
        for i in range(len(word_list)):
            for n in range(number_of_letters_to_change):
                if n % 2 == 0:
                    word_list[i] = word_list[i][1:]
                else:
                    word_list[i] = word_list[i][:-1]


def cipher():
    message = raw_input("Enter the message to be encrypted: ")
    word_list = message.split()
    word_count = len(word_list)
    decrypting = False

    if len(word_list) > 127:
        amount_to_rotate = len(word_list) % 127
    else:
        amount_to_rotate = 127 % len(word_list)

    if amount_to_rotate == 0:
        amount_to_rotate = 1

    letters_to_change = max(5, find_greatest_common_fibonacci_divisor(word_count))

    #If this condition is true, we are decrypting
    if chr(ord(word_list[0][0]) - amount_to_rotate) == "@" and chr(ord(word_list[-1][-1]) - amount_to_rotate) == "@":
        word_list[0] = word_list[0][1:]
        word_list[-1] = word_list[-1][:-1]
        modify_word_length(word_list, letters_to_change, False)
        decrypting = True
    else:
        modify_word_length(word_list, letters_to_change, True)
        word_list[0] = "@" + word_list[0]
        word_list[-1] += "@"

    for word in rotate_words(word_list, decrypting):
        print word,
    print


if __name__ == '__main__':
    while True:
        cipher()
