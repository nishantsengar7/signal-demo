import threading
import time
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from demo.models import Item, LogEntry


@receiver(post_save, sender=Item)
def on_item_saved_sync(sender, instance, created, **kwargs):
    if not instance.name.startswith('test'):
        return

    t0 = datetime.now()
    print(f"\n  [SIGNAL] Handler started  at: {t0.strftime('%H:%M:%S.%f')}")
    print(f"  [SIGNAL] Sleeping for 5 seconds...")

    time.sleep(5)

    t1 = datetime.now()
    print(f"  [SIGNAL] Handler finished at: {t1.strftime('%H:%M:%S.%f')}")
    print(f"  [SIGNAL] Total time in handler: {(t1 - t0).total_seconds():.2f}s\n")


@receiver(post_save, sender=Item)
def on_item_saved_thread(sender, instance, created, **kwargs):
    if not instance.name.startswith('thread_test'):
        return

    t = threading.current_thread()
    print(
        f"\n  [SIGNAL] Thread name : {t.name}\n"
        f"  [SIGNAL] Thread ID   : {threading.get_ident()}\n"
    )


@receiver(post_save, sender=Item)
def on_item_saved_txn(sender, instance, created, **kwargs):
    if not instance.name.startswith('txn_test'):
        return

    entry = LogEntry.objects.create(message='Logged from signal')
    print(
        f"\n  [SIGNAL] Created LogEntry pk={entry.pk} ('{entry.message}')"
        f" -- shares the caller's transaction.\n"
    )
