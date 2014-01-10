import unittest


def is_a_palindrome(input_string):
    return input_string == input_string[:: -1]


def is_an_anagram(first_string, second_string):
    x = list("".join(first_string.split()))
    y = list("".join(second_string.split()))
    if x.__len__() != y.__len__():
        return False
    for _ in list(x):
        if _ not in y:
            return False
    return True


class UnitTests(unittest.TestCase):
    def test_palindrome_pass(self):
        self.assertEqual(True, is_a_palindrome("wiw"))

    def test_palindrome_fail(self):
        self.assertEqual(False, is_a_palindrome("wiz"))

    def test_anagram_equal_string_length_anagram_returns_true(self):
        self.assertEqual(True, is_an_anagram("with", "ithw"))

    def test_anagram_equal_string_length_nonanagram_returns_false(self):
        self.assertEqual(False, is_an_anagram("with", "itha"))

    def test_anagram_non_equal_strings_return_false(self):
        self.assertEqual(False, is_an_anagram("with", "ith"))

    def test_anagram_ignores_whitespace(self):
        self.assertEqual(True, is_an_anagram("w\ni\t\t\tth  ", "ithw"))


if __name__ == '__main__':
    unittest.main()