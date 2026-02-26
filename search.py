import redis
import json
import connect
from models import Author, Quote

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def search_by_name(name):
    cache_key = f"name:{name}"

    if r.exists(cache_key):
        return json.loads(r.get(cache_key))

    authors = Author.objects(fullname__iregex=f"^{name}")
    quotes = Quote.objects(author__in=authors)

    result = [q.quote for q in quotes]
    r.set(cache_key, json.dumps(result))
    return result


def search_by_tag(tag):
    cache_key = f"tag:{tag}"

    if r.exists(cache_key):
        return json.loads(r.get(cache_key))

    quotes = Quote.objects(tags__iregex=f"^{tag}")
    result = [q.quote for q in quotes]
    r.set(cache_key, json.dumps(result))
    return result


def search_by_tags(tags):
    tag_list = tags.split(",")
    quotes = Quote.objects(tags__in=tag_list)
    return [q.quote for q in quotes]


while True:
    command = input(">>> ")

    if command == "exit":
        break

    try:
        cmd, value = command.split(":", 1)
    except ValueError:
        print("Invalid format")
        continue

    if cmd == "name":
        results = search_by_name(value)
    elif cmd == "tag":
        results = search_by_tag(value)
    elif cmd == "tags":
        results = search_by_tags(value)
    else:
        print("Unknown command")
        continue

    for item in results:
        print(item)