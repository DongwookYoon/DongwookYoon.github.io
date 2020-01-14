import json
from enum import Enum

class PubType(Enum):
    UNDEFINED = 0
    FULL_PAPER = 1

class Author(object):
    def __init__(self, s_author):
        l_names = s_author.split()
        self.first_name = l_names[0]
        self.last_name = l_names[-1]

    def ToShortStr(self):
        return self.last_name + ", " + self.first_name[0] + "."

class Authors(object):
    def __init__(self, s_authors):
        self.authors = []
        for s_author in s_authors.replace(" and ", " ").split(","):
            self.authors.append(Author(s_author))

    def ToShortStr(self):
        return ", ".join(list(map(lambda x: Author.ToShortStr(x), self.authors)))

class Venue(object):
    @staticmethod
    def GetVenue(s_venue, year):
        if s_venue in ["CHI", "CSCW", "UIST", "Learning at Scale"]:
            return VenueConference(s_venue, year)
        elif s_venue == "Information and Learning Sciences":
            return VenueJournal(s_venue, year)
        elif s_venue in ["ICCE"]:
            return VenueElsewhere(s_venue, year)
        else:
            raise Exception(s_venue)

    def __init__(self, s_venue, year):
        self.s_venue = s_venue
        self.year = year

class VenueConference(Venue):
    def ToShortStr(self):
        return "Proc. " + self.s_venue + "'" + str(self.year%100)

class VenueJournal(Venue):
    def ToShortStr(self):
        return self.s_venue + " " + str(self.year)

class VenueElsewhere(Venue):
    def ToShortStr(self):
        return "In Proc. " + self.s_venue + "'" + str(self.year%100)

class Pub(object):
    def __init__(self, s):
        self.title = s["title"]
        self.authors = Authors(s["authors"])
        self.venue = Venue.GetVenue(s["venue"], int(s["year"]))
        self.pub_type = PubType.UNDEFINED
        self.award = s["award"] if "award" in s.keys() else ""
    def printForDepartmentalExternalReview(self):
        print (f"{self.authors.ToShortStr()}, {self.title} ({self.venue.ToShortStr()}){('' if self.award == '' else ', ' + self.award)}.")

class Pubs(object):
    def __init__(self, s_pubs):
        self.pubs = set()
        for s_pub in s_pubs:
            self.pubs.add(Pub(s_pub))
    def RunByYear(self, func):
        for pub in sorted(self.pubs, key=lambda pub: pub.venue.year, reverse=True):
            func(pub)

if __name__ == "__main__":
    with open("files/data.json", "r") as readfile:
        d = json.load(readfile)
        pubs = Pubs(d["publications"])
        pubs.RunByYear(Pub.printForDepartmentalExternalReview)
