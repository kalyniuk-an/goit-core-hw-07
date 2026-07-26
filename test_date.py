from datetime import datetime, timedelta

def get_upcoming_birthdays():
    upcoming = []
    contacts = ["26.07.2008","28.07.2010", "01.08.2009", "12.07.2010", "02.08.2011" ]
    today = datetime.today().date()
    # end_date = today + timedelta(days=7)
    for d_str in contacts:
      birthday_date = datetime.strptime(d_str, "%d.%m.%Y").date()
      birthday_this_year = birthday_date.replace(year=today.year)
      if birthday_this_year < today:
        birthday_this_year = birthday_this_year.replace(year=today.year+1)
      days_until_birthday = (birthday_this_year-today).days
      print ("--------------------------")
      print(days_until_birthday)
      if 0 < days_until_birthday <= 7:
         print(birthday_this_year)
         if birthday_this_year.weekday()>=5:
            delta = (7-birthday_this_year.weekday())
            print (delta)
            birthday_this_year += timedelta(days=delta)


      print(birthday_this_year)
      print ("--------------------------")
      # print (today)
      # print(end_date)
    # print(year)
    return upcoming

get_upcoming_birthdays()