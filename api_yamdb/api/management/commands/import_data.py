from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import User, Title, Genre, Category, Comment, Review


class Command(BaseCommand):
    help = 'Накачка БД из данных csv файлов'

    def handle(self, *args, **options):
        for row in DictReader(open('./static/data/users.csv',
                                   encoding='utf-8')):
            user = User(id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        bio=row['bio'],
                        role=row['role'])
            user.save()

        for row in DictReader(open('./static/data/titles.csv',
                                   encoding='utf-8')):
            title = Title(id=row['id'],
                          name=row['name'],
                          year=row['year'],
                          category=Category.objects.get(id=row['category']))
            title.save()

        for row in DictReader(open('./static/data/genre.csv',
                                   encoding='utf-8')):
            genre = Genre(id=row['id'],
                          slug=row['slug'],
                          name=row['name'])
            genre.save()

        for row in DictReader(open('./static/data/comments.csv',
                                   encoding='utf-8')):
            comment = Comment(id=row['id'],
                              text=row['text'],
                              pub_date=row['pub_date'],
                              author=User.objects.get(id=row['author']),
                              review=Review.objects.get(id=row['review_id']))
            comment.save()

        for row in DictReader(open('./static/data/review.csv',
                                   encoding='utf-8')):
            review = Review(id=row['id'],
                            text=row['text'],
                            pub_date=row['pub_date'],
                            score=row['score'],
                            author=User.objects.get(id=row['author']),
                            title=Title.objects.get(id=row['title_id']))
            review.save()

        for row in DictReader(open('./static/data/category.csv',
                                   encoding='utf-8')):
            category = Category(id=row['id'],
                                slug=row['slug'],
                                name=row['name'])
            category.save()
