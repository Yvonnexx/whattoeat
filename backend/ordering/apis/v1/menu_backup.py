from ordering import app
from flask import jsonify
from HTMLParser import HTMLParser, HTMLParseError

from datetime import date

import requests
import re

MENU_URL = ('http://www.aramarkcafe.com/components/menu_weekly_alternate.aspx'
            '?locationid=2846&pageid=20&menuid=12926')

WEEKDAY = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri'}


class Error(Exception):
    pass


class DuplicatedDayError(Error):
    def __inti__(self):
        self.msg = 'Duplicated days when parsing HTML.'

    def __str__(self):
        return repr(self.msg)


class WeekendsError(Error):
    def __init__(self):
        self.msg = 'Resturant close on weekends'

    def __str__(self):
        return repr(self.msg)


class SymantecMenuParser(HTMLParser):
    """Customized HTML parser for parsing the menu.

    This class defines a customized parser to parse the menu website.
    It takes the stringified html and produces a dictionary object
    in the following format:
        {
            day1: {
                kind1: [name1, name2, name3],
                kind2: [name4, name5, name6],
            },
            day2: {
                kind3: [name7, name8],
            }
        }
    where 'day' is the day of the week, ie: 'Mon'
          'kind' is the type of the dish, ie: 'Breakfast'
          'name' is the name of the dish, ie: 'Chicken Salad'
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.menu = {}
        self.day = False
        self.kind = False
        self.name = False
        self.day_value = ''
        self.kind_value = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                if attr[0] == 'id' and attr[1] == 'column_container':
                    self.name = True

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'header':
                    self.day = True

        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'subhead':
                    self.kind = True

    def handle_data(self, data):
        data = re.sub('\t|\n|\r', '', data).strip(' ')

        if not data:
            return

        if self.day:
            self.day_value = data

            if self.menu.get(self.day_value):
                raise DuplicatedDayError

            self.menu[self.day_value] = {}
            self.day = False
        elif self.kind:
            self.kind_value = data

            if not self.day_value:
                raise HTMLParseError('No day found for this kind')

            if self.menu.get(self.day_value) is None:
                raise HTMLParseError('%s didn\'t get parsed' % self.day_value)

            self.menu[self.day_value][self.kind_value] = []
            self.kind = False
        elif self.name:
            if not self.day_value:
                raise HTMLParseError('No day found for this name')

            if not self.kind_value:
                raise HTMLParseError('No kind found for this name')

            if self.menu.get(self.day_value) is None:
                raise HTMLParseError('%s didn\'t get parsed' % self.day_value)

            if self.menu[self.day_value].get(self.kind_value) is None:
                raise HTMLParseError('%s didn\'t get parsed' % self.kind_value)

            this_kind = self.menu[self.day_value][self.kind_value]
            l = len(this_kind)

            # The data handler breaks when it hits '&', but we don't
            # want this happen, so here we concatenate the broken
            # words.
            if l > 1 and this_kind[l-1] == '&':
                and_symbol = this_kind.pop()
                first = this_kind.pop()
                data = ' '.join([first, and_symbol, data])

            self.menu[self.day_value][self.kind_value].append(data)


@app.route('/menu', methods=['GET'])
def get_menu():
    menu_html_request = requests.get(MENU_URL)
    menu_html = menu_html_request.text

    menu_parser = SymantecMenuParser()
    try:
        menu_parser.feed(menu_html)
    except Exception, e:
        print e.msg

    try:
        today = date.weekday(date.today())
        today = 0;
        if today > 4:
            raise WeekendsError()
    except Exception, e:
        print e.msg
        return (jsonify(message='Close on weekends, no order available.'),
                404,)

    day = WEEKDAY[today]
    menu = menu_parser.menu

    return jsonify(**menu[day])

if __name__ == '__main__':
    from pprint import pprint

    menu_html_request = requests.get(MENU_URL)
    menu_html = menu_html_request.text

    menu_parser = SymantecMenuParser()
    menu_parser.feed(menu_html)

    pprint(menu_parser.menu)
