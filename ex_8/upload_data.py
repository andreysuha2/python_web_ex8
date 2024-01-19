from pathlib import Path
from datetime import datetime
from ex_8.definitions import ROOT_DIR
from ex_8.connect import connect
from ex_8.models import Author, Quote
import aiofiles
import asyncio
import json

PATH_TO_AUTHORS = Path(f'{ROOT_DIR}/authors.json')
PATH_TO_QUOTES = Path(f'{ROOT_DIR}/quotes.json')

async def load_file(path) -> dict:
    async with aiofiles.open(path, mode='r') as file:
        return json.loads(await file.read())
    
def create_author(author: dict) -> Author:
    author["born_date"] = datetime.strptime(author['born_date'], '%B %d, %Y').date()
    author = Author(**author)
    author.save()
    return author

def create_quote(quote: dict, authors: list[Author]) -> Quote:
    author = next(item for item in authors if item.fullname == quote["author"])
    quote["author"] = author
    quote = Quote(**quote)
    quote.save()
    author.quotes.append(quote)
    author.save()
    
async def main() -> None:
    authors_data, quotes_data = await asyncio.gather(load_file(PATH_TO_AUTHORS), load_file(PATH_TO_QUOTES))
    authors = [ create_author(data) for data in authors_data ]
    [ create_quote(data, authors) for data in quotes_data ]
    
if __name__ == '__main__':
    asyncio.run(main())