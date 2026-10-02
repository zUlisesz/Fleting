from faker import Faker
import random
fake = Faker('es')


def get_random_avatar(gender: str):                                              
    idx = random.randint(1, 6)                                                            
    return f"/{gender}_{idx}.png"

def makeUser():

    female = fake.boolean(50)
    if female:
        return {
            'name': f'{fake.unique.first_name_female()} {fake.unique.last_name()} {fake.unique.last_name()}',
            'phone': f'{fake.unique.phone_number()}',
            'avatar': get_random_avatar('woman'),
            'address': f'{fake.address()}'
        }

    return {
        'name': f'{fake.unique.first_name_male()} {fake.unique.last_name()} {fake.unique.last_name()}',
        'phone': f'{fake.unique.phone_number()}',
        'avatar': get_random_avatar('man'),
        'address': f'{fake.address()}'
    }


data = [ makeUser() for _ in range(5)]


