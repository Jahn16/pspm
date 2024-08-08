"""Module with errors related to dependency management."""


class InstallError(Exception):
    """Can't install package."""

    def __init__(self, package: str) -> None:
        """Initialize InstallError.

        Args:
            package: Package that failed to be installed
        """
        self.package = package
        self.message = f"Error installing package {package}"
        super().__init__(self.message)
