# How Birdy?

### What do you mean, how birdy?
A bird course is a course that is not very difficult, or does not take a lot of effort to get a high mark. This piece of code evaluates how birdy a course is at my university, the University of Waterloo. The previous students have set up a website called UWFlow, on which students can vote for the difficulty and usefulness of the courses they have taken. The code draws from UWFlow when evaluating the courses' difficulty.


### The code seems like it takes a long time to run...
Unfortunately, yes. Due to UWFlow having dynamic components, the program must open each page with a webdriver to load the data before scraping it. That means it takes approximately 4-5 seconds for the data of each subject to be scraped. To prevent data loss due to battery dying, overheating, or your cat jumping onto the power button, the program saves a file every 50 courses scraped. 

If you find your program terminating unexpectedly, you can change line 160:
```python
for page in range(0,max_page_2):
```
into 
```python
for page in range(<THE PAGE YOU ENDED WITH>,max_page_2):
```
If you would like to back up more often, you can change the integer in line 162:
```python
if coursecounter>=49:
```
into a smaller positive integer.

### What if the courses change?
The courses may change from year to year. For future academic years, you may change the number in line 36:
```python
base_url="""http://www.ucalendar.uwaterloo.ca/1920/COURSE/course-"""
```
into the corresponding academic year. For example, 1920 means the scraper is collecting data from the 2019-20 school year. Next year you may want to replace it with 2021.

#### Note: the program uses the APIs Selenium Webdriver (Chrome), Pandas, and BeautifulSoup4. Make sure you have these installed.
