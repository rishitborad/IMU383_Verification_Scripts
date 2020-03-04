
class test_section:
    _section_number = 0

    def __init__(self, section_name):
        self.section_name = section_name
        test_section._section_number = test_section._section_number + 1
        self.section_id = test_section._section_number
        self.test_cases = []
        self.total_test_cases = 0

    def add_test_case(self, test_case):
        self.test_cases.append(test_case)
        self.total_test_cases += 1
        test_case.test_id = self.total_test_cases

    def run(self):
        print "\t" + str(self.section_id) + ". " + self.section_name + "\r\n"
        counter = 0
        for test in self.test_cases:
            #self.result = test.run()
            counter = counter + 1
            id = str(self.section_id) + "." + str(counter) + ". "
            test.run(id)

#############################################

class test_case:

    def __init__(self, case_name, handle = None, cmd = None, param = None):
        self.test_case_name = case_name
        self.handle = handle
        self.result = False
        self.cmd = cmd
        self.param = param
        self.test_id = 0

    def run(self, id):
        raise NotImplementedError("Subclass must implement abstract method")
        #print "\t\t" + self.test_case_name + "\r\n"
        #if(self.handle != None):
        #    self.result = self.handle(self.cmd, self.param)

#===========================================#

class condition_check(test_case):

    def run(self, id):
        print "\t\t" + id + self.test_case_name + "\r\n"
        if(self.handle != None):
            self.result = self.handle(self.cmd, self.param)
            result_str = "Passed" if self.result else "Failed" + "\t\t" + id + self.test_case_name + "\r\n"
            #print result_str

#===========================================#

class code(test_case):

    def run(self, id):
        print "\t\t" + id + self.test_case_name + "\r\n"
        if(self.handle != None):
            self.result = self.handle()
            result_str = "Passed" if self.result else "Failed" + "\t\t" + id + self.test_case_name + "\r\n"
            #print result_str
