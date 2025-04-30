from db import db
from models import Time
frome datetime import datetime as dt


def time_keeper():

    current_time_row = db.session.query(Time).first()
    if not current_time_row:
        current_time_row = Time(current_time= dt.now())
        db.session.add(current_time_row)
        db.session.commit()

    try:
        while True:
            try:
                current_time_row.current_time = dt.now()
                db.session.commit()
                # print(f'The current time is: {current_time_row.current_time}')
            except OperationalError as e:
                print("Database is locked. Rolling commit back and retrying in 5.0 seconds...")
                db.session.rollback()  # important: undo the failed transaction
                time.sleep(5)  # wait and retry
                continue
            time.sleep(1)  # normal delay
    except KeyboardInterrupt:
        print("Stopped updating.")
    finally:
        db.session.close()