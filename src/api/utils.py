"""General model utilities."""
import hashlib
import random
import string
from uuid import uuid4


class RandonGenerator:
    """Class to generate IDs for models."""

    def uuid(self) -> str:
        """Return au UUDI4."""
        return str(uuid4().hex)

    def salt(self) -> str:
        """Return a random salt."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    def email(self) -> str:
        """Return a random email."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=8)) + "@example.com"

    def name(self, words: int = 3, first_caps: bool = True) -> str:
        """
        Summary:
            Return a random name.

        Args:
            words (int, optional): Number of words. Defaults to 3.
            first_caps (bool, optional): First letter of each word in uppercase. Defaults to True.

        Returns:
            str: Name.

        Example:
            >>> from api.utils import generator
            >>> generator.name()
            'John Doe Carl'
            >>> generator.name(words=2, first_caps=False)
            'john doe'
        """
        name = ""
        for _ in range(words):
            n = random.choice(string.ascii_letters) * 8
            if first_caps:
                n = n.capitalize()
            name = name + n
            if _ != words - 1:
                name = name + " "
        return name

    def password(self, size: int = 12, numbers: int = 1, special: int = 1, uper: int = 1, lower=1) -> str:
        """
        Summary:
            Return a random password.

        Args:
            size (int, optional): Size of password. Defaults to 12.
            numbers (int, optional): Number of numbers. Defaults to 1.
            special (int, optional): Number of special chars. Defaults to 1.
            uper (int, optional): Number of upercase chars. Defaults to 1.
            lower (int, optional): Number of lowercase chars. Defaults to 1.

        Returns:
            str: Password.

        Example:
            >>> from api.utils import generator
            >>> generator.password()
            '1@2a3B4c5D6e7F'

        """
        # check if the sum of the numbers, special, uper and lower is less than the size of the password
        if (numbers + special + uper + lower) > size:
            raise ValueError(
                "The sum of the numbers, special, uper and lower must be less than the size of the password."
            )
        # check if the numbers, special, uper and lower are greater than or equal to zero
        if numbers < 0 or special < 0 or uper < 0 or lower < 0:
            raise ValueError("The numbers, special, uper and lower must be greater than or equal to zero.")

        char_set = ""
        password = ""

        if numbers > 0:
            # add numbers to char_set and password
            char_set += string.digits
            password += random.choice(string.digits) * numbers

        if special > 0:
            # add special chars to char_set and password
            char_set += string.punctuation
            password += random.choice(string.punctuation) * special

        if uper > 0:
            # add upercase chars to char_set and password
            char_set += string.ascii_uppercase
            password += random.choice(string.ascii_uppercase) * uper

        if lower > 0:
            # add lowercase chars to char_set and password
            char_set += string.ascii_lowercase
            password += random.choice(string.ascii_lowercase) * lower

        # add the remaining chars to password
        password += "".join(random.sample(char_set, size - len(password)))

        return password

    def hasher(self, password: str, salt: str) -> str:
        """Return a hashed password."""
        return str(hashlib.sha256(password.encode() + salt.encode()).hexdigest())


generator = RandonGenerator()
