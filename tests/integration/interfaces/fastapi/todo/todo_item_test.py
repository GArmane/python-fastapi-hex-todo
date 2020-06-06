import pytest

from tests.factories.model_factories import insert_todo_item
from tests.utils.auth import auth_headers


@pytest.mark.integration
class TestHandleCreateOne:
    def test_success(self, test_client, logged_user, create_todo_item_dto):
        with test_client:
            response = test_client.post(
                "/todo/item",
                json=create_todo_item_dto.dict(),
                headers=auth_headers(logged_user.access_token),
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 201
            assert data == {
                "id": 1,
                "msg": create_todo_item_dto.msg,
                "is_done": create_todo_item_dto.is_done,
                "user_id": logged_user.user.id,
            }

    def test_validation_error(self, test_client, logged_user):
        with test_client:
            response = test_client.post(
                "/todo/item", json={}, headers=auth_headers(logged_user.access_token)
            )
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

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.post("/todo/item")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401


@pytest.mark.integration
class TestHandleDeleteOne:
    def test_success(self, test_client, logged_user, create_todo_item_dto):
        with test_client:
            id_ = 1
            insert_todo_item(
                {
                    **create_todo_item_dto.dict(),
                    "id": id_,
                    "user_id": logged_user.user.id,
                }
            )
            response = test_client.delete(
                f"/todo/item/{id_}", headers=auth_headers(logged_user.access_token)
            )
            assert response.status_code == 204

    def test_item_not_found(self, test_client, logged_user):
        with test_client:
            id_ = 1
            response = test_client.delete(
                f"/todo/item/{id_}", headers=auth_headers(logged_user.access_token)
            )
            assert response.status_code == 404

    def test_validation_error(self, test_client, logged_user):
        with test_client:
            id_ = 1.0
            response = test_client.delete(
                f"/todo/item/{id_}", headers=auth_headers(logged_user.access_token)
            )
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

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.delete("/todo/item/1")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401


@pytest.mark.integration
class TestHandleGetAll:
    def test_success(self, test_client, logged_user, create_todo_item_dtos):
        with test_client:
            values = [
                {**value.dict(), "id": idx, "user_id": logged_user.user.id}
                for idx, value in enumerate(create_todo_item_dtos(5))
            ]
            insert_todo_item(values)

            response = test_client.get(
                "/todo/item", headers=auth_headers(logged_user.access_token)
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert len(data) == 5
            assert data == values

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.get("/todo/item")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401


@pytest.mark.integration
class TestHandleGetOne:
    def test_success(self, test_client, logged_user, create_todo_item_dto):
        with test_client:
            id_ = 1
            value = {
                **create_todo_item_dto.dict(),
                "id": id_,
                "user_id": logged_user.user.id,
            }
            insert_todo_item(value)

            response = test_client.get(
                f"/todo/item/{id_}", headers=auth_headers(logged_user.access_token)
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert data == value

    def test_item_not_found(self, test_client, logged_user):
        with test_client:
            id_ = 1
            response = test_client.get(
                f"/todo/item/{id_}", headers=auth_headers(logged_user.access_token)
            )
            assert response.status_code == 404

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.get(f"/todo/item/1")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401


@pytest.mark.integration
class TestHandleReplaceOne:
    def test_success(self, test_client, logged_user, create_todo_item_dto):
        with test_client:
            id_ = 1
            user_id = logged_user.user.id

            insert_todo_item(
                {
                    **create_todo_item_dto.dict(),
                    "msg": create_todo_item_dto.msg[::-1],
                    "id": id_,
                    "user_id": user_id,
                }
            )

            response = test_client.put(
                f"/todo/item/{id_}",
                json=create_todo_item_dto.dict(),
                headers=auth_headers(logged_user.access_token),
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert data == {
                "id": id_,
                "msg": create_todo_item_dto.msg,
                "is_done": create_todo_item_dto.is_done,
                "user_id": user_id,
            }

    def test_item_not_found(self, test_client, logged_user, create_todo_item_dto):
        with test_client:
            id_ = 1
            response = test_client.put(
                f"/todo/item/{id_}",
                json=create_todo_item_dto.dict(),
                headers=auth_headers(logged_user.access_token),
            )
            assert response.status_code == 404

    def test_validation_error(self, test_client, logged_user):
        with test_client:
            id_ = 1
            response = test_client.put(
                f"/todo/item/{id_}",
                json={},
                headers=auth_headers(logged_user.access_token),
            )
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

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.put(f"/todo/item/1")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401


@pytest.mark.integration
class TestHandleUpdateOne:
    def test_success(
        self, test_client, logged_user, create_todo_item_dto, update_todo_item_dto
    ):
        with test_client:
            id_ = 1
            user_id = logged_user.user.id
            insert_todo_item(
                {
                    **create_todo_item_dto.dict(),
                    "msg": create_todo_item_dto.msg,
                    "id": id_,
                    "user_id": user_id,
                }
            )

            response = test_client.patch(
                f"/todo/item/{id_}",
                json=update_todo_item_dto.dict(exclude={"msg"}),
                headers=auth_headers(logged_user.access_token),
            )
            data, status_code = response.json(), response.status_code
            assert status_code == 200
            assert data == {
                "id": id_,
                "msg": create_todo_item_dto.msg,
                "is_done": update_todo_item_dto.is_done,
                "user_id": user_id,
            }

    def test_item_not_found(self, test_client, logged_user, update_todo_item_dto):
        with test_client:
            id_ = 6
            response = test_client.patch(
                f"/todo/item/{id_}",
                json=update_todo_item_dto.dict(),
                headers=auth_headers(logged_user.access_token),
            )
            assert response.status_code == 404

    def test_authorization(self, test_client):
        with test_client:
            response = test_client.patch(f"/todo/item/1")
            data, status_code = response.json(), response.status_code
            assert data == {"detail": "Not authenticated"}
            assert status_code == 401
