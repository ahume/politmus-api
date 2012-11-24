import csv
import logging
import json
import datetime
import codecs

from google.appengine.ext import db

from models import User, MP, MPVote, Question, Constituency

def import_users():

    jdata = open('fixtures/dev_users.json').read()
    d = json.loads(jdata)

    if User.all().count() < 1:

        for row in d:
            u = User()
            u.username = row['username']
            u.gender = row['gender']
            u.age = row['age']
            u.ethnicity = row['ethnicity']
            u.postcode = row['postcode']
            u.constituency = row['constituency']
            u.constituency_score = row['constituency_score']
            u.mp_score = row['mp_score']
            u.mp = row['mp']
        
            u.put()
            print row['username']

def import_mp_votes(subset=False):

    if MPVote.all().count() > 0:
        print "Import already complete"
        return

    subset_const = [
        "Brighton, Kemptown",
        "Brighton, Pavillion",
        "Hove",
        "Hackney South and Shoreditch",
        "Edinburgh North, and Leith"
    ]
    subset_mp = [
        "Caroline Lucas",
        "Simon Kirby",
        "Mike Weatherley",
        "Meg Hillier",
        "Mark Lazarowicz"
    ]

    question_list = {}

    csvfile = open('fixtures/mp_votes/vote_questions.csv', 'rU')
    for row in csv.reader(csvfile):
        d = Question()
        d.question = row[0]
        d.title = row[1]
        d.date = datetime.datetime.now()
        d.publicwhip_url = row[3]
        d.put()

        question_list[row[4]] = d

    mps_created = []
    consts_created = []

    for question in question_list:

        print question

        csvfile = open('fixtures/mp_votes/%s.csv' % question, 'rU')
        for row in csv.reader(csvfile):

            if subset and row[1] not in subset_const and row[0] not in subset_mp:
                continue

            try:
                v = MPVote(parent=question_list[question])
                v.question = str(question_list[question].key())
                v.mp_name = row[0]
                v.mp_slug = slugify(row[0])
                v.mp_constituency = row[1]
                v.mp_party = normalise_party(row[2]).lower()
                v.selection = normalise_selection(row[3])
                v.mp_whilst = get_whilst(row[2])
                v.put()

                if v.mp_slug not in mps_created:
                    mp = MP()
                    mp.slug = v.mp_slug
                    mp.name = v.mp_name
                    mp.constituency = v.mp_constituency
                    mp.party = v.mp_party
                    mp.put()
                    mps_created.append(v.mp_slug)

                if v.mp_constituency not in consts_created:
                    const = Constituency()
                    const.name = v.mp_constituency
                    const.slug = slugify(v.mp_constituency)
                    const.mp_name = v.mp_name
                    const.mp_party = v.mp_party
                    const.put()
                    consts_created.append(v.mp_constituency)

            except:
                print "Failed insert"


def slugify(name):
    return ''.join(c.lower() for c in name if not c.isspace())

def normalise_party(party):
    return party.replace("whilst", "")

def normalise_selection(selection):

    if "aye" in selection:
        return "aye"

    if "no" in selection:
        return "no"

    if "both" in selection:
        return "both"

    print "WTF is this: %s", selection 

def get_whilst(party):
    if "whilst" in party:
        return True
    else:
        return False