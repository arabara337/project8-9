import json
from models import Author, Quote
import connect

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

for item in quotes:
    author = Author.objects(fullname=item["author"]).first()
    if author:
        Quote(
            tags=item["tags"],
            author=author,
            quote=item["quote"]
        ).save()

print("Quotes loaded successfully!")