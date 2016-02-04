


def entry():
    print "checking for updates"
    upgrade()
    print "launching Pyfa"
    import pyfa
    pyfa.main()

def upgrade():
    pass
