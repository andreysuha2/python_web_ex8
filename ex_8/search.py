from ex_8.connect import connect
from ex_8.models import Quote, Author
import json
import os
import redis

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"))

def search_by_name(name: str) -> list[Quote]:
    authors = Author.objects(fullname__istartswith=name).all()
    return Quote.objects(author__in=authors).all()

def search_by_tag(tag: str) -> list[Quote]:
    return Quote.objects(tags__icontains=tag, tags__istartswith=tag).all()

def search_by_tags(tags_str: str) -> list[Quote]:
    tags = tags_str.split(",")
    return Quote.objects(tags__in=tags).all()

queries = {
    "name": search_by_name,
    "tag": search_by_tag,
    "tags": search_by_tags
}

def pars_search_str(string: str) -> tuple[str, str]:
    key, value = string.split(":")
    return key.strip(), ",".join([ item.strip() for item in value.split(",") ])

def pars_quote(quote: Quote) -> str:
    return f"{quote.quote}; autor: {quote.author.fullname}; tags: {', '.join(quote.tags)}"

def load_quotes(query, key, value):
    redis_key = f"{key}:{value}"
    if not r.exists(redis_key):
        quotes = query(value)
        r.set(redis_key, json.dumps([ pars_quote(quote) for quote in quotes ]), ex=86400)
    return json.loads(r.get(redis_key))
    

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
                quotes = load_quotes(query, key, value)
                if len(quotes):
                    for quote in quotes:
                        print(quote)
                        print("")
                else:
                    print(f"For params '{search}' not found results!")
    except KeyboardInterrupt:
        print("Thank you, bay)")

if __name__ == "__main__":
    main()