# Copyright (c) 2004-2006 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from AccessControl.User import BasicUser
try:
    import cPickle
except ImportError:
    import pickle as cPickle


class User(BasicUser):

    # we don't want to support the domains thing
    domains = ()

    def __init__(self, user_dict):
        # bypass immutability
        d = self.__dict__
        d['__'] = user_dict['password']
        del user_dict['password']
        d['name'] = user_dict['name']
        del user_dict['name']
        d['roles'] = user_dict['roles']
        del user_dict['roles']
        d['extra'] = user_dict

    def __setattr__(self, name, value):
        # This type of user object should never get modified
        raise AttributeError('This object is immutable')

    def __getitem__(self, name):
        return self.extra[name]

    def __getstate__(self):
        """Don't let simple user objects get pickled"""
        raise cPickle.UnpickleableError("This object cannot be pickled")

    def _getPassword(self):
        """Return the password of the user."""
        return self.__

    def getDomains(self):
        """Return the list of domain restrictions for a user"""
        # This is always an empty tuple, since we don't support
        # domain restrictions.
        return ()

    def getRoles(self):
        """Return the list of roles assigned to a user."""
        return tuple(self.roles) + ('Authenticated', )

    def getUserName(self):
        """Return the username of a user"""
        return self.name
