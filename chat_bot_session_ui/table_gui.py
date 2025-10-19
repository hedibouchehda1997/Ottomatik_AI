import streamlit as st
from streamlit.delta_generator import DeltaGenerator

# Update CSS for table (fix table width to container, not page/body!)
st.markdown("""
    <style>
    /* Don't make page wider than Streamlit container */
    .block-container, .stMarkdown > div, .stMarkdown {
        width: 100% !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    /* MAIN FIX: the table should fill the parent container (the column), not the page! */
    .modern-table {
        width: 100% !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 1.5rem;
        background: #fff;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(60,60,60,0.08);
        overflow: hidden;
        font-family: 'Segoe UI', Arial, sans-serif;
        table-layout: fixed;
    }
    .modern-table th, .modern-table td {
        padding: 0.75rem 1.25rem;
        border: none;
        text-align: left;
        background: #fff;
        min-width: 80px;
        transition: background 0.2s, box-shadow 0.2s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    .modern-table thead th {
        background: #f8f9fa;
        color: #222;
        font-weight: 600;
        font-size: 1.05em;
        cursor: pointer;
    }
    .modern-table tbody tr {
        transition: background 0.2s;
    }
    .modern-table tbody tr:nth-child(even) {
        background: #f4f7fa;
    }
    .modern-table td {
        font-size: 1.05em;
        color: #333;
    }
    /* Interactive hover effect for cells */
    .modern-table td:hover {
        background: #ffefc0 !important;
        box-shadow: 0 0 0 2px #ffd24d;
        z-index: 2;
        transition: background 0.18s, box-shadow 0.2s;
    }
    .modern-table th:hover {
        background: #ececec !important;
        color: #0067ff !important;
    }
    </style>
""", unsafe_allow_html=True)

from typing import List, Dict, Tuple

class Data : 
    def __init__(self,columns:List[str],data:List[Dict]) : 
        self.columns = columns 
        self.data = data

class DataLoader : 
    def __init__(self,data:Data,metrics:List[str]) : 
        self.columns = []
        self.data = data.data
        self.num_cols = 0
        for i in range(len(data.columns)) : 
            self.num_cols += 1
            self.columns.append(("col"+str(self.num_cols),data.columns[i]))

        for metric in metrics : 
            if metric == "output" : 
                self.num_cols += 1 
                self.columns.append(("col"+str(self.num_cols),"Output")) 
            elif metric == "relevance" : 
                self.num_cols += 1 
                self.columns.append(("col"+str(self.num_cols),"Relevance"))
    
        for row in self.data : 
            for i in range(len(self.columns)) : 
                if i >= len(list(row.keys())) : 
                    row["col"+str(i+1)] = "" 

class TestTable : 
    def __init__(self,table_name:str,data_loader:DataLoader,container:DeltaGenerator) : 
        self.table_name = table_name 
        self.data_loader = data_loader
        self.container = container
        self.header = "".join(f"<th>{col[1].capitalize()}</th>" for col in self.data_loader.columns) 
        self.col_widths = None  # To be set by set_column_widths

    def set_column_widths(self, widths: List[int]):
        """
        Set the relative width (as int, not px/percent directly) for each column.
        Example: [1, 2, 1] means second column is twice as wide as others.
        """
        if widths and len(widths) == len(self.data_loader.columns):
            self.col_widths = widths
        else:
            self.col_widths = None  # Disable custom widths if invalid

    def _colgroup_html(self):
        """
        Build a <colgroup> HTML defining each column's width, if self.col_widths set.
        Uses percent widths; sum(widths) == 100%.
        """
        if not self.col_widths:
            return ""
        total = sum(self.col_widths)
        col_tags = []
        for w in self.col_widths:
            pct = 100 * w / total
            col_tags.append(f'<col style="width:{pct:.2f}%;">')
        return "<colgroup>" + "".join(col_tags) + "</colgroup>"

    def render_table(self) : 
        rows = ""
        for row in self.data_loader.data:
            row_html = ""
            for col in self.data_loader.columns:
                value = row[col[0]]
                row_html += f"<td>{value}</td>"
            rows += f"<tr>{row_html}</tr>"
        colgroup_html = self._colgroup_html()
        table_html = f"""
            <table class="modern-table">
                {colgroup_html}
                <thead><tr>{self.header}</tr></thead>
                <tbody>{rows}</tbody>
            </table>
        """
        with self.container :
            st.title(self.table_name) 
            # Use an extra div with style to confine table to the column's width
            st.markdown(
                f'<div style="width:100%;overflow-x:auto;">{table_html}</div>',
                unsafe_allow_html=True
            )

if __name__ == "__main__" : 
    cols =  ["User query","Ground truth"] 
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

    col1, col2 = st.columns([2,1])
    with col1 : 
        test_table = TestTable(table_name="Test table",
                            data_loader=data_loader,
                            container=col1)

        num_cols = len(data_loader.columns)
        if num_cols == 4:
            widths = [4,,2,1]
        else:
            # Fallback for other column counts: default to even
            widths = [1]*num_cols
        test_table.set_column_widths(widths)
        test_table.render_table()
    with col2 : 
        st.subheader("Agent Configuration")



