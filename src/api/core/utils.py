"""Core Utilities."""
import random
import string
from datetime import datetime
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from api.core.schema import Singleton


class RandomGenerator(Singleton):
    """Class to generate random values."""

    def uuid(self) -> str:
        """Return au UUDI4."""
        return str(uuid4())

    def salt(self) -> str:
        """Return a random salt."""
        return str("".join(random.choices(string.ascii_letters + string.digits, k=8)))

    def email(self) -> str:
        """Return a random email."""
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=8)) + "@example.com"

    def name(self, words: int = 3, first_caps: bool = True) -> str:
        """
        Return a random name.

        Args:
            words (int, optional): Number of words. Defaults to 3.
            first_caps (bool, optional): First letter of each word in uppercase. Defaults to True.

        Returns:
            str: Name.
        """
        name = ""
        for _ in range(words):
            if first_caps:
                name += random.choice(string.ascii_letters).upper()
            for _ in range(random.randint(3, 8)):
                name += random.choice(string.ascii_lowercase)
            name += " "
        return name[:-1]

    def password(  # pylint: disable=too-many-arguments
        self,
        size: int = 12,
        numbers: int = 1,
        special: int = 1,
        uper: int = 1,
        lower=1,
    ) -> str:
        """
        Return a random password.

        Args:
            size (int, optional): Size of password. Defaults to 12.
            numbers (int, optional): Number of numbers. Defaults to 1.
            special (int, optional): Number of special chars. Defaults to 1.
            uper (int, optional): Number of upercase chars. Defaults to 1.
            lower (int, optional): Number of lowercase chars. Defaults to 1.

        Returns:
            str: Password.
        """
        # check if the sum of the numbers, special, uper and lower is less than the size of the password
        if (numbers + special + uper + lower) > size:
            raise ValueError(
                "The sum of the numbers, special, uper and lower must be less than the size of the password."
            )
        # check if the numbers, special, uper and lower are greater than or equal to zero
        if numbers < 0 or special < 0 or uper < 0 or lower < 0:
            raise ValueError(
                "The numbers, special, uper and lower must be greater than or equal to zero."
            )

        char_set = ""
        generated_password = ""

        if numbers > 0:
            # add numbers to char_set and password
            char_set += string.digits
            generated_password += random.choice(string.digits) * numbers

        if special > 0:
            # add special chars to char_set and password
            char_set += string.punctuation
            generated_password += random.choice(string.punctuation) * special

        if uper > 0:
            # add upercase chars to char_set and password
            char_set += string.ascii_uppercase
            generated_password += random.choice(string.ascii_uppercase) * uper

        if lower > 0:
            # add lowercase chars to char_set and password
            char_set += string.ascii_lowercase
            generated_password += random.choice(string.ascii_lowercase) * lower

        # add the remaining chars to password
        generated_password += "".join(
            random.sample(char_set, size - len(generated_password))
        )

        return generated_password

    def now(self) -> datetime:
        """Return a datetime object with the current date and time."""
        return datetime.now()


class HashHandler(Singleton):
    """Class to handle passords hashs."""

    def generate_hash(self, password: str) -> str:
        """Return a hashed password."""
        return str(PasswordHasher().hash(password))  # pylint: disable=redefined-builtin
        # PyLint W0622: Redefining built-in 'hash' (redefined-builtin)

    def verify_hash(
        self, password: str, hash: str
    ) -> bool:  # pylint: disable=redefined-builtin
        # PyLint W0622: Redefining built-in 'hash' (redefined-builtin)
        """Verify if the hash is valid."""
        try:
            return PasswordHasher().verify(hash=hash, password=password)
        except VerifyMismatchError:
            return False


generator = RandomGenerator()
hash_handler = HashHandler()
