from faker import Faker
fake = Faker('es')

fake.boolean(50)

data = [
    {
        'name': f'{fake.unique.first_name()} {fake.unique.last_name()} {fake.unique.last_name()}',
        'phone': f'{fake.unique.phone_number()}',
        'address': f'{fake.address()}'
    } for _ in range(4)
]

