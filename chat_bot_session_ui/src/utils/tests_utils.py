import os
import csv

def create_txt_file_in_tests(filename) : 
    tests_dir = os.path.join(os.getcwd(), "tests")
    os.makedirs(tests_dir, exist_ok=True)
    file_path = os.path.join(tests_dir, filename)
    return file_path





