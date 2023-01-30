from flask import Flask, render_template, redirect, url_for, request
import time


def editTimestruck(struct_time, yearin=None, monthin=None, dayin=None, hourin=None, minin=None):
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    minute = struct_time.tm_min
    if not yearin is None:
        year = yearin
    if not monthin is None:
        month = monthin
    if not dayin is None:
        day = dayin
    if not hourin is None:
        hour = hourin
    if not minin is None:
        minute = minin
    try:
        return time.strptime('{} {} {} {} {}'.format(year, month, day, hour, minute), '%Y %m %d %H %M')
    except ValueError:
        return False


def weekdayIsDayInMonth(year, month, day):
    return weekday(year, month, day) + ' ' + isDayInMonth(year, month, day)


def weekday(year, month, day):
    try:
        return time.strftime('%A', time.strptime('{} {} {}'.format(year, month, day), '%Y %m %d'))
    except ValueError:
        return "hidden"


def isDayInMonth(year, month, day):
    try:
        time.strptime('{} {} {}'.format(year, month, day), '%Y %m %d')
        try:
            time.strptime('{} {} {}'.format(year, month, day + 1), '%Y %m %d')
            try:
                time.strptime('{} {} {}'.format(year, month, day - 1), '%Y %m %d')
                return "visible middle"
            except ValueError:
                return "visible first"
        except ValueError:
            return "visible last"
    except ValueError:
        return "hidden"


events = [{'timeStart': time.strptime('{} {} {} {} {}'.format(2023, 12, 24, 0, 0), '%Y %m %d %H %M'),
           'timeEnd': time.strptime('{} {} {} {} {}'.format(2023, 12, 24, 0, 0), '%Y %m %d %H %M'),
           'title': 'Christmas Eve',
           'description': 'Christmas Eve is the evening or entire day before Christmas Day, the festival commemorating the birth of Jesus. Christmas Day is observed around the world, and Christmas Eve is widely observed as a full or partial holiday in anticipation of Christmas Day. Christmas Eve is also known as the Feast of the Vigil of the Nativity or the Feast of the Incarnation, and this is reflected in the Eucharistic prayer used in the Mass of the Christmas Vigil.'},
          {'timeStart': time.strptime('{} {} {} {} {}'.format(2023, 12, 25, 0, 0), '%Y %m %d %H %M'),
           'timeEnd': time.strptime('{} {} {} {} {}'.format(2023, 12, 25, 23, 59), '%Y %m %d %H %M'),
           'title': 'Christmas Day',
           'description': 'Christmas Day is an annual festival commemorating the birth of Jesus Christ, observed most commonly on December 25 as a religious and cultural celebration among billions of people around the world. A feast central to the Christian liturgical year, it closes the Advent season and initiates the twelve days of Christmastide, which ends after the twelfth night. Christmas Day is a public holiday in many of the world\'s nations, is celebrated religiously by a majority of Christians, as well as culturally by many non-Christians, and forms an integral part of the holiday season centered around it.'},
          {'timeStart': time.strptime('{} {} {} {} {}'.format(2023, 8, 24, 0, 0), '%Y %m %d %H %M'),
           'timeEnd': time.strptime('{} {} {} {} {}'.format(2023, 8, 24, 0, 0), '%Y %m %d %H %M'),
           'title': 'My birthday', 'description': 'nothing special'}]

allEventsInYear = []


def ifEvent(year, month, day):
    if not isDayInMonth(year, month, day) == "hidden":
        for event in allEventsInYear:
            if event['timeStart'] <= time.strptime('{} {} {} {} {}'.format(year, month, day, 0, 0), '%Y %m %d %H %M') <= \
                    event['timeEnd']:
                return "event"
    return "noEvent"


