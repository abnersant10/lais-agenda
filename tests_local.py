import datetime
import calendar
data = '2022-04-03'
data = datetime.datetime.strptime(data, "%Y-%m-%d").hour
print(data)


# if data >= datetime.datetime.today() and calendar.day_name[data.weekday()] == ('Sunday' or 'Monday' or 'Tuesday'):
