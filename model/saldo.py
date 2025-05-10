class Saldo:
    def __init__(self, username, saldo):
        self.username = username
        self.saldo = saldo

    def to_line(self):
        return f"{self.username},{self.saldo}\n"
