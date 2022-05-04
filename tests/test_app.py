import pytest


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_all_courses_returns_200(client):
    resp = client.get("/all_courses/1")
    assert resp.status_code == 200


def test_all_professors_returns_200(client):
    resp = client.get("/all_professors/1")
    assert resp.status_code == 200

def test_professor_detail_returns_200(client):
    resp = client.get("/professor/%20Auguste%20Gezalyan/gezalyan")
    assert resp.status_code == 200

    resp = client.get("/professor/Aaron%20Swanlek/swanlek")
    assert resp.status_code == 200

def test_professor_detail_returns_404_if_no_professor(client):
    resp = client.get("/professor/non_existant")
    assert resp.status_code == 404

    resp = client.get("/professor/")
    assert resp.status_code == 404
