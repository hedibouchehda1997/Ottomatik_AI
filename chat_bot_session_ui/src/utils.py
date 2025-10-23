from contextlib import contextmanager
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict, Tuple
import csv


@contextmanager 
def load_env(api_keys_list:List[str]) : 
    path = find_dotenv()
    load_dotenv(path) 
    try : 
        yield 
    finally : 
        for api_key in api_keys_list : 
            os.environ.pop(api_key,None)

from typing import List, Dict, Tuple
import csv

class Data : 
    def __init__(self,columns:List[str],data:List[Dict]) : 
        self.columns = columns 
        self.data = data


class CSVHandler : 
    def __init__(self,file_name : str) : 
        self.file_name = file_name


    def set_data_and_cols(self,cols:List[Dict[str,str]],data:List[Dict]) : 
        self.data = data 
        self.cols = cols  
    
    def write_table_to_csv(self):
        keys = [col["key"] for col in self.cols]
        labels = [col["label"] for col in self.cols]
        widths = [col["widthWeight"] for col in self.cols]

        with open(self.file_name, mode="w", newline="", encoding="utf-8") as f:
            print("file opene correctlu for writing")
            writer = csv.writer(f)
            # Write metadata rows
            writer.writerow(labels)
            writer.writerow(keys)
            writer.writerow(widths)
            # Write data rows
            for row in self.data:
                writer.writerow([row.get(k, "") for k in keys])

    def load_table_from_csv(self):
    
        with open(self.file_name, mode="r", newline="", encoding="utf-8") as f:
            print("file opened correctly")
            reader = list(csv.reader(f))

        if len(reader) < 3:
            raise ValueError("CSV file format invalid. Missing header rows.")

        labels = reader[0]
        keys = reader[1]
        widths = reader[2]

        # Rebuild cols
        cols = [
            {"key": k, "label": l, "widthWeight": int(w)}
            for k, l, w in zip(keys, labels, widths)
        ]

        # Rebuild data
        data_rows = reader[3:]
        data = [dict(zip(keys, row)) for row in data_rows]

        return cols, data

class DataLoader : 
    def __init__(self,csv_handler:CSVHandler,metrics:List[Dict]) : 
        self.csv_handler = csv_handler 
        self.cols, self.data = self.csv_handler.load_table_from_csv()
        self.metrics_cols = []
        self.metrics_row_values = []
        start_col_num_metrics = len(self.cols)
        for metric in metrics : 
            self.metrics_cols.append({
                    "key":"col"+str(start_col_num_metrics),
                    "label":metric["label"],
                    "widthWeight":metric["widthWeight"]
                    })
            start_col_num_metrics += 1 

        for data in self.data : 
            metrics_row_value = {}
            for metric in self.metrics_cols : 
                metrics_row_value[metric["key"]] = "" 
            self.metrics_row_values.append(metrics_row_value)
            
    def build_full_table(self) : 
        cols_res = []
        final_rows = []
        for col in self.cols : 
            cols_res.append(col) 
        
        for col in self.metrics_cols : 
            cols_res.append(col)

        for d1, d2 in zip(self.data, self.metrics_row_values):
            final_rows.append({**d1, **d2})  

        return cols_res, final_rows


    



    def create_csv_in_tests(filename):

    tests_dir = os.path.join(os.getcwd(), "tests")
    os.makedirs(tests_dir, exist_ok=True)
    file_path = os.path.join(tests_dir, filename)
    return file_path


if __name__ == "__main__" : 
    cols =  [{"key":"col1","label":"User query","widthWeight":1},{"key":"col2","label":"Ground truth","widthWeight":1}] 
    query_ref_pais = [
        {"col1":"""Why does salt melt ice on the road during winter?""","col2":"""Salt lowers the freezing point of water, a process known as freezing point depression. When salt is added to ice, it dissolves into the thin layer of liquid water always present on the ice surface, forming a brine with a lower freezing point than pure water. As a result, the ice melts even though the temperature is below 0°C."""} ,
        {"col1":"""What is wrong with this Python code and how can I fix it?

my_list = [1, 2, 3]
print(my_list[3]) ""","col2":"""The code raises an IndexError because list indices in Python start at 0, so my_list[3] is out of range. The valid indices are 0, 1, 2.
✅ Fix:

print(my_list[2])


or

for item in my_list:
    print(item)""",
        },
        {"col1" :  """Summarize this text in one sentence:
“Artificial intelligence refers to systems that can perform tasks that typically require human intelligence, such as understanding language, recognizing patterns, solving problems, and learning from experience.” """,
    "col2":"""Artificial intelligence is the development of systems capable of performing human-like cognitive tasks such as learning, problem-solving, and language understanding."""},
        {"col1":"""Explain the difference between supervised and unsupervised learning in machine learning. """, 
    "col2":"""In supervised learning, models are trained on labeled data — each input has a known output (e.g., classifying emails as spam or not spam).
In unsupervised learning, models are trained on unlabeled data and must discover hidden structures or patterns by themselves (e.g., clustering customers by purchasing behavior). """}, 
        {"col1":"""Write a short motivational quote about learning to code.""",
    "col2":"""Every bug you fix is a lesson learned; every line of code is a step toward mastery."""}
    ]
    data = Data(columns=cols,data=query_ref_pais)
    metrics = ["output","relevance"] 

    data_loader = DataLoader(data=data,metrics=metrics)
    print("columns : ") 
    print(data_loader.columns)
    print("first row")

    csv_handler = CSVHandler("csv_test.csv") 
    csv_handler.set_data_and_cols(cols,query_ref_pais)
    csv_handler.write_table_to_csv()
    cols, data = csv_handler.load_table_from_csv() 
    print("##### \n##### \n######")
    print("printing cols" )
    for col in cols : 
        print(col) 

    print("##### \n##### \n######")
    print("printing rows" ) 
    for row in data : 
        print(row)


    
