import pytest

def configure_app():
    """
    Configure the application with the given settings.

    Returns:
        dict: A dictionary containing the configuration settings.
    """

    # Configuration
    app_name = "Dev Agent"
    version = "1.0.0"
    debug_mode = False

    try:
        # Validate input types
        if not isinstance(app_name, str):
            raise TypeError("APP_NAME must be a string")
        if not isinstance(version, str):
            raise TypeError("VERSION must be a string")
        if app_name.lower() != "dev agent" and version.lower() != "1.0.0":
            raise ValueError("Invalid configuration settings")

        # Set the configuration
        CONFIGURATION = {
            "APP_NAME": app_name,
            "VERSION": version,
            "DEBUG_MODE": debug_mode
        }

    except TypeError as e:
        print(f"Error: {e}")
        return None

    except ValueError as e:
        print(f"Error: {e}")
        return None

    return CONFIGURATION

def test_configure_app_normal_cases():
    # Test when configuration is valid
    config = configure_app()
    assert config is not None
    expected_config = {
        "APP_NAME": "Dev Agent",
        "VERSION": "1.0.0",
        "DEBUG_MODE": False
    }
    assert config == expected_config

def test_configure_app_invalid_app_name():
    # Test when app name is invalid
    config = configure_app(app_name="Invalid App")
    assert config is None

def test_configure_app_invalid_version():
    # Test when version is invalid
    config = configure_app(version="1.0-1")
    assert config is None

def test_configure_app_type_error():
    # Test when app name or version type is incorrect
    with pytest.raises(TypeError):
        configure_app(app_name=123)

def test_configure_app_value_error():
    # Test when app name or version value is incorrect
    with pytest.raises(ValueError):
        configure_app(app_name="Invalid App", version="1.0-1")