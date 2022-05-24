#-------------------------------------------------------------------------------
# Name:        reference manager
# Purpose:
#
# Author:      HDizzle
#
# Created:     09/May/2014
# Copyright:   (c) HDizzle 2014
# License:     MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import json
import unittest
#from sample_data import text_data
#from chp1 import text_data
#from chp2 import text_data
from chp3 import text_data

class makeReference:

    def __init__(self, reference_data):
        self.reference  = reference_data
        self.title      = reference_data.get('title',    False)
        self.authors    = reference_data.get('authors',  False)
        self.journal    = reference_data.get('journal',  False)
        self.volume     = reference_data.get('volume',   False)
        self.issue      = reference_data.get('issue',    False)
        self.year       = reference_data.get('year',     False)
        self.pages      = reference_data.get('pages',    False)
        self.link       = reference_data.get('link',     False)
        self.doi        = reference_data.get('doi',      False)
        self.type       = reference_data.get("type",     False)
        self.umi        = reference_data.get("umi",      False)

        self.school_name    = reference_data.get("school_name",         False)
        self.school_location= reference_data.get("school_location",     False)
        self.pub_city       = reference_data.get("pub_city",            False)
        self.pub_state      = reference_data.get("pub_state",           False)
        self.publisher      = reference_data.get("publisher",           False)



        #------------------------initialization
        self.title_fragment     = ""
        self.authors_fragment   = ""
        self.year_fragment      = "(n.d.)."
        self.journal_fragment   = ""
        self.origin_fragment    = ""
        self.generated_reference= ""
        self.all_types          = {"article", "thesis", "thesis-unpub", "dissertation", "dissertation-unpub", "book",
                                    "website"}
        #------------------------initialization

    def generate_authors_from_list(self):
        """
        method assumes self.authors is not null and is a list
        """
        self.authors_fragment = ""
        count = len(self.authors)
        i = 0
        #--------------------------------------
        while i < count:
            try:
                first_name, last_name = self.authors[i].split()
                self.authors_fragment += "%s, %s." % (last_name, first_name[0])
            except:
                self.authors_fragment += "%s" % (self.authors[i])

            if i < count - 1:
                #before and on the second to last author
                self.authors_fragment += ", "

            if i == count - 2:
                #on the second to last author
                self.authors_fragment += "& "
            i += 1
        #--------------------------------------


    def generate_authors(self, required = True):
        """
        According to the apa, if there are no authors, then self.authors remains an empty string.

        Also, if the author is an organization, the author is simply just the organization.

        source: https://owl.english.purdue.edu/owl/resource/560/06/

        When author is an organization or a dissertation or thesis use the first (primary) author
        """

        #----------------------------------------generate authors from list
        if self.authors:
            if self.type in {"website", "thesis", "thesis-unpub", "dissertation", "dissertation-unpub"} :
                self.authors = [self.authors[0]]
                self.generate_authors_from_list()
            elif self.type == "org":
                self.authors_fragment = self.authors[0]
            else:
                self.generate_authors_from_list()

        if required and self.authors_fragment == "":
            raise Exception("No Authors Included")
        #----------------------------------------generate authors from list

    def generate_year(self, required = True):
        """
        whenever there's no date n.d. is used

        http://psychology.about.com/b/2010/11/03/how-to-cite-an-online-article-with-no-date.htm
        """

        #----------------------------------------generate year
        if self.year:
            self.year_fragment = "(%s)." % (self.year)

        if required and self.year_fragment == "":
            raise Exception("No Year Included")
        #----------------------------------------generate year


    def generate_title(self, required = True):
        """
        A title must be included as a part of the reference

        According to apa only the first word and proper nouns should be capitalized.

        Also, the first word after a colon should be capitalized
        Because it is too challenging for the code to determine proper nouns, this will be
        left to the descretion of the user

        http://www.bemidjistate.edu/students/wrc/writing_sources/apa/references/

        http://www.bibme.org/citation-guide/APA/journal
        http://www.roanestate.edu/owl/apa-citations.htm

        http://employees.csbsju.edu/proske/nursing/apa.htm
        """

        #-----------------------------------------------------generate title
        if self.title:
            self.title_fragment = "%s" % (self.title)
            if self.type    == "thesis":
                self.title_fragment += " (Master's thesis)"
            elif self.type  == "thesis-unpub":
                self.title_fragment += " (Unpublished master's thesis)"
            elif self.type  == "dissertation":
                self.title_fragment += " (Doctoral dissertation)"
            elif self.type  == "dissertation-unpub":
                self.title_fragment += " (Unpublished doctoral dissertation)"

        self.title_fragment += "."
        if required and self.title_fragment == "":
            raise Exception("No Title Included")
        #-----------------------------------------------------generate title

    def generate_journal(self, required = True):

        #-------------------------------------generate journal
        """
        Significant words of a journal title are capitalized. This is left to the users discretion as well
        http://library.ucf.edu/rosen/guide_apa.php
        """
        if self.journal:
            self.journal_fragment = "%s" % (self.journal)
        #-------------------------------------generate journal

        #---------------------------------------------------generate volume
        """
        The volume is not necessary
        """
        if self.volume:
            self.journal_fragment += ", %s" % (self.volume)
        #---------------------------------------------------generate volume


        #------------------------------------generate issue
        """
        The issue is not necessary
        """
        if self.issue:
            self.journal_fragment += "(%s)" % (self.issue)
        #------------------------------------generate issue


        #---------------------------------------------------generate page
        """
        The pages is not necessary
        """
        if self.pages:
            self.journal_fragment += ", %s" % (self.pages)
        #---------------------------------------------------generate page


        #--------------------------------place period at the end of fragment
        self.journal_fragment += "."
        #--------------------------------place period at the end of fragment

        if required and self.journal_fragment == "":
            raise Exception("No Journal Included")

    def generate_origin(self, required = True):
        """
            This method will create an origin based on doi, link, umi, or school.

            rules for apa citation of thesis and dissertation are available here:
            https://owl.english.purdue.edu/owl/resource/560/09/
            http://www.umuc.edu/library/libhow/apa_examples.cfm#thesis
            http://library.ciis.edu/information/handouts/citing%20dissertations.htm

            can access umi's from here: http://dissexpress.umi.com
        """

        #-----------------------------------------------generate origin
        if self.umi and self.type in {"thesis", "thesis-unpub", "dissertation", "dissertation-unpub"}:
            #for thesis and dissertations published in the US
            self.origin_fragment = "Retrieved from ProQuest Dissertations and Theses. (UMI No. %s)." % (self.umi)
        elif self.school_name and self.school_location:
            #for published thesis/dissertation in print or unpublished thesis/dissertations
            #the location is given as city, state
            self.origin_fragment = "%s, %s." % (self.school_name, self.school_location)
        elif self.doi:
            #for only articles have them
            self.origin_fragment = "doi: %s" % (self.doi)
        elif self.link:
            #for articles, thesis/dissertations
            self.origin_fragment = "Retrieved from %s" % (self.link)
        elif self.pub_city and self.publisher:
            #for books in print
            self.origin_fragment = "%s" % (self.pub_city)

            if self.pub_state:
                self.origin_fragment += ", %s" % (self.pub_state)

            self.origin_fragment += ": %s" % (self.publisher)

        if required and self.origin_fragment == "":
            raise Exception("No Origin Included")
        #-----------------------------------------------generate origin

    def check_reference_for_errors(self):
        """
        this function will help the user enter correct information for each type
        """

        #------------------------------------all citations need author, year, title
        assert self.authors,    "authors not present"
        assert self.year,       "year not present"
        assert self.title,      "link not present"
        #------------------------------------all citations need author, year, title

        if self.type == "website":
            #website must have a link
            assert self.link, "link not present"

        if self.type == "article":
            #article must have a journal
            assert self.journal, "journal not present"

        if self.type == "book":
            #book must have a (city and publisher) or (a link)
            assert (self.pub_city and self.publisher) or self.link, \
                "(no publisher and no city) or no link present"

        if self.type in {"thesis-unpub", "dissertation-unpub"}:
            #unpublished thesis and dissertations must have links or (school name and location)
            assert (self.school_name and self.school_location) or self.link , \
                "(no school name and no school location) or no link present"

        if self.type in {"thesis", "dissertation"}:
            #published thesis and dissertations must have umi
            assert self.umi, "link not present"

    def generate_reference(self):

        self.check_reference_for_errors()
        self.generate_authors()
        self.generate_year()
        self.generate_title()


        if self.type in {"website","book", "thesis", "thesis-unpub", "dissertation", "dissertation-unpub"}:
            self.generate_origin()
            self.generated_reference = self.authors_fragment + " " + self.year_fragment + " " + self.title_fragment + \
                                       " " + self.origin_fragment
        elif self.type == "article":
            self.generate_journal()
            self.generate_origin(False)
            self.generated_reference = self.authors_fragment + " " + self.year_fragment + " " + self.title_fragment + \
                                       " " + self.journal_fragment + " " + self.origin_fragment



