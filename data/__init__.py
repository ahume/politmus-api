import csv
import logging
import json
import datetime
import codecs

from models import User, MPVote, Question

def import_users():

    jdata = open('fixtures/dev_users.json').read()
    d = json.loads(jdata)

    for row in d:
        u = User()
        u.username = row['username']
        u.gender = row['gender']
        u.age = row['age']
        u.ethnicity = row['ethnicity']
        u.postcode = row['postcode']
        u.constituency = row['constituency']
        u.mp = row['mp']
    
        u.put()
        print row['username']


def import_questions():
    csvfile = open('fixtures/mp_votes/vote_questions.csv', 'rU')
    for row in csv.reader(csvfile):
        d = Question()
        d.question = row[0]
        d.title = row[1]
        d.date = datetime.datetime.now()
        d.publicwhip_url = row[3]
        d.put()

def import_mp_votes(subset=False):

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

    question_list = {
        'afghanistan': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgHDA',
        'badgers': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgBDA',
        'blasphemy': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgDDA',
        'detention': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgLDA',
        'homosexuality': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgEDA',
        'royalmail': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgKDA',
        'sanctions': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgJDA',
        'sixteen': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgFDA',
        'smacking': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgCDA',
        'tuitionfees': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgGDA',
        'vat': 'ag1kZXZ-d2hpcGl0YXBwcg4LEghRdWVzdGlvbhgIDA'
    }


    for question in question_list:

        print question

        csvfile = open('fixtures/mp_votes/%s.csv' % question, 'rU')
        for row in csv.reader(csvfile):

            if subset and row[1] not in subset_const and row[0] not in subset_mp:
                continue

            try:
                v = MPVote()
                v.question = question_list[question]
                v.name = row[0]
                v.constituency = row[1]
                v.party = normalise_party(row[2])
                v.selection = normalise_selection(row[3])
                v.whilst = get_whilst(row[2])

                v.put()
            except:
                print "Failed insert"


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