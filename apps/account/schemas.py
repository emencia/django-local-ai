from ninja import Schema


class LoginFormContract(Schema):
    """Incoming data from login form post

    Args:
        username (str | None): the username
        password (str | None): the password

    Example:
        ::

        {
            "username": "lamdajoe",
            "password": "xxx48dioEjni",
        }
    """

    username: str | None
    password: str | None


class RegisterFormContract(Schema):
    """Incoming data from registration form post

    Args:
        name (str | None): the user full name
        email (str | None): the password
        password1 (str | None): the password
        password1 (str | None): the password confirmation

    Example:
        ::

        {
            "name": "lamdajoe",
            "email": "amail@example.com",
            "password1": "xxx48dioEjni",
            "password2": "xxx48dioEjni",
        }
    """

    name: str | None
    email: str | None
    password1: str | None
    password2: str | None


class StateContract(Schema):
    """Account state data

    This is returned by the /api/state endpoint called
    when the frontend app mounts to get the state of the
    user

    Args:
        is_connected (bool): if the user is connected or not
        username (str): the user username

    Example:
        ::

        {
            "is_connected": True,
            "username": "johndoe",
        }
    """

    is_connected: bool
    username: str
