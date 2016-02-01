print "module entry"
print __name__
def entry():
    print "enter entry()"
    if __name__ == '__main__':
        print "yes __main__"
        import pyfa
    else:
        print "not main"
        import pyfa
    print "exit entry()"

print "half done entry module"
if __name__ == '__main__':
    print "yes __main__ 2"
    import pyfa
else:
    print "not main 2"
    import pyfa
print "exit entry module"
