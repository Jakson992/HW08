import argparse
import json
from mongoengine import *

connect(db="web12", host="mongodb+srv://JekaWEB12:567234@cluster0.plizfca.mongodb.net/?retryWrites=true&w=majority")



parser = argparse.ArgumentParser(description='Quotes App')
parser.add_argument('--command', help='Command: load_authors, load_quotes, search')
parser.add_argument('--value')
arguments = parser.parse_args()

command = arguments.command
value = arguments.value


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()
    meta = {'collection': 'quotes'}


def load_authors():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        author = Author(
            fullname=author_data['fullname'],
            born_date=author_data['born_date'],
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()


def load_quotes():
    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data['author']).first()
        if author:
            quote = Quote(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()


def search():
    if value.startswith('name:'):
        name = value.split(':')[1]
        author = Author.objects(fullname=name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
    elif value.startswith('tag:'):
        tag = value.split(':')[1]
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(quote.quote)
    elif value.startswith('tags:'):
        tags = value.split(':')[1]
        tags_list = tags.split(',')
        quotes = Quote.objects(tags__in=tags_list)
        for quote in quotes:
            print(quote.quote)
    elif value == 'exit':
        return
    else:
        print("Unknown command")


def main():
    if command == 'load_authors':
        load_authors()
    elif command == 'load_quotes':
        load_quotes()
    elif command == 'search':
        search()


if __name__ == '__main__':
    main()