def add_source(config):
    source = raw_input("What is the source path?: ")
    if os.path.exists(source):
        print("Adding ({0})...".format(source))
        config['source'].append(source)

        ans = raw_input("Add more paths? (y/n): ")
        if ans in {"y", "Y"}:
            get_source(config)
    else:
        print("Path does not exist!")
        get_source(config)

def remove_source(config):
    if len(config['source']) == 0:
        print "Nothing to remove here."

    else:
        for path in config['source']:
            ans = raw_input("Remove {0}? (y/n):".format(path))
            if ans in {"y", "Y"}:
                config['source'].remove(path)

def view_source(config):
    if len(config['source']) == 0:
        print "Nothing to see here."

    else:
        for path in config['source']:
            print path
            ans = raw_input()
