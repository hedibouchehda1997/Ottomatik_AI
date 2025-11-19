from typing import Dict
from pymongo import MongoClient, errors 
import uuid 



class MongoDBInteractor : 
    def __init__(self,db_url,serverSelectionTimeoutMS=5000) : 
        try : 
            self.data_base_client = MongoClient(db_url,serverSelectionTimeoutMS=serverSelectionTimeoutMS)  
            self.data_base_client.admin.command('ping') 
            self.data_base = self.data_base_client["Agents"]
            self.agents_collection = self.data_base["agents"]
            self.history_collection = self.data_base["history"]
        
        except errors.ServerSelectionTimeoutError as err : 
            raise ValueError("could not connect to MongoDB: ",err) 

    

    def add_agent(self,agent_details:Dict) :  
        agent_elem_db = agent_details
        hist_elem_db = {
            "id_" : agent_details["id_"] , 
            "version" : agent_details["version"], 
            "history" : [],
        }
        self.agents_collection.insert_one(agent_elem_db)
        self.history_collection.insert_one(hist_elem_db)
        print("agent added successfuly to collection !!")

    def find_all_agents(self,user_id='') : 
        agent_collection = list(self.agents_collection.find({},{"_id":0}))
        return agent_collection

    def get_memory(self,id_:str) :  
        history_obj = list(self.history_collection.find({"id_":id_},{"_id":0}))
        return history_obj[0]


    def add_message(self,id_:str ,type_:str, msg :str) : 
        self.history_collection.update_one(
            {"id_":id_} , 
            {"$push" : {"history" : {type_ : msg}}}
        )

        

        