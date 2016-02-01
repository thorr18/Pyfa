print "module main"
print __name__
def main():
    print "enter main()"
    if __name__ == '__main__':
        print "yes __main__"
        import pyfa
    else:
        print "not main"
        import pyfa
    print "exit main()"

print "half done main module"
if __name__ == '__main__':
    print "yes __main__ 2"
    import pyfa
else:
    print "not main 2"
    import pyfa
print "exit main module"
