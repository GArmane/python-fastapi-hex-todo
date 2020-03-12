import pytest


@pytest.mark.integration
class TestHandleCreateOne:
    def test_success(self, test_client, create_todo_item_dto):
        response = test_client.post("/todo/item", json=create_todo_item_dto.dict())
        data, status_code = response.json(), response.status_code
        assert status_code == 201
        assert data == {
            "id": 6,
            "msg": create_todo_item_dto.msg,
            "is_done": create_todo_item_dto.is_done,
        }

    def test_validation_error(self, test_client):
        response = test_client.post("/todo/item", json={})
        data, status_code = response.json(), response.status_code
        assert status_code == 422
        assert data == {
            "detail": [
                {
                    "loc": ["body", "dto", "msg"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


@pytest.mark.integration
class TestHandleDeleteOne:
    def test_success(self, test_client):
        id_ = 1
        response = test_client.delete(f"/todo/item/{id_}")
        assert response.status_code == 204

    def test_item_not_found(self, test_client):
        id_ = 6
        response = test_client.delete(f"/todo/item/{id_}")
        assert response.status_code == 404

    def test_validation_error(self, test_client):
        id_ = 1.0
        response = test_client.delete(f"/todo/item/{id_}")
        data, status_code = response.json(), response.status_code
        assert status_code == 422
        assert data == {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }


@pytest.mark.integration
class TestHandleGetAll:
    def test_success(self, test_client):
        response = test_client.get("/todo/item")
        data, status_code = response.json(), response.status_code
        assert status_code == 200
        assert len(data) == 5
        assert data == [
            {"id": 1, "is_done": False, "msg": "Item 1"},
            {"id": 2, "is_done": False, "msg": "Item 2"},
            {"id": 3, "is_done": False, "msg": "Item 3"},
            {"id": 4, "is_done": True, "msg": "Item 4"},
            {"id": 5, "is_done": True, "msg": "Item 5"},
        ]


@pytest.mark.integration
class TestHandleGetOne:
    def test_success(self, test_client):
        id_ = 1
        response = test_client.get(f"/todo/item/{id_}")
        data, status_code = response.json(), response.status_code
        assert status_code == 200
        assert data == {"id": 1, "is_done": False, "msg": "Item 1"}

    def test_item_not_found(self, test_client):
        id_ = 6
        response = test_client.get(f"/todo/item/{id_}")
        assert response.status_code == 404


@pytest.mark.integration
class TestHandleReplaceOne:
    def test_success(self, test_client, create_todo_item_dto):
        id_ = 1
        response = test_client.put(
            f"/todo/item/{id_}", json=create_todo_item_dto.dict()
        )
        data, status_code = response.json(), response.status_code
        assert status_code == 200
        assert data == {
            "id": id_,
            "msg": create_todo_item_dto.msg,
            "is_done": create_todo_item_dto.is_done,
        }

    def test_item_not_found(self, test_client, create_todo_item_dto):
        id_ = 6
        response = test_client.put(
            f"/todo/item/{id_}", json=create_todo_item_dto.dict()
        )
        assert response.status_code == 404

    def test_validation_error(self, test_client):
        id_ = 1
        response = test_client.put(f"/todo/item/{id_}", json={})
        data, status_code = response.json(), response.status_code
        assert status_code == 422
        assert data == {
            "detail": [
                {
                    "loc": ["body", "dto", "msg"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }


@pytest.mark.integration
class TestHandleUpdateOne:
    def test_success(self, test_client, update_todo_item_dto):
        id_ = 1
        response = test_client.patch(
            f"/todo/item/{id_}", json=update_todo_item_dto.dict(exclude={"msg"})
        )
        data, status_code = response.json(), response.status_code
        assert status_code == 200
        assert data == {
            "id": id_,
            "msg": f"Item {id_}",
            "is_done": update_todo_item_dto.is_done,
        }

    def test_item_not_found(self, test_client, update_todo_item_dto):
        id_ = 6
        response = test_client.patch(
            f"/todo/item/{id_}", json=update_todo_item_dto.dict()
        )
        assert response.status_code == 404
