pytinycdb
=========

A very simple python interface to the tinycdb DBM library ( http://www.corpit.ru/mjt/tinycdb.html ).

Installation
============

::

    pip install tinycdb

Usage
=====

Example #1 writing::

    import tinycdb

    db = tinycdb.create('foo.db')
    db['foo'] = 'bar'
    db['bar'] = 'baz'
    print 'foo' in db # Prints True
    print 'moo' in db # Prints False
    db.close()

Example #2 reading::

    import tinycdb
    db = tinycdb.read('foo.db')
    if 'foo' in db :
        print "Found"
        print db['foo']
    else :
        print "Not found"

Thats all.

Authors & Contributors
======================

- Jeethu Rao <jeethu@jeethurao.com>;
- Brent Pedersen (https://bitbucket.org/brentp);
- Mikhail Korobov <kmike84@gmail.com>.