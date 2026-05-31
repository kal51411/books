from backend.app.main import create_app


def test_app_metadata():
    app = create_app()

    assert app.title == "NyayaGPT API"
