"""Module with errors related to dependency management."""


class InstallError(Exception):
    """Raised when could not install package."""

    def __init__(self, package: str) -> None:
        """Initialize InstallError.

        :param package: Package that failed to be installed
        """
        self.package = package
        self.message = f"Error installing package {package}"
        super().__init__(self.message)
