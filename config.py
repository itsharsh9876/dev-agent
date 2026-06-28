# Configuration
"""
Configuration variables for the application.
"""

APP_NAME = "Dev Agent"
"""
Application name.
"""
VERSION = "1.0.0"
"""
Version number of the application.
"""
DEBUG = False
"""
Debug mode flag.
"""

class Config:
    """
    Class containing configuration settings.
    """
    def __init__(self):
        """
        Initializes the configuration class.
        """
        self.APP_NAME = APP_NAME
        self.VERSION = VERSION
        self.DEBUG = DEBUG