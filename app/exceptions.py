class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message

        super().__init__(message)

    def __str__(self):
        return f"NotFoundError: {self.message}"


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

        super().__init__(message)

    def __str__(self):
        return f"ValidationError: {self.message}"
