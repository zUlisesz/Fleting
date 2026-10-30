import random

from faker import Faker


AVATAR_COUNT = 6
fake = Faker("es")


def available_avatars() -> list[str]:
    """Return one shuffled cycle containing every available avatar."""
    avatars = [
        f"/{gender}_{index}.png"
        for gender in ("woman", "man")
        for index in range(1, AVATAR_COUNT + 1)
    ]
    random.shuffle(avatars)
    return avatars


def make_user(avatar: str) -> dict[str, str]:
    """Create a user whose name matches the gender represented by its avatar."""
    if avatar.startswith("/woman_"):
        first_name = fake.unique.first_name_female()
    else:
        first_name = fake.unique.first_name_male()
    return {
        "name": f"{first_name} {fake.unique.last_name()} {fake.unique.last_name()}",
        "phone": fake.unique.phone_number(),
        "avatar": avatar,
        "address": fake.address(),
    }


def generate_users(count: int = 5) -> list[dict[str, str]]:
    """Generate users without repeating avatars until all twelve have been used."""
    if count < 0:
        raise ValueError("El número de usuarios no puede ser negativo.")

    users = []
    avatars = []
    for _ in range(count):
        if not avatars:
            avatars = available_avatars()
        users.append(make_user(avatars.pop()))
    return users


data = generate_users()


