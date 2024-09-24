import datetime
from suntime import Sun
import pytz


class HultSun(Sun):
    def __init__(self, lat=42.373830, lon=-71.076000):
        super().__init__(lat, lon)
        self.local_tz = pytz.timezone('US/Eastern')
        self.utc = pytz.utc
        self.fmt = '%I:%M %p'  # '%Y-%m-%d %H:%M:%S %Z%z'

    def get_todays_sunset(self):
        abd = datetime.datetime.today()
        abd_ss = self.get_sunset_time(abd)
        local_sunset_time = abd_ss.astimezone(self.local_tz)
        return local_sunset_time

    def get_sunset_from_date(self, date_isoformat):
        abd = datetime.datetime.fromisoformat(date_isoformat)
        abd_ss = self.get_sunset_time(abd)
        local_sunset_time = abd_ss.astimezone(self.local_tz)
        # print(f"Sunset on {date_isoformat} is at : ", local_sunset_time.strftime(self.fmt))
        return local_sunset_time


if __name__ == '__main__':
    sun = HultSun()

    local_sunset = sun.get_todays_sunset()
    print(local_sunset.time().strftime(sun.fmt))

    local_sunset = sun.get_sunset_from_date(datetime.date.today().isoformat())
    print(local_sunset.time().strftime(sun.fmt))

    # Get today's sunrise and sunset in UTC
    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()
    print(
        f"Today at Hult Soccer Field the sun raised at {today_sr.strftime('%H:%M')} and get down at {today_ss.strftime('%H:%M')} UTC")

    # On a special date in your machine's local time zone
    abd = datetime.datetime(2024, 3, 14)
    abd_sr = sun.get_sunrise_time(abd)
    abd_ss = sun.get_sunset_time(abd)
    print(
        f"On {abd} the sun at Hult Socccer Field raised at {abd_sr.strftime('%H:%M')} and get down at {abd_ss.strftime('%H:%M')}.")

    local_time = abd_ss.astimezone(sun.local_tz)
    print("    EPT: ", local_time.strftime(sun.fmt))
