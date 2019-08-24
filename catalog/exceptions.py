class BorrowLimitExceeded(Exception):
    def __init__(self, message):
        super(BorrowLimitExceeded, self).__init__(message)
