# encoding: utf-8
import unittest
from functionalTest import FunctionalTest

# get all tests from SearchText and HomePageTest class
team_test = unittest.TestLoader().loadTestsFromTestCase(FunctionalTest)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([team_test])

 #run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)