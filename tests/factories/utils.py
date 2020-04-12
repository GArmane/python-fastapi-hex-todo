def make_many(factory, amount=3):
    return [factory() for _ in range(amount)]
