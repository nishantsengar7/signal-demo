from datetime import datetime

from django.core.management.base import BaseCommand

from demo.models import Item


class Command(BaseCommand):
    help = 'Shows that post_save signals block the caller (5-second sleep demo).'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('  Django Signal Synchronicity Test')
        self.stdout.write('=' * 60)

        before = datetime.now()
        self.stdout.write(f'\n[MAIN]   BEFORE Item.objects.create() -> {before.strftime("%H:%M:%S.%f")}')
        self.stdout.write('[MAIN]   Calling Item.objects.create(name="test") ...')

        Item.objects.create(name='test')

        after = datetime.now()
        elapsed = (after - before).total_seconds()

        self.stdout.write(f'[MAIN]   AFTER  Item.objects.create() returned -> {after.strftime("%H:%M:%S.%f")}')
        self.stdout.write(f'\n[RESULT] Total wall-clock time: {elapsed:.2f}s')
        self.stdout.write(
            f'[RESULT] Signal ran SYNCHRONOUSLY -- main thread was blocked '
            f'for ~{elapsed:.0f} seconds while the handler executed.'
        )
        self.stdout.write('=' * 60 + '\n')
