# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

try:
    import Zope2 as Zope
except ImportError:
    import Zope

from Acquisition import Implicit

from Products.SimpleUserFolder.SimpleUserFolder import SimpleUserFolder

class User:

    def __init__(self,password,roles,extras=None):
        self.password = password
        self.roles = roles
        if extras is not None:
            self.__dict__.update(extras)

class dummyUserSource(Implicit):

    def __init__(self):
        # setup the user registry
        self.users = {'test_user':User('password',
                                       ['role']),
                      'test_user_with_extras':User('password',
                                                   [],
                                                   {'extra1':'extra1value',
                                                    'extra2':2}),}

    def __getitem__(self,name):
        return self.users[name]

    def addUser(self,name, password, roles):
        """add a user"""
        if self.users.has_key(name):
            raise ValueError
        self.users[name] = User(password,roles)

    def editUser(self,name, password, roles):
        """edit a user"""
        user = self.users[name]
        if password is not None:
            user.password = password
        user.roles = roles

    def getUserIds(self):
        """return a list of usernames"""
        names = self.users.keys()
        names.sort()
        return names

    def getUserDetails(self,name):
        """return a dictionary for the specified user"""        
        if self.users.has_key(name):
            # nice hack, return the dict from the object
            return self.users[name].__dict__
        return None

    def deleteUser(self,name):
        """delete the specified user"""
        del self.users[name]

class dummyUserFolder(dummyUserSource,SimpleUserFolder):
    pass
    
    
