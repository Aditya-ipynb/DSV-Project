import asyncio
from aiohttp import ClientSession
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.table import Table

from utils import URLGenerator, parse_response


async def main():
    """Main function to generate URLs, fetch Pokémon data, and save it to a JSON file."""
    urls = URLGenerator("poke_list.csv").generate()

    # Initialize TinyDB with UTF-8 and formatting configurations
    db = TinyDB(
        "pokemonDB.json",
        storage=JSONStorage,
        indent=4,
        sort_keys=True,
        ensure_ascii=False,
        encoding="utf-8",
    )
    pokemon_table = db.table("Pokemon")

    # --- RESUME LOGIC ---
    # Fetch all records currently stored in the table
    existing_records = pokemon_table.all()

    # Create a set of URLs that have already been processed.
    # (Assuming your URL format matches what parse_response saves or extracts)
    # If parse_response stores a 'url' key, we match against that.
    # Otherwise, we can extract the pokemon name/slug from the URL to check.
    scraped_urls = set()
    for record in existing_records:
        if "url" in record:
            scraped_urls.add(record["url"])
        elif "name" in record:
            # Alternative: If your URL ends with the pokemon name slug (e.g., /pokedex/bulbasaur)
            # we check if any URL contains the lowercase name
            pass

    # Filter out the URLs we have already scraped
    # Note: If 'url' isn't explicitly stored in your DB by parse_response,
    # you can match by extracting the slug: [u for u in urls if u.split('/')[-1] not in scraped_names]
    pending_urls = [u for u in urls if u not in scraped_urls]

    print(
        f"Found {len(existing_records)} existing entries. Resuming with {len(pending_urls)} remaining URLs..."
    )
    # ---------------------

    async with ClientSession() as session:
        for url in pending_urls:
            print(f"Fetching: {url}")
            await fetch(session, url, pokemon_table)
            await asyncio.sleep(4)


async def fetch(session: ClientSession, url: str, table: Table) -> None:
    """Fetches data from a URL and parses the response to update the results list."""
    async with session.get(url) as response:
        parse_response(await response.text(), table)


if __name__ == "__main__":
    asyncio.run(main())