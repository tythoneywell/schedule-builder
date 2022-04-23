import pytest


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_all_courses_returns_200(client):
    resp = client.get("/all_courses/1")
    assert resp.status_code == 200
