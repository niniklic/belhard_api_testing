import json

import pytest
import requests

from src.Pet import Pet
from src.endpoint import BASE_URL, POST_GET_URI, FIND_BY_STATUS

categories = {
    "1": "Dog",
    "2": "Cat",
    "3": "Elk",
    "4": "Fish",
    "5": "Rat",
    "6": "Parrot"
}
pets_list = []


def prepare_pets_to_post():
    pets_data = [["Dolly", 4], ["Che", 2], ["Pinki", 2], ["Elky", 3], ["Norma", 1],
                 ["Jutah", 1], ["Jessie", 1], ["Kesha", 6], ["Monty", 5]]
    for new_pet in pets_data:
        pets_list.append(Pet(new_pet[0], categories[str(new_pet[1])], new_pet[1]))


class TestGetAndPostPets:
    prepare_pets_to_post()

    def test_is_request_ok(self):
        response = requests.get(BASE_URL)
        assert response.status_code == 200

    def test_response_not_empty(self):
        response = requests.get(BASE_URL)
        assert response.text

    def test_post_success(self):
        for pet_to_post in pets_list:
            request_post = requests.post(BASE_URL + POST_GET_URI, json=pet_to_post.get_post_body())
            assert request_post.status_code == 200

    def test_find_pet_by_id(self):
        response = requests.get(BASE_URL + POST_GET_URI + f"/{pets_list[0].id}")
        assert response.status_code == 200

    def test_is_elky_present(self):
        response = requests.get(BASE_URL + POST_GET_URI + FIND_BY_STATUS +
                                f"?status={pets_list[3].status}")
        response_to_list = list(response.json())
        dolly = False
        for pet_item in response_to_list:
            if pet_item["name"] == "Elky":
                elky = True
        assert elky

    @pytest.mark.xfail
    def test_is_nemo_present(self):
        response = requests.get(BASE_URL + POST_GET_URI)
        assert "Nemo" in response.text

    @pytest.mark.skipif('Bear' not in categories, reason="I'm not gonna have a bear")
    def test_is_bear_present(self):
        response = requests.get(BASE_URL + POST_GET_URI)
        assert "Bear" in response.text

    def test_delete_pet_by_id(self):
        response_delete = requests.delete(BASE_URL + POST_GET_URI + f"/{pets_list[1].id}")
        assert response_delete.status_code == 200
        response_get = requests.get(BASE_URL + POST_GET_URI + f"/{pets_list[1].id}")
        assert response_get.status_code == 404



