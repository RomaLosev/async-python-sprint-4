from models.models import URL
from schemas.urls import URLCreate

from .base import RepositoryDB


class RepositoryURL(RepositoryDB[URL, URLCreate]):
    pass


urls_crud = RepositoryURL(URL)
