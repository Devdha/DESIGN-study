class PostCommand(Command):
    def __init__(self, path, data, headers):
        self.path = path
        self.data = data
        self.headers = headers

    def execute(self):
        return self.client.post(self.path, self.data, self.headers)