#-------------------------------------------------------------------------------
# Name:        reference manager
# Purpose:
#
# Author:      HDizzle
#
# Created:     09/May/2014
# Copyright:   (c) Junior 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import json
import unittest
from sample_data import text_data

class referenceMaker:

    def generate_authors_from_list(self, author_list):
        """
        method assumes author_list is not null
        """
        authors_fragment = ""
        count = len(author_list)
        i = 0
        #--------------------------------------
        while i < count:
            first_name, last_name = author_list[i].split()
            authors_fragment += "%s, %s." % (last_name, first_name[0])

            if i < count - 1:
                #before and on the second to last author
                authors_fragment += ", "

            if i == count - 2:
                #on the second to last author
                authors_fragment += "& "
            i += 1
        #--------------------------------------
        return authors_fragment


    def generate_reference(self, reference):
        if reference["type"] == "article":

            title   = reference.get('title',    False)
            authors = reference.get('authors',  False)
            journal = reference.get('journal',  False)
            volume  = reference.get('volume',   False)
            issue   = reference.get('issue',    False)
            year    = reference.get('year',     False)
            pages   = reference.get('pages',    False)
            link    = reference.get('link',     False)
            doi     = reference.get('doi',      False)
            special = reference.get('special',  False)


            #------------------------initialization
            title_fragment      = ""
            authors_fragment    = ""

            journal_fragment    = ""
            year_fragment       = "(n.d.)."
            link_fragment       = ""
            doi_fragment        = ""
            #------------------------initialization



            #----------------------------------------generate authors from list
            """

            According to the apa, if there are no authors, then authors_list remains an empty string.

            Also, if the author is an organization, the author is simply just the organization.

            source: https://owl.english.purdue.edu/owl/resource/560/06/



            When the author is an organization, code takes the first element in author list.

            example: The reference will have a key of "special":{"author_is_org": true}
            Otherwise it generates authors by <last name>, <first name letter>
            """
            if authors:
                if special:
                    author_is_org = special.get("author_is_org", False)
                    if author_is_org:
                        #when author is an organization
                        authors_fragment = reference["authors"][0]
                else:
                    authors_fragment = self.generate_authors_from_list(reference["authors"])
            #----------------------------------------generate authors from list


            #----------------------------------------generate year
            """
            whenever there's no date n.d. is used

            http://psychology.about.com/b/2010/11/03/how-to-cite-an-online-article-with-no-date.htm

            """
            if year:
                year_fragment = "(%s)." % (year)
             #----------------------------------------generate year

            #-----------------------------------------------------generate title
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
            if title:
                title_fragment = "%s." % (title)
            else:
                raise Exception("No Title Included")
            #-----------------------------------------------------generate title

            #-------------------------------------generate journal
            """
            A journal name must be included as a part of the reference.

            Significant words of a journal title are capitalized. This is left to the users descretion as well
            http://library.ucf.edu/rosen/guide_apa.php
            """
            if journal:
                journal_fragment = "%s" % (journal)
            else:
                raise Exception("No Journal Included")
            #-------------------------------------generate journal


            #---------------------------------------------------generate volume
            """
            The volume is not necessary

            """
            if volume:
                journal_fragment += ", %s" % (volume)
            #---------------------------------------------------generate volume


            #------------------------------------generate issue
            """
            The issue is not necessary
            """
            if issue:
                journal_fragment += "(%s)" % (issue)
            #------------------------------------generate issue


            #---------------------------------------------------generate page
            """
            The pages is not necessary
            """
            if pages:
                journal_fragment += ", %s" % (pages)
            #---------------------------------------------------generate page


            #--------------------------------place period at the end of fragment
            journal_fragment += "."
            #--------------------------------place period at the end of fragment


            #-----------------------------------------------generate doi or link
            """
            The doi and/or link are not needed.

            If both a link and a doi are present, the doi will supercede the link
            """
            if doi:
                doi_fragment += " doi: %s" % (doi)
            elif link:
                link_fragment += " Retrieved from %s" % (link)
            #-----------------------------------------------generate doi or link

            return authors_fragment + " " + year_fragment + " " + title_fragment + " " +journal_fragment + doi_fragment + link_fragment


    def generate_references(self, references):
        """
        input is an array of references
        """
        for reference in references:
            print self.generate_reference(reference)
            print ""


class generateReferenceTest(unittest.TestCase):

    def setUp(self):
        self.text_data = """
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
        self.list_data  = json.loads(self.text_data)
        self.authors    = [ "M Prasanna", "K Chandran", "K Thiruvenkadam"]




    def test_generate_authors_from_list(self):
        reference_maker = referenceMaker()
        authors = reference_maker.generate_authors_from_list(self.authors)
        self.assertEqual(authors, "Prasanna, M., Chandran, K., & Thiruvenkadam, K.")
        print "generate author test passed"



    def test_generate_reference(self):
        reference_maker = referenceMaker()
        reference = reference_maker.generate_reference(self.list_data)
        self.assertEqual(reference, "Prasanna, M., Chandran, K., & Thiruvenkadam, K. (2011). Automatic test case generation for unified modelling language collaboration diagrams. ETE Journal of Research, 57(1), 77 - 81. doi: 10.4103/0377-2063.78373" )
        print "generate reference test passed"


print referenceMaker().generate_references( json.loads(text_data) )
#unittest.main()

