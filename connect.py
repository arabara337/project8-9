from mongoengine import connect

connect(
    db="quotes_db",
    host="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/quotes_db?retryWrites=true&w=majority"
)