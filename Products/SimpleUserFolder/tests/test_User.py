# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from unittest import makeSuite,main,TestCase
from cPickle import UnpickleableError, dumps

from Products.SimpleUserFolder.User import User

class Tests(TestCase):

    def setUp(self):
        self.user = User({    'name':'test',
                          'password':'tpassword',
                             'roles':['role1','role2']})


    def test_pickle(self):
        self.assertRaises(UnpickleableError,dumps,self.user)

    def test_immutable(self):
        try:
            self.user.x = 1
        except:
            pass
        else:
            self.fail('User object was not immutable')

    def test_Password(self):
        self.assertEqual(self.user.__,'tpassword')

    def test_name(self):
        self.assertEqual(self.user.name,'test')

    def test_domains(self):
        self.assertEqual(self.user.domains,())

    def test_roles(self):
        self.assertEqual(self.user.roles,['role1','role2'])

    def test_authenticate(self):
        # make sure the user object has an athenticate method
        assert callable(self.user.authenticate)

    def test__getPassword(self):
        self.assertEqual(self.user._getPassword(),'tpassword')

    def test_getDomains(self):
        self.assertEqual(self.user.getDomains(),())

    def test_getRoles(self):
        self.assertEqual(self.user.getRoles(),('role1','role2','Authenticated'))

    def test_getUserName(self):
        self.assertEqual(self.user.getUserName(),'test')        

def test_suite():
    return makeSuite(Tests)

if __name__=='__main__':
    main(defaultTest='test_suite')
