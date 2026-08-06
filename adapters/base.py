from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Abstract base adapter for provider implementations."""

    @abstractmethod
    def is_healthy(self) -> bool:
        """Check provider operational status."""
        pass
