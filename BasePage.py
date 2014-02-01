import CipherV2
import Homework

if '__main__' == __name__:
    Homework.name_track()

    key_table = CipherV2.create_key_table("KRYPTOS")
    print CipherV2.decrypt_message(CipherV2.encrypt_message("ab", key_table), key_table)

    Homework.is_prefix_dictionary(raw_input("Enter a String: ").split())