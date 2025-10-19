from typing import List, Dict, Tuple
import json
import uuid  


class Data:
    def __init__(self, columns: List[str], data: List[Dict]):
        self.columns = columns
        self.data = data


class DataLoader:
    def __init__(self, data: Data, metrics: List[str]):
        self.columns = []
        self.data = data.data
        self.new_data = []
        self.num_cols = 0
        for i in range(len(data.columns)):
            self.num_cols += 1
            self.columns.append(("col" + str(self.num_cols), data.columns[i]))

        for metric in metrics:
            if metric == "output":
                self.num_cols += 1
                self.columns.append(("col" + str(self.num_cols), "Output"))
            elif metric == "relevance":
                self.num_cols += 1
                self.columns.append(("col" + str(self.num_cols), "Relevance"))

        for row in self.data:
            new_raw_with_metrics = {}
            for i in range(len(self.columns)):
                if i >= len(list(row.keys())):
                    new_raw_with_metrics["col" + str(i + 1)] = ""
            self.new_data.append(new_raw_with_metrics)


class LLMPipeline:
    def __init__(
        self,
        agent_details: Dict,
        agent_id: str,
        user_id: str = "user0",
        version: int = 0,
        agent_title: str = "Agent"
    ):
        self.user_id = user_id
        self.version = version
        self.agent_details = agent_details
        self.agent_id = agent_id
        self.agent_title = agent_title
        self.database_agents = None

    def compare_details(new_details, old_details):
        changes = {}
        for key, value in new_details.items():
            if key not in old_details or old_details[key] != value:
                changes[key] = value
        return changes

    def find_version_zero(array, user_id: str, agent_id: str):
        for item in array:
            if item.get('user_id') == user_id and item.get('agent_id') == agent_id and item.get('version') == 0:
                return item
        return None

    def check_if_agent_exsist(self, user_id: str, agent_id: str,version: str):
        try:
            with open("agents_database.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        for item in data:
            if item.get('user_id') == user_id and item.get('agent_id') == agent_id and item.get('version') == version:
                return True
        return False

    def save(self):
        # Read current agents from file
        try:
            with open("agents_database.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        if not data:
            data = []
        self.database_agents = data
        # Check if agent exists before saving
        if self.check_if_agent_exsist(self.user_id, self.agent_id,self.version):
            print("agent exisit")
            return
        new_agent = {}
        new_agent["user_id"] = self.user_id
        new_agent["agent_id"] = self.agent_id
        new_agent["version"] = self.version
        new_agent["agent_details"] = self.agent_details
        if self.version != 0:
            zero_version = self.find_version_zero(self.database_agents, self.user_id, self.agent_id)
            if zero_version:
                changes = self.compare_details()
                new_agent = {**new_agent, **changes}
        self.database_agents.append(new_agent)
        # Write entire agents array back to file in write mode
        with open("agents_database.json", "w") as f:
            print("new_agent")
            print(new_agent)
            json.dump(self.database_agents, f, indent=4)

    def build_agent(self)


class AgentLoader:
    def __init__(self, agent: LLMPipeline, data_loader: DataLoader):
        self.agent = agent
        self.data_loader = data_loader



if __name__ == "__main__":
    cols = ["User query", "Ground truth"]
    query_ref_pais = [
        {"col1": """Why does salt melt ice on the road during winter?""",
         "col2": """Salt lowers the freezing point of water, a process known as freezing point depression. When salt is added to ice, it dissolves into the thin layer of liquid water always present on the ice surface, forming a brine with a lower freezing point than pure water. As a result, the ice melts even though the temperature is below 0°C."""},
        {"col1": """What is wrong with this Python code and how can I fix it?

my_list = [1, 2, 3]
print(my_list[3]) """, "col2": """The code raises an IndexError because list indices in Python start at 0, so my_list[3] is out of range. The valid indices are 0, 1, 2.
✅ Fix:

print(my_list[2])


or

for item in my_list:
    print(item)""",
         },
        {"col1": """Summarize this text in one sentence:
“Artificial intelligence refers to systems that can perform tasks that typically require human intelligence, such as understanding language, recognizing patterns, solving problems, and learning from experience.” """,
         "col2": """Artificial intelligence is the development of systems capable of performing human-like cognitive tasks such as learning, problem-solving, and language understanding."""},
        {"col1": """Explain the difference between supervised and unsupervised learning in machine learning. """,
         "col2": """In supervised learning, models are trained on labeled data — each input has a known output (e.g., classifying emails as spam or not spam).
In unsupervised learning, models are trained on unlabeled data and must discover hidden structures or patterns by themselves (e.g., clustering customers by purchasing behavior). """},
        {"col1": """Write a short motivational quote about learning to code.""",
         "col2": """Every bug you fix is a lesson learned; every line of code is a step toward mastery."""}
    ]
    data = Data(columns=cols, data=query_ref_pais)
    metrics = ["output", "relevance"]

    data_loader = DataLoader(data=data, metrics=metrics)
    print("columns : ")
    print(data_loader.columns)
    print("first row")
    id1 = str(uuid.uuid4())
    id2 = uuid.uuid4().hex
    print("id1 : ", type(id1))
    print(id1)
    print("id2 : ", type(id2))
    print(id2)
    user_id = "d3ce86ed86474f1f934ce78f3986efbb"
    agent_id =  "92a3875011b246f697efafb3f733eaf9"
    agent_title = "React agent"
    version = 0
    agent_details = {
        "agent_type": "React",
        "model": "gpt-4",
        "system_prompt": "You are a helpful assitant ",
        "tools": ["tavily_search"]
    }

    llm_pipeline = LLMPipeline(
        user_id=user_id,
        agent_id=agent_id,
        version=version,
        agent_title=agent_title,
        agent_details=agent_details
    )

    llm_pipeline.save()


