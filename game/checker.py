import re

class Checker(object):
    """Simplistic solution checker."""

    def __init__(self, problem):
        self.problem = problem
        self._whitespace = re.compile(r'\s+')

    def clean(self, text):
        return re.sub(self._whitespace, '', text)

    def check_solution(self, solution):
        outfile = self.problem.out_file
        expected = outfile.read()
        outfile.close()
        return self.clean(expected) == self.clean(solution)