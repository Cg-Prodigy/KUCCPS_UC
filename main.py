from pprint import pprint
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


options=Options()
options.add_argument("--headless")
client=Chrome()
client.get(url="https://students.kuccps.net/institutions/")
University_data=[]
while True:
    start=2
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
        University_data.append(data_dict)
    pagination=client.find_elements(By.CSS_SELECTOR,"ul.pagination li")
    for i in range(len(pagination)):
        if i==start:
            initial_class="paginate_button"
            new_class="paginate_button active"
            client.execute_script("arguments[0].setAttribute('class',arguments[1])",pagination[i-1],initial_class)
            client.execute_script("arguments[0].setAttribute('class',arguments[1])",pagination[i],new_class)
            start+=1
        break
    if start==17:
        break
