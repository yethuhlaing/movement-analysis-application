import datetime
import matplotlib.pyplot as plt

current_date = datetime.date.today()
current_time = datetime.datetime.now().time().strftime("%H:%M:%S")

COLOR = '#%02x%02x%02x' % (174, 239, 206)
STYLE_SHEETS = plt.style.available

# button_font = font.Font(family="Bookman Old Style", size=10)
# text_font = font.Font(family="Bookman Old Style", size=12)
