#  Copyright 2019-2020 Simon Zigelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import re

import aiohttp
from dateutil.relativedelta import relativedelta, MO

PREFIX = "https://www.jw.org/en/library/jw-meeting-workbook"


async def get_month_name(month):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(month, "Invalid month")


async def extract(start_date, end_date=None):
    last_monday = start_date + relativedelta(weekday=MO(-1))

    async with aiohttp.ClientSession() as session:
        weeks = {}
        response_code = 200
        while response_code == 200:
            next_sunday = last_monday + relativedelta(days=6)
            if last_monday.year >= 2020:
                url = await get_2020_url(last_monday, next_sunday)
            else:
                url = await get_url(last_monday, next_sunday)

            print(url)
            async with session.get(url) as resp:
                response_code = resp.status
                if resp.status == 200:
                    print("Download completed. Parsing...")
                    content = await resp.text()
                    times = await parse(content)
                    print(times)
            weeks[last_monday] = times
            last_monday = last_monday + relativedelta(days=7)
            if end_date is not None and last_monday > end_date:
                response_code = 404
    await session.close()
    return weeks


async def parse(content):
    times = []
    times_tmp = re.findall("\([0-9]+ min.*?\)", content)
    for t in times_tmp:
        ti = re.findall("[0-9]+", t)
        times.append(int(ti[0]))
    return times


async def get_url(last_monday, next_sunday):
    month = await get_month_name(last_monday.month)
    if last_monday.month == next_sunday.month:
        url = "%s/%s-%s-mwb/meeting-schedule-%s%s-%s/" % (
            PREFIX, month.lower(), last_monday.year, month.lower(), last_monday.day, next_sunday.day)
    else:
        next_month = await get_month_name(next_sunday.month)
        url = "%s/%s-%s-mwb/meeting-schedule-%s%s-%s%s/" % (
            PREFIX, month.lower(), last_monday.year, month.lower(), last_monday.day, next_month.lower(),
            next_sunday.day)
    return url


async def get_2020_url(last_monday, next_sunday):
    month = await get_month_name(last_monday.month)
    if last_monday.month == next_sunday.month:
        url = "%s/%s-%s-mwb/Our-Christian-Life-and-Ministry-Schedule-for-%s-%s-%s-%s/" % (
            PREFIX, month.lower(), last_monday.year, month, last_monday.day, next_sunday.day,
            last_monday.year)
    else:
        next_month = await get_month_name(next_sunday.month)
        if last_monday.year == next_sunday.year:
            url = "%s/%s-%s-mwb/Our-Christian-Life-and-Ministry-Schedule-for-%s-%s-%s-%s-%s/" % (
                PREFIX, month.lower(), last_monday.year, month, last_monday.day, next_month,
                next_sunday.day, last_monday.year)
        else:
            url = "%s/%s-%s-mwb/Our-Christian-Life-and-Ministry-Schedule-for-%s-%s-%s-%s-%s-%s/" % (
                PREFIX, month.lower(), last_monday.year, month, last_monday.day, last_monday.year,
                next_month, next_sunday.day, next_sunday.year)
    return url