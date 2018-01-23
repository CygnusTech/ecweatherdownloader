#!/usr/bin/python3

# This file is part of ECWeatherDownloader.
#
# ECWeatherDownloader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ECWeatherDownloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ECWeatherDownloader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2017 Charles Hache (chache@cygnustech.ca)

import datetime
import requests
import sys, traceback
import shutil
import csv
import pytz

from weather_download_config import WeatherDownloaderConfig

def weatherOfficeDataGet(filename, stationId, stationTimezone, outputTimezone, year, month, day):
  #URL uses GET and is http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=41883&Year=2014&Month=11&Day=11&timeframe=1&submit=Download+Data
  # The day in the URL doesn't seem to matter - it just gives us the whole month of data
  
  url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID="+str(stationId)+"&Year="+str(year)+"&Month="+str(month)+"&Day="+str(day)+"&timeframe=1&submit=Download+Data"
  #print "Trying URL: "+url
  data = requests.get(url)
  if data.status_code == 200:
    with open(filename, 'w') as f:
      f.write(data.text)
  else:
    print ('Invalid response code after retrieving data from weather.gc.ca: {}'.format(data.status_code))
    return False
    
  # The environment canada CSVs also include rows for the future.
  # It looks like valid data can be expected up until midnight local time yesterday
  # Here we modify the CSV file we downloaded to omit the empty rows.
  # Here we also change the output timezone of the data if required.
  
  todayUTC = datetime.datetime.now(pytz.UTC)
  todayLocal = todayUTC.astimezone(stationTimezone)

  filenamebak = filename+".bak"
  with open(filename, "r") as fin:
    with open(filenamebak, "w") as fout:
      csvreader = csv.reader(fin)
      csvwriter = csv.writer(fout)
      
      for row in csvreader:
        try:
          ts = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M")
        except:
          ts = None
        if ts is None:
          csvwriter.writerow(row)
        else:
          ts = stationTimezone.localize(ts)
          outts = ts.astimezone(outputTimezone)
          row[0] = outts
          
          # Do not output rows from later than midnight last night
          if ts.date() < todayLocal.date():
            csvwriter.writerow(row)
          else:
            break
  shutil.move(filenamebak, filename)
    
  return True

def retrieveDataWeatherOffice(startDate, endDate, stationId, stationTimezone, outputTimezone, filenameformat):
  
  # If the startDate and endDate are in the same month, we request the end date from the server, which will give us the whole month of data (if available, otherwise
  # it just has empty rows with timestamps for future/not collected data).  If the startDate and endDate are in different months, first we request the last day of the
  # month of startDate (which gives us that whole month) and then we request the last day of all months up to and including the endDate month.
  theYear = startDate.year
  theMonth = startDate.month
  ret = True
  while ret:
    nameParams = {'year':theYear, 'month':theMonth}
    ret = weatherOfficeDataGet(filenameformat.format(**nameParams), 
          stationId, 
          stationTimezone, 
          outputTimezone, 
          theYear, 
          theMonth, 
          1)
    if theYear >= endDate.year and theMonth >= endDate.month:
      break
    theMonth = theMonth + 1
    if theMonth == 13:
      theMonth = 1
      theYear = theYear + 1
  
  return ret


if __name__ == "__main__":
  # Request the data for the current month.
  # If we're in the first 7 days of the month, we also request the data for last
  # month, just to ensure we still get the tail end of it.
  # The corrolary is that the script needs to be run at least once a week.
  
  for siteconfig in WeatherDownloaderConfig.sites:
    site = siteconfig['site']
    filename = siteconfig['filename']
    localTimezone = pytz.timezone(siteconfig['timezone'])
    outTimezone = siteconfig.get('outtimezone', None)
    if outTimezone is not None:
      outTimezone = pytz.timezone(outTimezone)
    else:
      outTimezone = localTimezone
  
    endDateUTC = datetime.datetime.now(pytz.UTC)
    endDateLocal = endDateUTC.astimezone(localTimezone)
    startDateLocal = endDateLocal.replace(day=1)
    if endDateLocal.day <= 7:
      startDateLocal = startDateLocal - datetime.timedelta(days=1) #Last day of previous month
      startDateLocal.replace(day=1) #first day of previous month
      
    retrieveDataWeatherOffice(startDateLocal, 
        endDateLocal,
        site,
        localTimezone,
        outTimezone,
        filename)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
