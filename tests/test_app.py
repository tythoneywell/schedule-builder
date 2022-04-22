import pytest


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_clear_all_courses(client):
    clear_classes = SimpleNamespace(clear_all="Clear Schedule")
    form = ClearAllCoursesForm(formdata=None, obj=clear_classes)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Schedule is already empty" in response.data