class makeReferences:
    """
       This class makes references with the reference data
       which is stored as JSON
    """

    def __init__(self, data):
        self.references_json = json.loads(data)
        self.references      = []


    def make_references(self):
        for reference in self.references_json:
            local_reference = makeReference(reference)
            local_reference.generate_reference()
            self.references.append(local_reference.generated_reference)

    def sort_references(self):
        self.references.sort()

    def print_references(self):
        for reference in self.references:
            print reference

    def generate_references(self):
        self.make_references()
        self.sort_references()
        self.print_references()


class generateReferenceTest(unittest.TestCase):

    def setUp(self):
        reference1 = """
        {
        "type": "article",
        "title": "Automatic test case generation for unified modelling language collaboration diagrams",
        "authors":  [ "M Prasanna", "K Chandran", "K Thiruvenkadam"],
        "journal": "ETE Journal of Research",
        "volume" : "57",
        "issue" : "1",
        "year": "2011",
        "pages": "77 - 81",
        "doi": "10.4103/0377-2063.78373"
        }
        """

        reference2 = """
        {
        "type": "thesis",
        "title": "Portable game based instruction of American sign language",
        "authors": [ "Christyna Wilson" ],
        "journal": "All Theses",
        "year": "2013",
        "link": "http://tigerprints.clemson.edu/cgi/viewcontent.cgi?article=2760&context=all_theses",
        "umi": "1544218"
        }
        """
        self.reference1 = makeReference(json.loads(reference1))
        self.reference2 = makeReference(json.loads(reference2))

    def test_generate_reference(self):
        self.reference1.generate_reference()
        self.reference2.generate_reference()

        self.assertEqual(self.reference1.generated_reference,
            "Prasanna, M., Chandran, K., & Thiruvenkadam, K. (2011). Automatic test case generation for "
            "unified modelling language collaboration diagrams. ETE Journal of Research, "
            "57(1), 77 - 81. doi: 10.4103/0377-2063.78373" )
        print "reference for article test passed"

        self.assertEqual(self.reference2.generated_reference,
            "Wilson, C. (2013). Portable game based instruction of American sign language (Master's thesis)."
            " Retrieved from ProQuest Dissertations and Theses. (UMI No. 1544218)." )
        print "reference for published thesis test passed"


#unittest.main()
makeReferences(text_data).generate_references()


