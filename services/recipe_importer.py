import requests
from recipe_scrapers import scrape_html
from models.recipe import Recipe
from models.ingredient import Ingredient

# Many recipe sites reject requests that don't look like a real browser.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def import_recipe_from_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Couldn't fetch the page ({type(e).__name__}: {e})")

    try:
        # supported_only=False lets it work on any site with schema.org recipe
        # markup, not just the sites the library has explicit scrapers for.
        scraper = scrape_html(html=response.text, org_url=url, supported_only=False)
    except Exception as e:
        raise ValueError(f"Couldn't read a recipe from that page ({type(e).__name__}: {e})")

    try:
        title = scraper.title()
        ingredient_lines = scraper.ingredients()
        instructions = scraper.instructions()
    except Exception as e:
        raise ValueError(f"Page loaded, but no recipe data found ({type(e).__name__}: {e})")

    if not title and not ingredient_lines:
        raise ValueError("Page loaded, but it has no recipe markup.")

    # recipe-scrapers gives back full text lines like "2 cups flour, sifted" —
    # not split into separate name/amount/unit fields. Rather than trying to
    # parse that ourselves (a genuinely hard problem on its own), each line
    # goes straight into the ingredient's name; amount/unit/calories are left
    # blank and can be filled in later via the Edit Recipe popup if wanted.
    ingredients = [Ingredient(name=line, amount="") for line in ingredient_lines]

    try:
        total_time = scraper.total_time()
    except Exception:
        total_time = None
    time = f"{total_time} minutes" if total_time else ""

    return Recipe(
        name=title,
        ingredients=ingredients,
        time=time,
        instructions=instructions
    )
