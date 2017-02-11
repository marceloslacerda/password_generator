import shlex
import unittest

from subprocess import check_output

def get_output(cmd_string):
    return check_output(shlex.split(cmd_string), universal_newlines=True)

class TestCLIParser(unittest.TestCase):
    def test_listOne(self):
        output = get_output("password-generator list --db foobar.json")
        self.assertIn(
            "foo.bar",
            output)
    def test_listNone(self):
        output = get_output("password-generator list --db notexists.json")
        self.assertIn(
            "No entries",
            output)

if __name__ == '__main__':
    unittest.main()
