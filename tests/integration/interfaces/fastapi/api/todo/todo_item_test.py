import pytest

from tests.factories.model_factories import insert_todo_item


@pytest.mark.integration
class TestHandleCreateOne:
    def test_success(self, test_client, create_todo_item_dto):
        with test_client as client:
            response = client.post("/todo/item", json=create_todo_item_dto.dict())
            data, status_code = response.json(), response.status_code
            assert status_code == 201
            assert data == {
                "id": 1,
                "msg": create_todo_item_dto.msg,
                "is_done": create_todo_item_dto.is_done,
            }

    def test_validation_error(self, test_client):
        with test_client as client:
            response = client.post("/todo/item", json={})
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
    def test_success(self, test_client, create_todo_item_dto):
        with test_client:
            id_ = 1
            insert_todo_item({**create_todo_item_dto.dict(), "id": id_})
            response = test_client.delete(f"/todo/item/{id_}")
            assert response.status_code == 204

    def test_item_not_found(self, test_client):
        with test_client:
            id_ = 1
            response = test_client.delete(f"/todo/item/{id_}")
            assert response.status_code == 404

    def test_validation_error(self, test_client):
        with test_client:
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
    def test_success(self, test_client, create_todo_item_dtos):
        with test_client:
            values = [
                {**value.dict(), "id": idx}
                for idx, value in enumerate(create_todo_item_dtos(5))
            ]
            insert_todo_item(values)

            response = test_client.get("/todo/item")
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert len(data) == 5
            assert data == values


@pytest.mark.integration
class TestHandleGetOne:
    def test_success(self, test_client, create_todo_item_dto):
        with test_client:
            id_ = 1
            value = {**create_todo_item_dto.dict(), "id": id_}
            insert_todo_item(value)

            response = test_client.get(f"/todo/item/{id_}")
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert data == value

    def test_item_not_found(self, test_client):
        with test_client:
            id_ = 1
            response = test_client.get(f"/todo/item/{id_}")
            assert response.status_code == 404


@pytest.mark.integration
class TestHandleReplaceOne:
    def test_success(self, test_client, create_todo_item_dto):
        with test_client:
            id_ = 1
            insert_todo_item(
                {
                    **create_todo_item_dto.dict(),
                    "msg": create_todo_item_dto.msg[::-1],
                    "id": id_,
                }
            )

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
        with test_client:
            id_ = 1
            response = test_client.put(
                f"/todo/item/{id_}", json=create_todo_item_dto.dict()
            )
            assert response.status_code == 404

    def test_validation_error(self, test_client):
        with test_client:
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
    def test_success(self, test_client, create_todo_item_dto, update_todo_item_dto):
        with test_client:
            id_ = 1
            insert_todo_item(
                {
                    **create_todo_item_dto.dict(),
                    "msg": create_todo_item_dto.msg,
                    "id": id_,
                }
            )

            response = test_client.patch(
                f"/todo/item/{id_}", json=update_todo_item_dto.dict(exclude={"msg"})
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert data == {
                "id": id_,
                "msg": create_todo_item_dto.msg,
                "is_done": update_todo_item_dto.is_done,
            }

    def test_item_not_found(self, test_client, update_todo_item_dto):
        with test_client:
            id_ = 6
            response = test_client.patch(
                f"/todo/item/{id_}", json=update_todo_item_dto.dict()
            )
            assert response.status_code == 404
