"""Compatibility Streamlit entrypoint using unified requirements.txt."""

import importlib


def _check_runtime_dependencies() -> None:
    """Fail fast with a clear install message when dependencies are missing."""
    required = ["streamlit", "plotly", "pandas", "requests"]
    for module_name in required:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise SystemExit(
                f"Missing dependency '{module_name}'. Install with: pip install -r requirements.txt"
            )


_check_runtime_dependencies()

# Re-export app code so either file works:
#   streamlit run streamlit.py
#   streamlit run streamlit_app.py
from streamlit_app import *  # noqa: F401,F403