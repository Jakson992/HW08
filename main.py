import argparse
from mongoengine import *

connect(db="web12", host="mongodb+srv://JekaWEB12:567234@cluster0.plizfca.mongodb.net/?retryWrites=true&w=majority")

parser = argparse.ArgumentParser(description='Cats APP')
parser.add_argument('--action', help='Command: create, update, find, remove')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--fullname')
parser.add_argument('--born_date')
parser.add_argument('--born_location')
parser.add_argument('--description', nargs='+')


arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
fullname = my_arg.get('fullname')
born_date = my_arg.get('born_date')
_id = my_arg.get('id')
description = my_arg.get('description')


class Authors(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = StringField(required=True)
    born_location = StringField(max_length=120, required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}


class Quotes(Document):
    author = ReferenceField(Authors)
    tags = ListField(StringField(max_length=50))
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}


def create(fullname, born_date, born_location, description):
    author = Authors(
        fullname=fullname,
        born_date=born_date,
        born_location=born_location,
        description=description
    )
    author.save()
    return author


def find_quotes_by_author(fullname):
    author = Authors.objects(fullname=fullname).first()
    if author:
        quotes = Quotes.objects(author=author)
        return quotes
    else:
        return None


def find_quotes_by_tag(tag):
    quotes = Quotes.objects(tags=tag)
    return quotes


def find_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quotes.objects(tags__in=tags_list)
    return quotes

def main():
    while True:
        command = input("Введіть команду: ")
        if command == "exit":
            print("Дякую за використання. До побачення!")
            break
        elif command.startswith("name:"):
            fullname = command.split(":")[1].strip()
            quotes = find_quotes_by_author(fullname)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = find_quotes_by_tag(tag)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip()
            quotes = find_quotes_by_tags(tags)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()