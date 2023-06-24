import aiohttp
from .settings import url_start


async def get_simple_data(url_data, value=None, value2=None, value3=None):
    async with aiohttp.ClientSession() as session:
        if value is None and value2 is None and value3 is None:
            async with session.get(f'{url_start}{url_data}') as response:
                result = await response.json()
        elif value and value2 and value3 is None:
            async with session.get(f'{url_start}{url_data}{value}/{value2}/') as response:
                result = await response.json()
        elif value and value2 and value3:
            async with session.get(f'{url_start}{url_data}{value}/{value2}/{value3}/') as response:
                result = await response.json()
        elif value and value2 is None and value3 is None:
            async with session.get(f'{url_start}{url_data}{value}/') as response:
                result = await response.json()
        return result