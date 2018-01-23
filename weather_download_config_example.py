
#  Special note for timezones:
#  From https://en.wikipedia.org/wiki/Tz_database#Area
#  "The special area of "Etc" is used for some administrative zones, 
#  particularly for "Etc/UTC" which represents Coordinated Universal Time. In 
#  order to conform with the POSIX style, those zone names beginning with 
#  "Etc/GMT" have their sign reversed from the standard ISO 8601 convention. In 
#  the "Etc" area, zones west of GMT have a positive sign and those east have a 
#  negative sign in their name (e.g "Etc/GMT-14" is 14 hours ahead of GMT.)"
#  
#  This is especially relevant because the timezones in the Environment Canada
#  data are non-DST timezones, so you do *not* want to use the typical named
#  timezone for the area, but rather the Etc/GMT+X timezone.  In particular,
#  the Canadian timezones are all Etc/GMT+X (using the + rather than -).


# Format:
# site: is the site ID used by environment canada
# filename: is a format string to use for the output file.  Named parameters for
#  year and month are used.
# timezone: is the environment canada timezone used for the site.  See the note
#  above for some relevant info.
# outtimezone: (optional) The timezone to use in the output/downloaded file.
#  If this argument is not used, the timezone of the output is whatever timezone
#  environment canada used in the file.

class WeatherDownloaderConfig:
  sites = [
    {'site':41883, 'filename':'{year:04d}-{month:02d}-Inuvik-EnvironmentCanada.csv', 'timezone':'Etc/GMT+7', 'outtimezone':'UTC'},
    {'site':48168, 'filename':'{year:04d}-{month:02d}-Whitehorse-EnvironmentCanada.csv', 'timezone':'Etc/GMT+8', 'outtimezone':'UTC'},
    ]
