from Backend.RoomDesignApp.models import Account


def handle_login(
    username: str, email: str, password: str
) -> tuple[Account | None, bool, str]:
    """
    Handles user login by checking the provided username and password.

    Args:
        username: The username of the user.
        password: The password of the user.

    Returns:
        Tuple of (success: bool, message: str)
    """
    if (not username and not email) or not password:
        return (None, False, "Username or email, and password are required")

    account_username = Account.objects.filter(username=username, email=email).first()
    account_email = Account.objects.filter(email=email).first()

    if not account_username and not account_email:
        return (None, False, "User not found")

    account = account_username if account_username else account_email

    if account and not account.check_password(password):
        return (None, False, "Invalid password")

    return (account, True, "Login successful")


def handle_register(
    email: str, username: str, password: str
) -> tuple[Account | None, bool, str]:
    """
    Handles user registration by creating a new account.

    Args:
        email: The email of the user.
        username: The username of the user.
        password: The password of the user.

    Returns:
        Tuple of (account: Account | None, success: bool, message: str)
    """
    if not email or not username or not password:
        return (None, False, "Email, username, and password are required")

    if Account.objects.filter(email=email).exists():
        return (None, False, "Email already registered")

    if Account.objects.filter(username=username).exists():
        return (None, False, "Username already taken")

    account = Account.objects.create(email=email, username=username, password=password)
    return (account, True, "Registration successful")


def handle_admin(userid: str) -> tuple[bool, str]:
    """
    Checks if the user is an admin based on their user ID.

    Args:
        userid: The ID of the user to check.

    Returns:
        Tuple of (is_admin: bool, message: str)
    """
    if not userid:
        return (False, "User ID is required")

    account = Account.objects.filter(id=userid).first()

    if not account:
        return (False, "User not found")

    if not account.is_admin:
        return (False, "User is not an admin")

    return (True, "User is an admin")
