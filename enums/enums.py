from enum import Enum


class Searcher(Enum):
    GOOGLE = 'google'
    DUCKDUCKGO = 'duckduckgo'


class Language(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en'
