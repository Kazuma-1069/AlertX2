# Alias module so screens can import from app.utils.local_store
from app.utils.storage import local_store, LocalStore

__all__ = ["local_store", "LocalStore"]
