"""Module with errors related to dependency management."""


class DependencyError(Exception):
    """Base error for dependencies."""


class InstallError(DependencyError):
    """Can't install package."""

    def __init__(self, package: str) -> None:
        """Initialize InstallError.

        Args:
            package: Package that failed to be installed
        """
        self.package = package
        self.message = f"Error installing package {package}"
        super().__init__(self.message)


class AddError(InstallError):
    """Can't add package to project."""


class SyncError(DependencyError):
    """Can't sync dependencies."""

    def __init__(self) -> None:
        """Initialize SyncError."""
        super().__init__("Could not sync dependencies")


class ResolveError(DependencyError):
    """Can't resolve dependencies."""

    def __init__(self) -> None:
        """Initialize SyncError."""
        super().__init__("Error resolving dependencies")
