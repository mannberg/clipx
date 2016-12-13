from datetime import datetime, date, timedelta

class DateHandler:

    @staticmethod
    def date_from_alias(alias, offset=None):

        alias = DateHandler.check_for_weekday_shortform(alias)
        if alias in DateHandler.weekdays():
            date = DateHandler.date_from_weekday(alias)
            return DateHandler.date_with_offset(date, offset)

        try:
            date = {
                'today': DateHandler.today(),
                'tomorrow': DateHandler.tomorrow(),
                'yesterday': DateHandler.yesterday()
                }[alias]
            return DateHandler.date_with_offset(date, offset)
        except:
            return None

    @staticmethod
    def week_from_alias(alias, offset=None):
                try:
                    week = {
                        'tw': DateHandler.current_week(),
                        }[alias]
                    return DateHandler.week_with_offset(week, offset)
                except:
                    return None

    @staticmethod
    def offset_from_alias(alias, offset):
        alias = DateHandler.check_for_weekday_shortform(alias)

        if offset is None:
            return offset
        elif alias in ['today', 'tomorrow', 'yesterday']:
            return offset
        elif alias in DateHandler.weekdays():
            return offset * 7
        elif alias == 'tw':
            return offset * 7

        return offset

    @staticmethod
    def check_for_weekday_shortform(alias):
        if alias in ['mon', 'monday']:
            return 'monday'
        elif alias in ['tue', 'tuesday']:
            return 'tuesday'
        elif alias in ['wed', 'wednesday']:
            return 'wednesday'
        elif alias in ['thu', 'thursday']:
            return 'thursday'
        elif alias in ['fri', 'friday']:
            return 'friday'
        elif alias in ['sat', 'saturday']:
            return 'saturday'
        elif alias in ['sun', 'sunday']:
            return 'sunday'

        return alias

    @staticmethod
    def date_from_string(string, frmt, offset=None):
        date = datetime.strptime(string, frmt).date()
        return date_with_offset(date, offset)

    @staticmethod
    def date_with_offset(date, offset):
        if offset is not None:
            date = date + timedelta(days=offset)
        return date

    @staticmethod
    def week_with_offset(week, offset):
        if offset is not None:
            week = week + offset
        return week

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
    def current_week():
        return date.today().isocalendar()[1]

    @staticmethod
    def date_from_weekday(day):
        weekday = day.lower()

        weekdays = DateHandler.weekdays()

        if weekday not in weekdays:
            return None

        today_index = datetime.today().weekday()
        weekday_index = weekdays.index(weekday)
        index_diff = weekday_index - today_index
        new_date = date.today() + timedelta(days=index_diff)

        return new_date

    @staticmethod
    def weekdays():
        return [
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
                    ]
