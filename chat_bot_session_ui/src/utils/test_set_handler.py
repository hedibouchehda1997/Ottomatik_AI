from typing import Dict, List


class TestSetHandler : 
    def __init__(self,test_set_dict : Dict) :
        self.test_set_dict = test_set_dict 
        print("from TestSetHandler")
        print(self.test_set_dict["metrics"])



