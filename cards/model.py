"""Generación de perfiles de usuario falsos"""
import random
from typing import TypedDict

from faker import Faker

AVATAR_COUNT = 6
AVATARS = tuple(
    f"/{gender}_{index}.png"
    for gender in ("woman", "man")
    for index in range(1, AVATAR_COUNT + 1)
)

class User(TypedDict):
    name: str
    phone: str
    avatar: str
    address: str


def available_avatars(random_source: random.Random | None = None) -> list[str]:
    """Return one shuffled cycle containing every available avatar."""
    avatars = list(AVATARS)
    (random_source or random).shuffle(avatars)
    return avatars


def make_user(avatar: str, generator: Faker) -> User:
    """Create a user whose name matches the gender represented by its avatar."""
    if avatar not in AVATARS:
        raise ValueError("El avatar no pertenece al catálogo disponible.")
    if avatar.startswith("/woman_"):
        first_name = generator.first_name_female()
    else:
        first_name = generator.first_name_male()
    return {
        "name": f"{first_name} {generator.last_name()} {generator.last_name()}",
        "phone": generator.phone_number(),
        "avatar": avatar,
        "address": generator.address(),
    }


def generate_users(count: int = 5, *, seed: int | None = None) -> list[User]:
    """Generate users with repeatable data when an optional seed is provided."""
    if type(count) is not int or count < 0:
        raise ValueError("El número de usuarios no puede ser negativo.")

    users: list[User] = []
    avatars: list[str] = []
    random_source = random.Random(seed) if seed is not None else None
    generator = Faker("es")
    if seed is not None:
        generator.seed_instance(seed)
    for _ in range(count):
        if not avatars:
            avatars = available_avatars(random_source)
        users.append(make_user(avatars.pop(), generator))
    return users
