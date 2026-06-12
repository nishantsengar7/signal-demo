from django.core.management.base import BaseCommand

from demo.rectangle import Rectangle


class Command(BaseCommand):
    help = 'Iterates over a Rectangle and prints each dimension dict.'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '=' * 40)
        self.stdout.write('  Rectangle __iter__ Demo')
        self.stdout.write('=' * 40 + '\n')

        rect = Rectangle(length=10, width=5)
        self.stdout.write(f'Created: {rect!r}\n')

        for dim in rect:
            self.stdout.write(str(dim))

        self.stdout.write('\n' + '=' * 40 + '\n')
