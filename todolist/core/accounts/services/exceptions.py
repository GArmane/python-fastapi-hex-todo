class EmailNotUniqueError(Exception):
    def __init__(self, email: str, msg="email already registered"):
        super().__init__(msg)
        self.msg = msg
        self.details = {"email": email}
