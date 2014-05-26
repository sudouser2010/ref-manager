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

text_data = """
[
    {
    "type": "article",
	"title": "A grey-box approach for automated gui-model generation of mobile applications",
	"authors":  ["Wei Yang", "Mukul Prasad", "Tao Xie"],
	"journal": "Fundamental Approaches to Software Engineering Lecture Notes in Computer Science",
	"volume" : "7793",
	"year": "2013",
	"pages": "250-265",
    "link": "http://link.springer.com/chapter/10.1007/978-3-642-37057-1_19",
    "doi": "10.1007/978-3-642-37057-1_19"
    },

    {
    "type": "article",
	"title": "A whitebox approach for automated security testing of android applications on the cloud",
	"authors":  ["N Esfahani", "T Kacem", "N Mirzaei", "S Malek", "A Stavrou" ],
	"journal": "Automation of Software Test",
	"year": "2013",
	"pages": "22 - 28",
    "link": "http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6228986&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6228986",
    "doi": "10.1109/IWAST.2012.6228986"
    },

    {
    "type": "article",
	"title": "Testing android apps through symbolic execution",
	"authors":  ["Nariman Mirzaei", "Sam Malek", "Corina Pasareanu", "Naeem Esfahani", "Riyadh Mahmood"],
	"journal": "ACM SIGSOFT Software Engineering Notes",
	"volume" : "37",
    "issue" : "6",
	"year": "2012",
    "link":"http://dl.acm.org/citation.cfm?id=2382798"
    },

    {
    "type": "article",
	"title": "Web vulnerability study of online pharmacy sites",
	"authors":  ["Joanne Kuzma"],
	"journal": "Informatics for Health and Social Care",
	"volume" : "36",
    "issue" : "1",
	"year": "2011",
    "pages": "20 - 34",
    "doi": "10.3109/17538157.2010.520418"
    },

    {
    "type": "article",
	"title": "Integrative software design for reliability: Beyond models and defect prediction",
	"authors":  ["Abhaya Asthana","Kazu Okumoto"],
	"journal": "Bell Labs Technical Journal",
	"volume" : "17",
    "issue" : "3",
	"year": "2012",
    "pages": "37 - 59",
    "doi": "10.1002/bltj"
    },

    {
    "type": "article",
	"title": "A method of a priori software reliability evaluation",
	"authors":  [ "Dmitry Maevsky" , "Svetlana Yaremchuk" , "Ludmila Shapa"],
	"journal": "Reliability: Theory and Applications",
	"volume" : "9",
    "issue" : "1",
	"year": "2014",
    "pages": "64 - 72",
    "link": "http://gnedenko-forum.org/Journal/2014/012014/RTA_1_2014-02.pdf"
    },

    {
    "type": "article",
	"title": "Survey on software testing practices",
	"authors":  [ "J Lee", "S Kang", "D Lee"],
	"journal": "IET Software",
	"volume" : "6",
    "issue" : "3",
	"year": "2012",
    "pages": "275 - 282",
    "doi": "10.1049/iet-sen.2011.0066"
    },

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
    },

    {
    "type": "article",
	"title": "WebMate: A tool for testing web 2.0 applications",
	"authors":  [ "Valentin Dallmeier", "Martin Burger", "Tobias Orth", "Andreas Zeller"],
	"journal": "Software Quality. Increasing Value in Software and Systems Development",
	"volume" : "133",
	"year": "2013",
    "pages": "55 - 69",
    "doi": "10.1007/978-3-642-35702-2_5"
    }


]
"""
def generateAuthorsFromList(author_list):
    """
    method assumes author_list is not null
    """
    authors_fragment = ""
    count = len(author_list)
    i=0
    #--------------------------------------
    while i < count:
        first_name, last_name = author_list[i].split()
        authors_fragment += "%s, %s." % (last_name , first_name[0])

        if i < count - 1:
            #before and on the second to last author
            authors_fragment += ", "

        if i == count - 2:
            #on the second to last author
            authors_fragment += "& "
        i += 1
    #--------------------------------------
    return authors_fragment

def generateReference(reference):
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
                    authors_fragment = generateAuthorsFromList(reference["authors"])
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
                journal_fragment +=", %s" % (volume)
            #---------------------------------------------------generate volume


            #------------------------------------generate issue
            """
            The issue is not necessary
            """
            if issue:
                journal_fragment +="(%s)" % (issue)
            #------------------------------------generate issue


            #---------------------------------------------------generate page
            """
            The pages is not necessary
            """
            if pages:
                journal_fragment +=", %s" % (pages)
            #---------------------------------------------------generate page


            #--------------------------------place period at the end of fragment
            journal_fragment +="."
            #--------------------------------place period at the end of fragment


            #-----------------------------------------------generate doi or link
            """
            The doi and/or link are not needed.

            If both a link and a doi are present, the doi will supercede the link
            """
            if doi:
                doi_fragment +=" doi: %s" % (doi)
            elif link:
                link_fragment +=" Retrieved from %s" % (link)
            #-----------------------------------------------generate doi or link

            return authors_fragment + " " + year_fragment + " " + title_fragment + " " +journal_fragment + doi_fragment + link_fragment


def generateReferences(references):
    """
    input is an array of references
    """
    for reference in references:
		print generateReference(reference)
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
		self.list_data 	= json.loads(self.text_data)
		self.authors	= [ "M Prasanna", "K Chandran", "K Thiruvenkadam"]




	def test_generateAuthorsFromList(self):
		authors = generateAuthorsFromList(self.authors)
		self.assertEqual(authors, "Prasanna, M., Chandran, K., & Thiruvenkadam, K.")
		print "generate author test passed"



	def test_generateReference(self):
		reference = generateReference(self.list_data)
		self.assertEqual(reference, "Prasanna, M., Chandran, K., & Thiruvenkadam, K. (2011). Automatic test case generation for unified modelling language collaboration diagrams. ETE Journal of Research, 57(1), 77 - 81. doi: 10.4103/0377-2063.78373" )
		print "generate reference test passed"



print generateReferences( json.loads(text_data) )
#unittest.main()









