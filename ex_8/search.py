from ex_8.connect import connect
from ex_8.models import Quote, Author


def search_by_name(name: str) -> list[Quote]:
    authors = Author.objects(fullname__istartswith=name).all()
    return Quote.objects(author__in=authors).all()

def search_by_tag(tag: str) -> list[Quote]:
    return Quote.objects(tags__icontains=tag, tags__istartswith=tag).all()

def search_by_tags(tags_str: str) -> list[Quote]:
    tags = [ tag.strip() for tag in tags_str.split(',') ]
    return Quote.objects(tags__in=tags).all()

queries = {
    "name": search_by_name,
    "tag": search_by_tag,
    "tags": search_by_tags
}

def pars_search_str(string: str) -> tuple[str, str]:
    key, value = string.split(":")
    return key.strip(), value.strip()

def pars_quote(quote: Quote) -> str:
    return f"{quote.quote}; autor: {quote.author.fullname}; tags: {', '.join(quote.tags)}"

def main() -> None:
    try:
        while True:
            search = input(">>> ")
            if search.strip() == "exit":
                raise KeyboardInterrupt
            key, value = pars_search_str(search)
            query = queries.get(key, None)
            if not query:
                print(f"You cant find somesing by key: {key}. Please use name, tag or tags as kay")
            else:
                quotes = query(value)
                if len(quotes):
                    for quote in quotes:
                        print(pars_quote(quote))
                        print("")
                else:
                    print(f"For params '{search}' not found results!")
    except KeyboardInterrupt:
        print("Thank you, bay)")

if __name__ == "__main__":
    main()