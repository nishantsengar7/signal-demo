from django.core.management.base import BaseCommand
from django.db import transaction

from demo.models import Item, LogEntry


class Command(BaseCommand):
    help = 'Shows that a signal rollback takes the signal\'s DB writes with it.'

    def handle(self, *args, **options):
        # clean slate so counts are unambiguous
        Item.objects.filter(name__startswith='txn_test').delete()
        LogEntry.objects.filter(message='Logged from signal').delete()

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('  Django Signal Same-Transaction Test')
        self.stdout.write('=' * 60)
        self.stdout.write('\n[MAIN] Opening transaction.atomic() block...')

        try:
            with transaction.atomic():
                self.stdout.write('[MAIN] Calling Item.objects.create(name="txn_test")...')
                item = Item.objects.create(name='txn_test')
                self.stdout.write(f'[MAIN] Item created: pk={item.pk}, name="{item.name}"')
                self.stdout.write(
                    f'[MAIN] LogEntry count INSIDE transaction (before rollback): '
                    f'{LogEntry.objects.count()}'
                )
                self.stdout.write('[MAIN] Raising exception to force rollback...')
                raise Exception('Force rollback')

        except Exception as exc:
            self.stdout.write(f'\n[MAIN] Caught exception: "{exc}"')
            self.stdout.write('[MAIN] transaction.atomic() block has been rolled back.\n')

        item_count = Item.objects.filter(name__startswith='txn_test').count()
        log_count = LogEntry.objects.filter(message='Logged from signal').count()

        self.stdout.write(f'[MAIN] Item.objects.count()     (after rollback): {item_count}')
        self.stdout.write(f'[MAIN] LogEntry.objects.count() (after rollback): {log_count}')

        if item_count == 0 and log_count == 0:
            self.stdout.write(
                "\n[RESULT] Both counts are 0 -- the signal's DB write was"
                " rolled back together with the caller's write."
            )
            self.stdout.write(
                '[RESULT] Django signals share the SAME database transaction'
                ' as the caller by default.'
            )
        else:
            self.stdout.write('\n[RESULT] UNEXPECTED: some rows survived the rollback!')

        self.stdout.write('=' * 60 + '\n')
