import pytest

from types import SimpleNamespace
from flask_app.forms import SearchForCourseSectionsForm, AddRemoveForm, ClearAllCoursesForm


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_clear_all_courses(client):
    clear_classes = SimpleNamespace(clear_all="Clear Schedule")
    form = ClearAllCoursesForm(formdata=None, obj=clear_classes)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Schedule is already empty" in response.data


def test_all_courses_returns_200(client):
    resp = client.get("/all_courses/1")
    assert resp.status_code == 200

#
# @pytest.mark.parametrize(
#     ("course_query", "section_query", "message"),
#     [
#         ("CMSC131", "0101", b"CMSC131-0101 added."),
#     ]
# )
# def test_add_course(client, course_query, section_query, message):
#     # response = client.get("/")
#     # # print(response.data.decode())
#     add_class = SimpleNamespace(course_query=course_query, section_query=section_query, add="Add")
#     form = AddRemoveForm(formdata=None, obj=add_class)
#
#     # Form is not validating for some reason

#     response = client.post("/", data=form.data, follow_redirects=True)
#     assert response.status_code == 200
#     print(response.data.decode())
#     assert message in response.data
#
#
# @pytest.mark.parametrize(
#     ("course_query", "section_query", "message"),
#     [
#         ("CMSC131", "0101", b"CMSC131-0101 removed."),
#     ]
# )
# def test_remove_course(client, course_query, section_query, message):
#     remove_class = SimpleNamespace(course_query=course_query, section_query=section_query, remove="Remove")
#     form = AddRemoveForm(formdata=None, obj=remove_class)
#     response = client.post("/", data=form.data, follow_redirects=True)
#     assert response.status_code == 200
#     assert message in response.data
#
#
# @pytest.mark.parametrize(
#     ("query", "message"),
#     [
#         ("CMSC131", b"CMSC131-0101"),
#         ("BSCI207", b"BSCI207-0201"),
#     ]
# )
# def test_search_for_sections(client, query, message):
#     search = SimpleNamespace(search_query=query, search_for_course="Search")
#     form = SearchForCourseSectionsForm(formdata=None, obj=search)
#
#     assert form.validate() == True
#
#     response = client.post("/", data=form.data, follow_redirects=True)
#
#     assert response.status_code == 200
#     assert message in response.data
