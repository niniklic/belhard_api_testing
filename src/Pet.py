from random import randrange

STATUS_LIST = ["available", "pending", "sold"]


class Pet:
    id = 100000

    def __init__(self, pet_name: str, category_name: str, category_id: int):
        self.id = Pet.id
        Pet.id += 1
        self.name = pet_name
        self.category = [category_id, category_name]
        self.status = STATUS_LIST[randrange(len(STATUS_LIST) - 1)]

    def get_post_body(self):
        return {
            "id": self.id,
            "category": {"id": self.category[0], "name": self.category[1]},
            "name": self.name,
            "status": self.status
        }
