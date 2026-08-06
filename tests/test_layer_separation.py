import ast
from pathlib import Path

FORBIDDEN_SERVICE_IMPORTS = {
    "fastapi",
    "starlette",
    "Request",
    "Response",
    "UploadFile",
    "HTTPException",
    "APIRouter",
}


def test_services_layer_has_no_fastapi_types():
    """Mechanically enforce that services/ package never imports FastAPI types or modules."""
    services_dir = Path(__file__).parent.parent / "services"
    for py_file in services_dir.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in FORBIDDEN_SERVICE_IMPORTS, (
                        f"Forbidden import '{alias.name}' found in {py_file}"
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert not any(pkg in module for pkg in ["fastapi", "starlette"]), (
                    f"Forbidden import from '{module}' found in {py_file}"
                )
                for alias in node.names:
                    assert alias.name not in FORBIDDEN_SERVICE_IMPORTS, (
                        f"Forbidden symbol '{alias.name}' imported from '{module}' in {py_file}"
                    )
