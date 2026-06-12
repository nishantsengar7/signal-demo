# Django Signal Demo

A hands-on Django project that demonstrates the **three core behaviours** of Django signals through runnable management commands.

---

## What this project covers

| # | Behaviour | Command |
|---|-----------|---------|
| 1 | Signals are **synchronous** – they block the caller | `test_signal_sync` |
| 2 | Signals run on the **same thread** as the caller | `test_signal_thread` |
| 3 | Signals share the **same database transaction** as the caller | `test_signal_transaction` |

---

## Project Structure

```
signaldemo/
├── manage.py
├── signaldemo/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── demo/                   # Main app
    ├── models.py            # Item, LogEntry models
    ├── signals.py           # Three post_save signal handlers
    ├── apps.py
    ├── rectangle.py         # Iterable Rectangle utility class
    └── management/
        └── commands/
            ├── test_signal_sync.py         # Demo 1: Synchronous signals
            ├── test_signal_thread.py       # Demo 2: Same-thread signals
            ├── test_signal_transaction.py  # Demo 3: Same-transaction signals
            └── test_rectangle.py           # Rectangle iteration demo
```

---

## Prerequisites

- Python 3.10+
- pip

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/nishantsengar7/signal-demo.git
cd signal-demo

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install django

# 4. Apply migrations
python manage.py migrate
```

---

## Running the Demos

### Demo 1 — Signals are Synchronous

Proves that a `post_save` signal **blocks** the calling thread until the handler finishes.  
The handler sleeps for 5 seconds; the main thread cannot proceed until it returns.

```bash
python manage.py test_signal_sync
```

**Expected output:**
```
============================================================
  Django Signal Synchronicity Test
============================================================

[MAIN]   BEFORE Item.objects.create() -> 12:00:00.000000
[MAIN]   Calling Item.objects.create(name="test") ...

  [SIGNAL] Handler started  at: 12:00:00.001000
  [SIGNAL] Sleeping for 5 seconds...
  [SIGNAL] Handler finished at: 12:00:05.003000
  [SIGNAL] Total time in handler: 5.00s

[MAIN]   AFTER  Item.objects.create() returned -> 12:00:05.004000

[RESULT] Total wall-clock time: 5.00s
[RESULT] Signal ran SYNCHRONOUSLY -- main thread was blocked for ~5 seconds while the handler executed.
============================================================
```

---

### Demo 2 — Signals Run on the Same Thread

Proves that the signal handler runs on the **exact same thread** as the code that triggered it.

```bash
python manage.py test_signal_thread
```

**Expected output:**
```
============================================================
  Django Signal Same-Thread Test
============================================================

[MAIN] Thread BEFORE create() : name='MainThread'  id=12345
[MAIN] Calling Item.objects.create(name="thread_test") ...

  [SIGNAL] Thread name : MainThread
  [SIGNAL] Thread ID   : 12345

[MAIN] Thread AFTER  create() : name='MainThread'  id=12345

[RESULT] If the thread name and ID inside [SIGNAL] match [MAIN], signals run on the SAME thread as the caller.
============================================================
```

---

### Demo 3 — Signals Share the Same Database Transaction

Proves that any DB writes made inside a signal handler are part of the **caller's transaction**.  
If the caller rolls back, the signal's writes are rolled back too.

```bash
python manage.py test_signal_transaction
```

**Expected output:**
```
============================================================
  Django Signal Same-Transaction Test
============================================================

[MAIN] Opening transaction.atomic() block...
[MAIN] Calling Item.objects.create(name="txn_test")...
[MAIN] Item created: pk=1, name="txn_test"

  [SIGNAL] Created LogEntry pk=1 ('Logged from signal') -- shares the caller's transaction.

[MAIN] LogEntry count INSIDE transaction (before rollback): 1
[MAIN] Raising exception to force rollback...

[MAIN] Caught exception: "Force rollback"
[MAIN] transaction.atomic() block has been rolled back.

[MAIN] Item.objects.count()     (after rollback): 0
[MAIN] LogEntry.objects.count() (after rollback): 0

[RESULT] Both counts are 0 -- the signal's DB write was rolled back together with the caller's write.
[RESULT] Django signals share the SAME database transaction as the caller by default.
============================================================
```

---

## Models

### `Item`
```python
class Item(models.Model):
    name = models.CharField(max_length=100)
```

### `LogEntry`
```python
class LogEntry(models.Model):
    message = models.CharField(max_length=200)
```

---

## Signal Handlers (`demo/signals.py`)

| Handler | Trigger condition | Demonstrates |
|---------|-------------------|--------------|
| `on_item_saved_sync` | `item.name` starts with `"test"` | Synchronous blocking (5s sleep) |
| `on_item_saved_thread` | `item.name` starts with `"thread_test"` | Same-thread execution |
| `on_item_saved_txn` | `item.name` starts with `"txn_test"` | Shared transaction |

---

## Key Takeaways

> **Django signals are synchronous, single-threaded, and transactional by default.**

1. **Synchronous**: The sender waits for every connected handler to finish before continuing.  
2. **Same thread**: Handlers execute in the exact same OS thread as the sender.  
3. **Same transaction**: DB writes in a handler are part of the sender's active transaction — a rollback affects both.

---

## License

MIT
