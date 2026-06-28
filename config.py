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

# Usage
configuration = configure_app()
if configuration is not None:
    print("Configuration:")
    for key, value in configuration.items():
        print(f"{key}: {value}")