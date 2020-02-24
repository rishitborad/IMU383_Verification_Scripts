
class test_section:
    _section_number = 0

    def __init__(self, section_name):
        self.section_name = section_name
        test_section._section_number += 1
        self.section_number = test_section._section_number
        self.test_cases = []
        self.total_test_cases = 0
        #self.result = False

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)
        self.total_test_cases += 1

    def run(self):
        print "\t" + self.section_name + "\r\n"
        for test in self.test_cases:
            #self.result = test.run()
            test.run()

#############################################

class test_case:

    def __init__(self, case_name, handle = None, cmd = None, param = None):
        self.test_case_name = case_name
        self.handle = handle
        self.result = False
        self.cmd = cmd
        self.param = param

    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")
        #print "\t\t" + self.test_case_name + "\r\n"
        #if(self.handle != None):
        #    self.result = self.handle(self.cmd, self.param)

class default_checks(test_case):
    
    def run(self):
        print "\t\t" + self.test_case_name + "\r\n"
        if(self.handle != None):
            self.result = self.handle(self.cmd, self.param)

class code(test_case):

    def run(self):
        print "\t\t" + self.test_case_name + "\r\n"
        if(self.handle != None):
            self.result = self.handle()
