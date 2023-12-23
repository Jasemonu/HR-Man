from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from leave import Leave
from engine import storage

storage.connect()

scheduler = BlockingScheduler()


def reset_remaining():
    print("Resetting remaining values...")
    leave_docs = Leave.objects()
    for leave_doc in leave_docs:
        leave_doc.remaining = 30
        leave_doc.save()
    print("Reset completed.")

scheduler.add_job(reset_remaining, 'cron', minute=1)

#sceduler.add_job(reset_remaining, 'cron', month=1, day=1)

# Start the scheduler
scheduler.start()

