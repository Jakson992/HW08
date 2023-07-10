import json
from datetime import datetime
from models import Authors, Quotes
from mongoengine import connect



# Підключення до бази даних
connect(db="web12", host="mongodb+srv://JekaWEB12:567234@cluster0.plizfca.mongodb.net/?retryWrites=true&w=majority")


# Завантаження даних з файлів JSON
with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Завантаження авторів
for author_data in authors_data:
    fullname = author_data['fullname']
    born_date_str = author_data['born_date']
    born_date = datetime.strptime(born_date_str, '%B %d, %Y')
    born_location = author_data['born_location']
    description = author_data['description']

    author = Authors(
        fullname=fullname,
        born_date=born_date,
        born_location=born_location,
        description=description
    )
    author.save()

# Завантаження цитат
for quote_data in quotes_data:
    tags = quote_data['tags']
    author_fullname = quote_data['author']
    quote_text = quote_data['quote']

    author = Authors.objects(fullname=author_fullname).first()
    if author:
        quote = Quotes(
            tags=tags,
            author=author,
            quote=quote_text
        )
        quote.save()
