class A2ui():
    def __init__(self):
        self.initPaths()
        self.db = a2dblib.check(self.a2setdir)

        print('available modules and parts:\n')
        self.getMods()
        for m in self.mods:
            print('module: ' + str(m))

        print('a2ui initialised!')

    def getMods(self):
        """
        lists all available modules as a dictionary
        {'modname':modObject,...}
        """
        self.mods = {}
        for mod in os.listdir(self.a2dir + '/modules'):
            self.mods[mod] = Mod(mod, self.a2moddir, self.db)

        print('self.mods: ' + str(self.mods))

    def initPaths(self):
        """
        makes sure all necessary paths and their variables are available
        """
        # if run on its own sys.path[0] will be the script dir
        self.a2uidir = sys.path[0]
        if not self.a2uidir:
            self.a2uidir = 'C:/My Files/code/a2/ui'
        self.a2dir = os.path.dirname(self.a2uidir)
        self.a2libdir = self.a2dir + '/' + 'lib/'
        #
        self.a2exe = self.a2dir + '/a2Starter.exe'
        self.a2ahk = self.a2dir + '/a2.ahk'
        # WIP - temporary under a2dir!! has to be VARIABLE!
        self.a2setdir = self.a2dir + '/' + 'settings/'
        self.a2moddir = self.a2dir + '/' + 'modules/'
        # test if all necessary directories are present:
        mainItems = [self.a2ahk, self.a2exe, self.a2libdir, self.a2moddir, self.a2setdir, self.a2uidir]
        missing = [p for p in mainItems if not os.path.exists(p)]
        if missing:
            raise Exception('a2ui start interrupted! ' + str(missing) + ' not found in main dir!')
        if not os.access(self.a2setdir, 1):
            raise Exception('a2ui start interrupted! ' + self.a2setdir + ' inaccessable!')
