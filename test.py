import unittest
import tinycdb
import os

class TinyCDBTestCase(unittest.TestCase):
    _TEST_DB_FILENAME = 'test.cdb'
    def setUp(self):
        self.db = tinycdb.TinyCDB(self._TEST_DB_FILENAME, mode="w")

    def test_writes(self):
        data = os.urandom(100)
        db = self.db

        db['foo'] = data
        db['bar'] = 'hello world'
        self.assertEqual('foo' in db,True)
        self.assertEqual('moo' in db,False)
        self.assertRaises(TypeError,lambda : db['foo'])
        self.assert_(hasattr(db, "__setitem__"))
        db.close()

        db1 = tinycdb.TinyCDB(self._TEST_DB_FILENAME, mode="r")
        self.assertEqual(db1['foo'],data)
        self.assertRaises(KeyError,lambda : db1['moo'])
        self.assert_(not hasattr(db1, "__setitem__"))

    def test_repr(self):
        db = self.db
        self.assertEqual(repr(db), "TinyCDB('test.cdb', 'w')")
        db.close()

        db1 = tinycdb.TinyCDB(self._TEST_DB_FILENAME, mode="r")
        self.assertEqual(repr(db1), "TinyCDB('test.cdb', 'r')")
        db1.close()

    def tearDown( self ) :
        os.unlink(self._TEST_DB_FILENAME)

class TestCase(unittest.TestCase) :
    _TEST_DB_FILENAME = 'test.cdb'
    def tearDown( self ) :
        os.unlink(self._TEST_DB_FILENAME)

    def _setitem( self, db, k, v ) :
        db[k] = v

    def test( self ) :
        db = tinycdb.create(self._TEST_DB_FILENAME)
        data = os.urandom(100)
        db['foo'] = data
        db['bar'] = 'hello world'
        self.assertEqual('foo' in db,True)
        self.assertEqual('moo' in db,False)
        self.assertRaises(TypeError,lambda : db['foo'])
        db.close()
        db1 = tinycdb.read(self._TEST_DB_FILENAME)
        self.assertEqual(db1['foo'],data)
        self.assertRaises(KeyError,lambda : db1['moo'])
        self.assertRaises(TypeError,lambda : self._setitem(db1,'foo','bar'))

if __name__ == '__main__' :
    unittest.main()
