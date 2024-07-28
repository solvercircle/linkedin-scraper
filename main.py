from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json, os, sys
from selenium.webdriver.chrome.options import Options
import argparse

def saveCookies(drv):
	# Get and store cookies after login
	cookies = drv.get_cookies()

	# Store cookies in a file
	with open('cookies.json', 'w') as file:
		json.dump(cookies, file)
	print('New Cookies saved successfully')


def loadCookies():
	# Check if cookies file exists
	if 'cookies.json' in os.listdir():

		# Load cookies to a vaiable from a file
		with open('cookies.json', 'r') as file:
			cookies = json.load(file)

		# Set stored cookies to maintain the session
		for cookie in cookies:
			driver.add_cookie(cookie)
	else:
		print('No cookies file found')

	driver.refresh()  # Refresh Browser after login

def login():
	# Opening linkedIn's login page
	driver.get("https://linkedin.com/uas/login")
	loadCookies()

	# waiting for the page to load
	time.sleep(5)
	if 'login' in driver.current_url:
		if manual_login:
			print('Please Login the the website')
			print('Press Enter after successful login ...')
			input('>: ')

			# After successful login save new session cookies ot json file
			saveCookies(driver)
		else:
			# entering username
			username = driver.find_element(By.ID, "username")

			# In case of an error, try changing the element
			# tag used here.

			# Enter Your Email Address
			username.send_keys(li_email)

			# entering password
			pword = driver.find_element(By.ID, "password")
			# In case of an error, try changing the element
			# tag used here.

			# Enter Your Password
			pword.send_keys(li_password)

			# Clicking on the log in button
			# Format (syntax) of writing XPath -->
			# //tagname[@attribute='value']
			driver.find_element(By.XPATH, "//button[@type='submit']").click()
			time.sleep(300)

			saveCookies(driver)
	else:
		print("Previous session loaded.")

def getProfileName():
	# Extracting the HTML of the complete introduction box
	# that contains the name, company name, and the location
	# intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
	# intro = soup.find('h1', {'class': 'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0'})
	intro = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})

	print(intro.get_text().strip())


def sendConnection():
	#Start: Send Connction
	sent_connect = False
	#driver.find_element(By.CSS_SELECTOR, ".contextual-sign-in-modal__outlet-btn.cursor-pointer.btn-md.btn-primary.top-card-layout__cta.btn-secondary-emphasis").click()
	#driver.find_element(By.CSS_SELECTOR, 'a[href*="https://www.linkedin.com/company/"][data-tracking-control-name="public_profile_topcard-current-company"]').click()
	try:
		elm_conn_btn = driver.find_element(By.CSS_SELECTOR, '.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.pvs-profile-actions__action')
		elm_conn_btn_text = elm_conn_btn.find_element(By.CSS_SELECTOR, 'span.artdeco-button__text')
		if elm_conn_btn_text.text == 'Connect':
			elm_conn_btn.click()
			time.sleep(3)
			driver.find_element(By.CSS_SELECTOR, '.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1').click()

			sent_connect = True
	except Exception as exp:
		print("#1 No connect button")
		print(exp)

	if not sent_connect:
		try:
			elm_more_btn_text = driver.find_element(By.CSS_SELECTOR, 'section.artdeco-card .artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view.pvs-profile-actions__action.artdeco-button.artdeco-button--secondary.artdeco-button--muted.artdeco-button--2 > span')
			print(elm_more_btn_text.text)
			if elm_more_btn_text.text == 'More':
				driver.find_element(By.CSS_SELECTOR, 'section.artdeco-card .artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view.pvs-profile-actions__action.artdeco-button.artdeco-button--secondary.artdeco-button--muted.artdeco-button--2').click()
				time.sleep(10)

				#elm_menu_connect_text_list = driver.find_element(By.CSS_SELECTOR, 'section.artdeco-card .artdeco-dropdown__item.artdeco-dropdown__item--is-dropdown.ember-view.full-width.display-flex.align-items-center > span.display-flex')
				elm_menu_connect_list = driver.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__content.artdeco-dropdown__content--is-open.artdeco-dropdown--is-dropdown-element.artdeco-dropdown__content--justification-left.artdeco-dropdown__content--placement-bottom.ember-view > div.artdeco-dropdown__content-inner > ul > li')
				for elm_menu_connect in elm_menu_connect_list:
					elm_menu_connect_text = elm_menu_connect.find_element(By.CSS_SELECTOR, 'span.display-flex')
					print(elm_menu_connect_text.text)
					if elm_menu_connect_text.text == 'Connect':
						#driver.find_element(By.CSS_SELECTOR, '.artdeco-dropdown__item.artdeco-dropdown__item--is-dropdown.ember-view.full-width.display-flex.align-items-center').click()
						elm_menu_connect.click()
						time.sleep(3)
						driver.find_element(By.CSS_SELECTOR, '.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml1').click()
						break

			time.sleep(10)
			sent_connect = True
		except Exception as exp:
			print("#2 No connect button")
			print(exp)

	time.sleep(3)

	#End: Send Connction

