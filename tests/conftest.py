import pytest

from flask_app.app import GetApp


@pytest.fixture
def app(request):
    """
    Get app object and set it up for testing
    """
    app = GetApp.get_app()
    app.debug = True
    app.config['SECRET_KEY'] = "super secret key"
    app.config['TESTING'] = True
    app.config["WTF_CSRF_ENABLED"] = False

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture
def client(app):
    """
    Creates a test client
    """
    return app.test_client()
