from typing import Optional
from .models import CoordinatorSession
from .exceptions import SessionError

class CoordinatorManager:
    def __init__(self):
        self._session = CoordinatorSession()

    def get_session(self) -> CoordinatorSession:
        return self._session

    def update_session(self, **kwargs) -> CoordinatorSession:
        self._session = CoordinatorSession(**{**self._session.__dict__, **kwargs})
        return self._session

    def clear_session(self) -> None:
        self._session = CoordinatorSession()
