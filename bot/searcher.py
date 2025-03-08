import aiohttp
from random import choice
from enum import Enum
from duckduckgo_search import DDGS
from bot.config import GOOGLE_API_KEY, GOOGLE_CSE_ID
from enums.enums import Searcher

current_searcher = Searcher.GOOGLE


async def search_image_google(query: str, start_index: int = 0) -> str:
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'searchType': 'image',
        'safe': 'active',
        'num': 10
    }
    if start_index > 0:
        params['start'] = start_index
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, params=params) as resp:
            if resp.status == 200:
                result = await resp.json()
                items = result.get('items')
                if items:
                    return choice(items).get('link')


async def search_image_duckduckgo(query: str, start_index: int = 0) -> str:
    ddgs = DDGS()
    results = ddgs.images(query, max_results=max(start_index, 10), safesearch='off')
    if results:
        return choice(results).get('image')


async def search_image(query: str, start_index: int = 0) -> str:
    if current_searcher == Searcher.GOOGLE:
        return await search_image_google(query, start_index)
    elif current_searcher == Searcher.DUCKDUCKGO:
        return await search_image_duckduckgo(query, start_index)
