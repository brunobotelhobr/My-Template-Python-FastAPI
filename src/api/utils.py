"""General model utilities."""
import hashlib
import random
import string
from uuid import uuid4


class RandonGenerator:
    """Class to generate IDs for models."""

    def get_uuid(self) -> str:
        """Return au UUDI4."""
        return str(uuid4().hex)

    def get_salt(self) -> str:
        """Generate a 16 letters salt."""
        return "".join(random.choice(string.ascii_letters) for i in range(16))

    def get_password_hash(self, password: str, salt: str) -> str:
        """Hash a password with a salt."""
        password = password + salt
        return str(hashlib.sha256(password.encode()).hexdigest())


generator = RandonGenerator()
