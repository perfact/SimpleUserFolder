# Copyright (c) 2004-2010 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import Globals

from base import UsageBase, test_dir
from unittest import TestSuite, makeSuite
from os import mkdir
from os.path import exists, join
from shutil import rmtree
from dummyUserSource import User

from Products.ZSQLMethods.SQL import SQL
from Products.SQLAlchemyDA.da import manage_addSAWrapper

# monkeypatch Result.dictionaries to cater for gadfly
from Shared.DC.ZRDB.Results import Results, NoBrains

original__init__ = Results.__init__

def __init__(self,(items,data),brains=NoBrains, parent=None,
             zbrains=None):
    for item in items:
        item['name'] = item['name'].lower()
    original__init__(self,(items,data),brains=NoBrains, parent=None,
                     zbrains=None)

def addSQLMethod(obj,id):
    f=open(test_dir+'/'+id+'.sql')     
    data=f.read()     
    f.close()     

    # bits below lifted from FS ZSQL Methods

    # parse parameters
    parameters={}
    start = data.find('<dtml-comment>')
    end   = data.find('</dtml-comment>')
    if start==-1 or end==-1 or start>end:
        raise ValueError,'Could not find parameter block'
    block = data[start+14:end]

    for line in block.split('\n'):
        pair = line.split(':',1)
        if len(pair)!=2:
            continue
        parameters[pair[0].strip().lower()]=pair[1].strip()

    # check for required an optional parameters
    try:            
        title =         parameters.get('title','')
        connection_id = parameters.get('connection id',parameters['connection_id'])
        arguments =     parameters.get('arguments','')
        max_rows =      parameters.get('max_rows',1000)
        max_cache =     parameters.get('max_cache',100)
        cache_time =    parameters.get('cache_time',0)            
    except KeyError,e:
        raise ValueError,"The '%s' parameter is required but was not supplied" % e
        
    s = SQL(id,
            title,
            connection_id,
            arguments,
            data)
    s.manage_advanced(max_rows,
                      max_cache,
                      cache_time,
                      '',
                      '')
    
    obj._setObject(id, s)    
    return getattr(obj,id)     

class SQLUsers:

    def __init__(self,folder):
        self.folder = folder

    def __getitem__(self,name):
        rows = self.folder.getUserDetails(name=name)
        if not rows:
            raise KeyError,name
        password = rows[0].PASSWORD
        roles=[]
        for row in rows:
            role = row.ROLE
            if role:
                roles.append(role)
        return User(password,roles)
        
class TestsUpperCase(UsageBase):

    def _setup(self):
        
        f = self.folder
        
        # add DB Connection
        manage_addSAWrapper(f, id='sufdb', dsn='sqlite://', title='')
        
        # create tables
        addSQLMethod(f,'createTables')
        f.createTables()
        
        # methods
        addSQLMethod(f,'addUser')
        addSQLMethod(f,'deleteUser')
        addSQLMethod(f,'editUser')
        addSQLMethod(f,'getUserDetails')
        addSQLMethod(f,'getUserIds')
        
        # initial users
        f.addUser(name='test_user',password='password',roles=['role'])

        f.addUser(name='test_user_with_extras',
                  password='password',
                  roles=[],
                  extra1='extra1value',
                  extra2=2)

        self.users = SQLUsers(f)
        
    def tearDown(self):
        UsageBase.tearDown(self)
        
class TestsLowerCase(TestsUpperCase):

    def setUp(self):
        TestsUpperCase.setUp(self)
        # We patch the results class here to return lowercase
        Results.__init__ = __init__

    def tearDown(self):
        # we undo our patching here
        Results.__init__ = original__init__
        TestsUpperCase.tearDown(self)
            
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestsUpperCase))
    suite.addTest(makeSuite(TestsLowerCase))
    return suite
