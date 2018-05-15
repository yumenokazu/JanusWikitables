class NoTableFoundException(Exception):
    def __init__(self):
        self.message = "No tables with class='wikitable' found on the specified page"

    def __str__(self):
        return self.message


class HTTPStatusError(Exception):
    def __init__(self, status):
        self.message = f'HTTP Status returned:{status}'

    def __str__(self):
        return self.message
