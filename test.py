import unittest
import pytinycdb
import os

class TestCase(unittest.TestCase) :
    _TEST_DB_FILENAME = 'test.cdb'
    def tearDown( self ) :
        os.unlink(self._TEST_DB_FILENAME)

    def _setitem( self, db, k, v ) :
        db[k] = v

    def test( self ) :
        db = pytinycdb.create(self._TEST_DB_FILENAME)
        data = os.urandom(100)
        db['foo'] = data
        db['bar'] = 'hello world'
        self.assertEqual('foo' in db,True)
        self.assertEqual('moo' in db,False)
        self.assertRaises(TypeError,lambda : db['foo'])
        db.close()
        db1 = pytinycdb.read(self._TEST_DB_FILENAME)
        self.assertEqual(db1['foo'],data)
        self.assertRaises(KeyError,lambda : db1['moo'])
        self.assertRaises(TypeError,lambda : self._setitem(db1,'foo','bar'))

if __name__ == '__main__' :
    unittest.main()
