import json
from models import Author
import connect

with open("authors.json", "r", encoding="utf-8") as f:
    authors = json.load(f)

for item in authors:
    Author(
        fullname=item["fullname"],
        born_date=item.get("born_date"),
        born_location=item.get("born_location"),
        description=item.get("description")
    ).save()

print("Authors loaded successfully!")