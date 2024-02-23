class Logger():
    def info(self, function, message):
        print('[INFO] [{}] - {}'.format(function, message))

    def error(self, function, message):
        print('[ERROR] [{}] - {}'.format(function, message))