from datetime import datetime, date, timedelta

class BadValueException(Exception):
    pass

class DateHandler:

    @staticmethod
    def date_from_alias(alias, offset=None):

        alias = DateHandler.weekday_from_alias(alias)
        if alias in DateHandler.weekdays():
            date = DateHandler._date_from_weekday(alias)
            return DateHandler._date_with_day_offset(date, offset)

        try:
            date = {
                'today': DateHandler.today(),
                'tomorrow': DateHandler.tomorrow(),
                'yesterday': DateHandler.yesterday()
                }[alias]
            return DateHandler._date_with_day_offset(date, offset)
        except:
            return None

    @staticmethod
    def week_from_alias(alias, offset=None):
                try:
                    week = {
                        'tw': DateHandler.current_week(),
                        'nw': DateHandler.next_week(),
                        'lw': DateHandler.last_week()
                        }[alias]
                    return DateHandler._week_with_offset(week, offset)
                except:
                    return None

    @staticmethod
    def day_offset_from_alias(alias, offset):
        alias = DateHandler.weekday_from_alias(alias)

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
    def weekday_from_alias(alias):
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
        try:
            if not all((string, frmt)):
                raise BadValueException

            date = datetime.strptime(string, frmt).date()
            return DateHandler._date_with_day_offset(date, offset)
        except (TypeError, BadValueException):
            return None

    @staticmethod
    def dates_in_week(week):
        dates = []
        week_string = "2017-W{}".format(str(week))

        for x in range(1, 8):
            if x == 7:
                x = 0
            w = '-{}'.format(x)
            date = datetime.strptime(week_string + w, "%Y-W%W-%w").date()
            dates.append(date)
        return dates

    @staticmethod
    def _date_with_day_offset(date, offset):
        if offset is not None:
            date = date + timedelta(days=offset)
        return date

    @staticmethod
    def _week_with_offset(week, offset):
        if offset is not None:
            week = week + offset
        return week

    @staticmethod
    def today():
        return date.today()

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
    def next_week():
        d = date.today() + timedelta(days=7)
        return d.isocalendar()[1]

    @staticmethod
    def last_week():
        d = date.today() - timedelta(days=7)
        return d.isocalendar()[1]

    @staticmethod
    def _date_from_weekday(day):
        weekday = day.lower()
        weekdays = DateHandler.weekdays()

        if weekday not in weekdays:
            return None

        today_index = date.today().weekday()
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