def sendMessage(msg_body, msg_subject=''):
	#Click on Message Button
	driver.find_element(By.CSS_SELECTOR, 'div.entry-point.profile-action-compose-option .artdeco-button.artdeco-button--2.ember-view.pvs-profile-actions__action').click()
	time.sleep(5)


	#Send Message

	#Put message subject and body in the inputs
	#msg_subject = "Tour"
	#msg_body = "Are you interested?"

	try:
		elm_subject = driver.find_element(By.NAME, 'subject')
		#print(elm_subject)
		if elm_subject is not None:
			elm_subject.send_keys(msg_subject)
	except:
		print("No subject element exist")


	elm_body = driver.find_element(By.CSS_SELECTOR, '.msg-form__contenteditable > p')
	elm_body.send_keys(msg_body)
	time.sleep(5)

	#Click on Send Button
	driver.find_element(By.CSS_SELECTOR, '.msg-form__send-button.artdeco-button.artdeco-button--1').click()
	time.sleep(30)




def doEndorse():
	#Start: Endorse
	skills_url = profile_url + "details/skills/"
	driver.get(skills_url)  # this will open the link
	src_skills = driver.page_source
	soup_skills = BeautifulSoup(src_skills, 'lxml')

	elm_endorse_list = driver.find_elements(By.CSS_SELECTOR, 'li[id*="profilePagedListComponent-"] .artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view')
	for elm_endorse in elm_endorse_list:
		print(elm_endorse)

		#elm_endorse_text = elm_endorse.find("span", {'class': 'artdeco-button__text'})
		elm_endorse_text = elm_endorse.find_element(By.CSS_SELECTOR, 'span.artdeco-button__text')
		print(elm_endorse_text.text)

		if elm_endorse_text.text.strip() == "Endorse":
			elm_endorse.click()
			break

	time.sleep(30)







#-----------------------------------------Start: Main---------------------------
parser = argparse.ArgumentParser(description='Scrap LinkeIn')
parser.add_argument('--is_manual_login',default="0")
parser.add_argument('--linkedin_email',required=True)
parser.add_argument('--linkedin_password',required=True)
parser.add_argument('--linkedin_profile_to_scrap',required=True)
parser.add_argument('--operation',required=True)
parser.add_argument('--message',default="Hello, Hope you are doing great.")




args = parser.parse_args()
#print(args.is_manual_login)
#print(args.linkedin_email)
#exit()

cmd_manaual_login = args.is_manual_login
cmd_email = args.linkedin_email
cmd_password = args.linkedin_password
cmd_profile_url = args.linkedin_profile_to_scrap
cmd_op = args.operation
cmd_msg = args.message

manual_login = False
if cmd_manaual_login == "1":
    manual_login = True

li_email = cmd_email 
li_password = cmd_password


#options = Options()
#options.add_argument('--profile-directory=Profile 1')
#options.add_argument("user-data-dir=C:\\Users\\Ahsan\\AppData\\Local\\Google\\Chrome\\User Data\\") #Path to your chrome profile
# Creating a webdriver instance
driver = webdriver.Chrome()


# Open Chrome Browser
#driverPath = ChromeDriverManager().install()
#driver = webdriver.Chrome(executable_path=driverPath)
login()
time.sleep(5)






# In case of an error, try changing the
# XPath used here.




profile_url = cmd_profile_url

driver.get(profile_url)  # this will open the link

time.sleep(5)


src = driver.page_source

# Now using beautiful soup

soup = BeautifulSoup(src, 'lxml')
#soup = BeautifulSoup(src, features="html.parser")

getProfileName()

if cmd_op == 'connect':
    sendConnection()
if cmd_op == 'message':
    sendMessage(cmd_msg)
if cmd_op == 'endorse':
    doEndorse()





#-----------------------------------------End: Main---------------------------

exit()



#----------------------------------------------END----------------------------------

