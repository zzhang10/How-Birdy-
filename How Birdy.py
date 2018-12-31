#========================================================================================#
#                                                                                        #
#                              HOW BIRDY: A COURSE SCRAPER                               #
#                                                                                        #
#                                     BY ZACK ZHANG                                      #
#                                                                                        #
#========================================================================================#


#The APIs you need:
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import time
import requests
import random
import decimal

#A list of all the course title
abbr_list=["AFM","ACTSC","ASL","ANTH","AHS","APPLS","AMATH","ARCH","AE","ARTS","ARBUS","AVIA",
           "BASE","BIOL","BME","BUS","BET","CDNST","CHE","CHEM ","CHINA","CMW","CIVE","CLAS",
           "COGSCI","CO","COMM","SCCOM","CS","COOP","CROAT","CI","DAC","DRAMA","DUTCH","EARTH",
           "EASIA","ECON","ECE","ENGL","EFAS","EMLS","ENBUS","ERS","ENVE","ENVS","FINE","FR",
           "GENE","GEOG","GEOE","GER","GERON","GBDA","GRK","HLTH","HIST","HRM","HUMSC","HUMSC",
           "INDEV" ,"INTST","ITAL","ITALST","JAPAN","JS","KIN","INTEG","KOREA","LAT","LS",
           "MATBUS","MGMT","MSCI","MNS","MATH","MATH","ME","MTE","MEDVL","MUSIC","NE","OPTOM",
           "PACS","PACS","PACS","PHYS","PLAN","PSCI","PORT","PD","PDARCH","PDPHRM ","PSYCH",
           "PMATH","REC","RS","RUSS","REES","SCI","SCBUS","SMF","SDS","SVENT","SOCWK","SWREN",
           "STV","SOC","SE","SPAN","SPCOM","STAT","SI","SYDE","UNIV","VCULT","WS","WKRPT"]

course_info_combined=[]
abbr_list_2=[]

#The first section of the URL for the course pages; searching this section only will not
#  lead to a valid page
base_url="""http://www.ucalendar.uwaterloo.ca/1920/COURSE/course-"""

#Parses the HTML code scraped from the pages to find the course codes:
max_page=len(abbr_list)
for page in range(0,max_page):
    subject_courses_list=[]
    course_desc_list=[]
    course_abbr_list=[]
    course_component_list=[]
    course_credit_list=[]
    url=requests.get(base_url+abbr_list[page]+".html#"+abbr_list[page])
    html_code=url.content
    reduced_html_code=BeautifulSoup(html_code,"html.parser")
    subject_courses=reduced_html_code.find_all("b")[1:]
    #Filters out some non-course-codes
    for item in subject_courses:
        if str(item).lower() in ["<b>only offered online</b>",\
                                 "<b>also offered online</b>","<b>note</b>","<b>notes:</b>"]:
            pass
        else:
            subject_courses_list.append(str(item)[3:-4])
    for item in subject_courses_list:
        
        if item[0]!="<":
            course_desc_list.append(item)

        else:
            point1=item.find("a>")
            point2=item.find(" ")
            point3=item.find(" ",point2+1)
            point4=item.find(" ",point3+1)
            coursename_spaceless=str(item).lower()[point1+2:point3]+str(item).lower()[point3+1:point4]
            course_abbr_list.append(str(item)[point1+2:point4])
            abbr_list_2.append(coursename_spaceless)
            course_component_list.append(str(item)[point4+1:-5])
            course_credit_list.append(str(item)[-4:])
    #Sets up the dataframe column titles:    
    for desc,abbr,component,weight in zip(course_abbr_list,course_desc_list,\
                                          course_component_list,course_credit_list):
        temp_lib={}
        temp_lib["Course Code"]=abbr
        temp_lib["Title"]=desc
        temp_lib["Components"]=component
        temp_lib["Credit Amount"]=weight
        temp_lib["Usefulness"]="Unavailable"
        temp_lib["Difficulty"]="Unavailable"
        course_info_combined.append(temp_lib)
    #Pseudo-progress bar:   
    print ("""














































""")
    print("Please wait while your data is being collected")
    print ("Data collection progress:"+page*"█"+(max_page-page-1)*\
           "⌷"+" "+str(int(1000*page/(max_page-1))/10)+"%")
chart2.to_csv("Course Info Final.csv")


#Due to UWFlow having dynamic rating bars, each website is opened for the data to load before scraping happens
def get_info (page):
    driver = webdriver.Chrome()  
    driver.get(base_url_2+abbr_list_2[page])
    time.sleep(2)
    try:
        reduced_html_code_2=BeautifulSoup(driver.page_source,features="html5lib")
        usefulness=reduced_html_code_2.find_all("div",{"class":"rating-bar bar active positive bar-success"})[0]
        easiness=reduced_html_code_2.find_all("div",{"class":"rating-bar bar active positive bar-success"})[1]
        usefulness_input=float(str(usefulness)[70:-12])
        easiness_input=str(easiness)[70:-12]
        difficulty=float(str(100-float(easiness_input))[:5])
        course_info_combined[page]["Usefulness"]=usefulness_input
        course_info_combined[page]["Difficulty"]=difficulty
    #Some courses do not exist in UWflow, so the data is labeled "unavailable".    
    except:
        course_info_combined[page]["Usefulness"]="Unavailable"
        course_info_combined[page]["Difficulty"]="Unavailable"
    driver.close()

base_url_2="https://uwflow.com/course/"
max_page_2=len(abbr_list_2)
coursecounter=0
for page in range(0,max_page_2):
    #Backs up data in a CSV file once every 50 pages scraped, to prevent loss of data due to interruptions
    if coursecounter>=49:
        chart=pandas.DataFrame(course_info_combined)
        try:
            chart.to_csv("Course Info Up To {}.csv".format(page))
            print("Data collection and storage {} complete!".format(page))
        except:
            print("Data cannot be stored at this moment.")
            print("""Please ensure you do not have a file saved already under the name "Course Info".""")
        coursecounter=0
    else:
        coursecounter+=1                
        get_info(page)

print("done")


chart2=pandas.DataFrame(course_info_combined)
try:
    chart2.to_csv("Course Info Final.csv")
    print("Data collection and storage complete!")
    
#Prevents overriding of previously scraped data
except:
    print("Data cannot be stored at this moment.")
    print("""Please ensure you do not have a file saved already under the name "Course Info".""")
    

