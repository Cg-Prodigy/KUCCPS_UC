from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from pprint import pprint
import time
options=Options()
options.add_argument("--headless")
client=Chrome()
client.get(url="https://students.kuccps.net/institutions/")
university_data={}
while True:
    last_inst=None
    soup=BeautifulSoup(client.page_source,"html.parser")
    root=soup.find("div",id="page-wrapper").find("div",class_="white-box").find("table",class_="table table-hover table-condensed small dataTable no-footer")
    t_head=root.find("thead").find_all("th")
    colum_heads=[i.text for i in t_head][1:]
    t_body=root.find("tbody").find_all("tr")
    client_two=Chrome(options=options)
    for row in t_body:
        href=row["data-href"]
        data=[r.text for r in row.find_all("td")][1:]
        client_two.get(url="https://students.kuccps.net"+href)
        soup_two=BeautifulSoup(client_two.page_source,"html.parser")
        data_dict={key:value for key,value in zip(colum_heads,data)}
        try:
            root_two=soup_two.find("div",class_="white-box").find("div",class_="table-responsive").find("table",class_="table table-hover table-responsive table-bordered small")
            t_head_two=str([th.text for th in root_two.find("thead").find("tr").find_all("th")][2])
            t_body_two=root_two.find("tbody").find_all("tr")
            course_list=[]
            for each in t_body_two:
                data_two=each.find_all("td")[2]
                course=str(data_two.text).strip().title()
                course_list.append(course)
            data_dict["Courses"]=course_list
        except:
            data_dict["Courses"]=["None declared"]
        inst_name=data_dict["Name"]
        last_inst=inst_name
        data_dict.pop("Name")
        university_data[inst_name]=data_dict
        print(inst_name)
    count=0
    try:
        li_active=client.find_element(By.CSS_SELECTOR,"ul.pagination li.paginate_button.active")
        next_li=li_active.find_element(By.XPATH,"./following-sibling::li[1]")
        a=next_li.find_element(By.TAG_NAME,"a")
        a.click()
        time.sleep(3)
    except Exception as e:
        pass
    if inst_name=="ZIWA TECHNICAL TRAINING INSTITUTE":
        break

uni={}
colle={}
for inst in university_data:
    if university_data[inst]["Category"]=="University":
        uni[inst]=university_data[inst]
    else:
        colle[inst]=university_data[inst]

# write data to file
with open("universities.json","w") as file:
    json.dump(uni,file)
with open("colleges.json","w") as file:
    json.dump(colle,file)