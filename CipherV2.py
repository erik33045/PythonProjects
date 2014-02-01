def create_key_table(key_string):
    """input is the keyphrase. The keyphrase may contain at most one of each alphabetic character
       return is a table containing the rotation for each letter given by the key"""
    key_list = [letter for letter in key_string]

    if len(key_list) < 26:
        letter = 65
        while len(key_list) < 26:
            if chr(letter) not in key_list:
                key_list.append(chr(letter))
            letter += 1

    return key_list


def encrypt_message(message, key_table):
    """message is a set of alphabetic characters with no spaces
       key_table is the generated table from the earlier function
       return is the encrypted message"""
    return ''.join([key_table[ord(letter) - 65] for letter in message.upper()].__reversed__())


def decrypt_message(message, key_table):
    """message is a set of alphabetic characters with no spaces
       key_table is the generated table from the earlier function
       return is the decrypted message"""
    return ''.join([chr(key_table.index(letter) + 65) for letter in message.upper()].__reversed__())