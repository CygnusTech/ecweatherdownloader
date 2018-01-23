# ECWeatherDownloader

Script to read and process CSV files from Environment Canada.

## Setup

Copy the ecweatherdownloader_config_example.py file to ecweatherdownloader_config.py.

Edit the ecweatherdownloader_config.py file as required.

## Usage

When executed, the script will download the current month's of data for each site listed in the configuration.  If the script is run in the first week of the month, it also downloads the previous month's data.

Some processing is done to the raw Environment Canada data files.  In particular, the script also does the following:

 - Removes 'future' rows.  The Environment Canada data files also have timestamped rows for the future.  These rows are removed.
 - Adds the appropriate timezone formatting to the first column's timestamps.  If you configure the correct timezone in the configuration file (info is included within that file), the the timestamps in the output CSV will be correct and useful for integration in other systems.
 
## License
ECWeatherDownloader
Copyright (C) 2017  Cygnus Technical Services Ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
