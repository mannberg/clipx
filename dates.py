from datetime import datetime, date, timedelta

class DateHandler:

    @staticmethod
    def date_from_shortform(shortform):
        try:
            return {
                'today': DateHandler.today(),
                'tomorrow': DateHandler.tomorrow(),
                'yesterday': DateHandler.yesterday(),
                'monday': DateHandler.date_from_weekday('monday'),
                'tuesday': DateHandler.date_from_weekday('tuesday'),
                'wednesday': DateHandler.date_from_weekday('wednesday'),
                'thursday': DateHandler.date_from_weekday('thursday'),
                'friday': DateHandler.date_from_weekday('friday'),
                'saturday': DateHandler.date_from_weekday('saturday'),
                'sunday': DateHandler.date_from_weekday('sunday')
                }[shortform]
        except:
            return None

    @staticmethod
    def date_from_string(string, frmt):
        return datetime.strptime(string, frmt).date()

    @staticmethod
    def today():
        return datetime.today()

    @staticmethod
    def tomorrow():
        tomorrow = date.today() + timedelta(days=1)
        return tomorrow

    @staticmethod
    def yesterday():
        yesterday = date.today() - timedelta(days=1)
        return yesterday

    @staticmethod
    def date_from_weekday(day):

        weekday = day.lower()

        weekdays = [
                    'monday',
                    'tuesday',
                    'wednesday',
                    'thursday',
                    'friday',
                    'saturday',
                    'sunday'
                    ]

        if weekday not in weekdays:
            return None

        today_index = datetime.today().weekday()
        weekday_index = weekdays.index(weekday)
        index_diff = weekday_index - today_index
        print("index diff: " + str(index_diff))
        today = date.today()

        new_date = date.today() + timedelta(days=index_diff)

        return new_date
