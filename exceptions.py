class UserNotFoundException(Exception):
    detail = 'User not found'


class UserIncorrectPasswordException(Exception):
    detail = 'Incorrect password'


class TokenExpiredException(Exception):
    detail = 'Token has expired'


class InvalidTokenException(Exception):
    detail = 'Token is invalid'


class TaskNotFound(Exception):
    detail = 'Task not found'
