from typing import Dict


class HealthService:
    """Service providing health status logic without web framework dependencies."""

    def __init__(self, adapter_mode: str) -> None:
        self.adapter_mode = adapter_mode

    def get_health_status(self) -> Dict[str, str]:
        return {
            "status": "ok",
            "adapter_mode": self.adapter_mode,
        }
