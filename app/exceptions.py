class InvalidParameters(Exception):
    def __init__(self, message="Invalid Parameters."):
        self.message = message
        super().__init__(self.message)
