from bs4 import BeautifulSoup
import re 



class Logger : 
    def __init__(self,log_file_path:str)  : 
        self.logging_contents = [] 
        self.log_file_path = log_file_path 
        print("build logger correctly !!!!")


    def warning(self,message:str,no_display:bool=False) : 
        self.logging_contents.append(["warning",message,no_display]) 
    def info(self,message:str,no_display:bool=False) :
        self.logging_contents.append(["info",message,no_display]) 
    def error(self,message:str,no_display:bool=False) : 
        self.logging_contents.append(["error",message,no_display]) 
    def build_logging_page(self) : 
        with open(self.log_file_path,"w") as file : 
            for logging_content in self.logging_contents :
                content = f"{logging_content[0]} : {logging_content[1]}" + "\n"
                file.write(content)


    def build_logging_html(self) : 
        with open("src\\frontend\\logger_tst.html","r",encoding="utf-8") as f : 
            print("opened the html file correctly ")
            soup = BeautifulSoup(f,"html.parser")  

        target_div = soup.find("div",class_="collapsible-outer-container") 
        if  target_div : 
            target_div.clear()
            test_num = 0
            for logging_content in self.logging_contents : 
                 
                test_num+=1
                logging_content_paragraph = logging_content[1].replace("\n","<br>")
                

                if  logging_content[2] : 
                    background = ""
                    if logging_content[0] == "warning" : 
                        background = "warning" 
                    elif logging_content[0] == "error" : 
                        background = "error"
                    div_to_add =f""" 
<div class="collapsible-container {background}">
    <div class="collapsible-header" tabindex="0">
        <span class="arrow">&#9654;</span>
        Show Details  
    </div>
    <div class="collapsible-content {background}">
    {logging_content_paragraph}
    </div>
</div>"""
                else : 
                    background = ""
                    if logging_content[0] == "warning" : 
                            background = "warning-message" 
                    elif logging_content[0] == "error" : 
                        background = "error-message"
                    else : 
                        background = "info-message" 
                    div_to_add = f"""<div class="{background}">
{logging_content_paragraph}
    </div>"""
                target_div.append(BeautifulSoup(div_to_add,"html.parser")) 

        else : 
            print("element not found ")

        with open("src\\frontend\\logger_tst.html","w",encoding="utf-8") as f :
            f.write(str(soup))





if __name__ == "__main__" : 
    logger = Logger("tst.pdf")  
    logger.build_logging_html()