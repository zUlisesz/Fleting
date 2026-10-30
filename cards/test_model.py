import unittest

from cards.model import AVATAR_COUNT, generate_users


class GenerateUsersTests(unittest.TestCase):
    def test_assigns_each_avatar_once_before_repeating(self):
        users = generate_users(AVATAR_COUNT * 2)

        self.assertEqual(len(users), AVATAR_COUNT * 2)
        self.assertEqual(len({user["avatar"] for user in users}), AVATAR_COUNT * 2)

    def test_accepts_an_empty_collection(self):
        self.assertEqual(generate_users(0), [])

    def test_rejects_a_negative_count(self):
        with self.assertRaises(ValueError):
            generate_users(-1)


if __name__ == "__main__":
    unittest.main()