def event(year, month, day):
    eventList = []
    for event in allEventsInYear:
        if event['timeStart'] <= time.strptime('{} {} {} {} {}'.format(year, month, day, 0, 0), '%Y %m %d %H %M') <= \
                event['timeEnd']:
            eventList.append(event)
    return eventList


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        year = request.form['year']
    elif request.method == 'GET':
        year = request.args.get('year')
    try:
        year = int(year)
    except:
        return redirect(url_for('home', year=time.localtime().tm_year))
    global events
    global allEventsInYear
    allEventsInYear = []
    for event in events:
        try:
            repeat = event['repeat']
            if repeat == 'yearly':
                if event['timeStart'].tm_year <= int(year):
                    if editTimestruck(event['timeStart'], yearin=int(year)):
                        allEventsInYear.append({'timeStart': editTimestruck(event['timeStart'], yearin=int(year)),
                                                'timeEnd': editTimestruck(event['timeEnd'], yearin=int(year)),
                                                'title': event['title'], 'description': event['description']})
            elif repeat == "monthly":
                if event['timeStart'].tm_year <= int(year):
                    for month in range(12):
                        if editTimestruck(event['timeStart'], yearin=int(year), monthin=month + 1) and (event['timeStart'].tm_mon <= month+1 or event['timeStart'].tm_year <= int(year-1)):
                            allEventsInYear.append({'timeStart': editTimestruck(event['timeStart'], yearin=int(year),
                                                                                monthin=month + 1),
                                                    'timeEnd': editTimestruck(event['timeEnd'], yearin=int(year),
                                                                              monthin=month + 1),
                                                    'title': event['title'], 'description': event['description']})
            elif repeat == "daily":
                if event['timeStart'].tm_year <= int(year):
                    for month in range(12):
                        if event['timeStart'].tm_mon <= month+1 or event['timeStart'].tm_year <= int(year-1):
                            for day in range(31):
                                if editTimestruck(event['timeStart'], yearin=int(year), monthin=month + 1,
                                                  dayin=day + 1) and (event['timeStart'].tm_mday <= day+1 or event['timeStart'].tm_mon <= month or event['timeStart'].tm_year <= int(year-1)):
                                    allEventsInYear.append({'timeStart': editTimestruck(event['timeStart'], yearin=int(year),
                                                                                        monthin=month + 1, dayin=day + 1),
                                                            'timeEnd': editTimestruck(event['timeEnd'], yearin=int(year),
                                                                                      monthin=month + 1, dayin=day + 1),
                                                            'title': event['title'], 'description': event['description']})
        except:
           pass
        a=0
        for eventsInYear in allEventsInYear:
            if eventsInYear['title'] == event['title']:
                a+=1
        if a==0:
           if event['timeStart'].tm_year <= int(year) <= event['timeEnd'].tm_year:
               allEventsInYear.append(event)
    return render_template('kalender.html',
                           weekday=weekday,
                           weekdayIsDayInMonth=weekdayIsDayInMonth,
                           ifEvent=ifEvent,
                           year=year,
                           str=str,
                           int=int)


@app.route('/event', methods=['POST', 'GET'])
def requestEvent():
    if request.method == 'POST':
        return event(day=request.form['day'], month=request.form['month'], year=request.form['year'])
    else:
        return event(day=request.args.get('day'), month=request.args.get('month'), year=request.args.get('year'))


@app.route("/addEvent", methods=["POST", "GET"])
def addEvent():
    global events
    if request.method == 'POST':
        newEvent = {}
        if "-" in request.form['time']:
            startTime, endTime = request.form['time'].split("-")[0], request.form['time'].split("-")[1]
            startHour, startMinute = startTime.split(":")[0], startTime.split(":")[1]
            endHour, endMinute = endTime.split(":")[0], endTime.split(":")[1]
        else:
            startHour, startMinute = request.form['time'].split(":")[0], request.form['time'].split(":")[1]
            endHour, endMinute = startHour, startMinute
        if "-" in request.form['date']:
            startDate, endDate = request.form['date'].split("-")[0], request.form['date'].split("-")[1]
            startYear, startMonth, startDay = startDate.split(".")[2], startDate.split(".")[1], startDate.split(".")[0]
            endYear, endMonth, endDay = endDate.split(".")[2], endDate.split(".")[1], endDate.split(".")[0]
        else:
            startYear, startMonth, startDay = request.form['date'].split(".")[2], request.form['date'].split(".")[1], \
                                              request.form['date'].split(".")[0]
            endYear, endMonth, endDay = startYear, startMonth, startDay
        newEvent['timeStart'] = time.strptime(
            '{} {} {} {} {}'.format(startYear, startMonth, startDay, startHour, startMinute), '%Y %m %d %H %M')
        newEvent['timeEnd'] = time.strptime('{} {} {} {} {}'.format(endYear, endMonth, endDay, endHour, endMinute),
                                            '%Y %m %d %H %M')
        newEvent['title'] = request.form['title']
        newEvent['description'] = request.form['description']
        newEvent['repeat'] = request.form['repeat']
        events.append(newEvent)
        return redirect(url_for('home'))
    else:
        return render_template('kalender.html')

@app.route("/deleteEvent", methods=["POST", "GET"])
def deleteEvent():
    global events
    if request.method == 'POST':
        for event in events:
            if event['title'] == request.form['title']:
                events.remove(event)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
