import requests
from recipe_scrapers import scrape_html
from ingredient_parser import parse_ingredient
from models.recipe import Recipe
from models.ingredient import Ingredient

# Many recipe sites reject requests that don't look like a real browser.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def _first_text(field):
    """Pull plain text out of a parser field.

    Depending on the ingredient-parser version, fields like `name` come back
    either as a single object with `.text` or as a list of them (an ingredient
    can have alternatives, e.g. "butter or margarine"). Handle both.
    """
    if not field:
        return None
    if isinstance(field, list):
        field = field[0]
    return getattr(field, "text", None) or str(field)


def _parse_ingredient_line(line):
    """Turn a raw ingredient line like '2 cups flour, sifted' into an Ingredient.

    Falls back to putting the whole line in the name if parsing fails or the
    line isn't really an ingredient (scraped recipes often include section
    headers like 'For the sauce:').
    """
    try:
        parsed = parse_ingredient(line)

        name = _first_text(parsed.name) or line

        # `amount` is a list — a line can carry more than one (ranges, dual units).
        # We only model a single amount/unit, so take the first if there is one.
        amount = ""
        unit = None
        if parsed.amount:
            first = parsed.amount[0]
            amount = str(first.quantity) if first.quantity else ""
            unit = str(first.unit) if first.unit else None

        # Both of these hold the "extra" wording — "sifted", "room temperature",
        # "plus more for dusting" — which is what our description field is for.
        description_parts = []
        for field in (parsed.preparation, parsed.comment):
            text = _first_text(field)
            if text:
                description_parts.append(text)
        description = ", ".join(description_parts) if description_parts else None

        # calories stays None — no parser can infer that from the text alone.
        return Ingredient(name=name, amount=amount, calories=None, unit=unit, description=description)
    except Exception:
        return Ingredient(name=line, amount="")


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

    ingredients = [_parse_ingredient_line(line) for line in ingredient_lines]

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
