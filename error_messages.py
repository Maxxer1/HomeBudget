from enum import Enum


class ErrorMessage(Enum):
    LOGIN_CREDENTIALS_INVALID = "E-mail or password not valid"
    PASSWORD_DONT_MATCH = "Passwords are not the same"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    EMAIL_ALREADY_EXISTS = "E-mail already exists"
    CATEGORY_ALREADY_EXISTS = "Category already exists"
    ACCOUNT_ALREADY_EXISTS = "Account already exists"

