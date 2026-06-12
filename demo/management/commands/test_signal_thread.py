import threading

from django.core.management.base import BaseCommand

from demo.models import Item


def current_thread_info():
    t = threading.current_thread()
    return f"name='{t.name}'  id={threading.get_ident()}"


class Command(BaseCommand):
    help = 'Shows that the signal handler runs on the same thread as the caller.'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('  Django Signal Same-Thread Test')
        self.stdout.write('=' * 60)

        self.stdout.write(f'\n[MAIN] Thread BEFORE create() : {current_thread_info()}')
        self.stdout.write('[MAIN] Calling Item.objects.create(name="thread_test") ...\n')

        Item.objects.create(name='thread_test')

        self.stdout.write(f'[MAIN] Thread AFTER  create() : {current_thread_info()}')
        self.stdout.write(
            '\n[RESULT] If the thread name and ID inside [SIGNAL] match'
            ' [MAIN], signals run on the SAME thread as the caller.'
        )
        self.stdout.write('=' * 60 + '\n')
