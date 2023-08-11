import datetime

current_date = datetime.date.today()
current_time = datetime.datetime.now().time().strftime("%H:%M:%S")

COLOR = '#%02x%02x%02x' % (174, 239, 206)
