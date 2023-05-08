"""Core Utilities."""
from api.core.environment import Environment
from api.core.model import HashHandler, RandomGenerator


def get_generator() -> RandomGenerator:
    """Return a RandomGenerator instance."""
    return RandomGenerator()


def get_hash_handler() -> HashHandler:
    """Return a HashHandler instance."""
    return HashHandler()


def get_environment() -> Environment:
    """Return a Environment instance."""
    return Environment()


generator = RandomGenerator()
hash_handler = HashHandler()
environment = Environment()
