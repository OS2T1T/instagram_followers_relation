from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import *
import sqlite3
import time
import sys

import json

# Driver for web scrapping
driver = webdriver.Chrome(executable_path="./chromedriver")

# Database for data retrieving
connexion = sqlite3.connect(":memory:")
connexion.row_factory = sqlite3.Row
cursor = connexion.cursor()

# Create table
cursor.execute('''
	CREATE TABLE users (
		[user_id] INTEGER PRIMARY KEY, [username] CHAR(20), [related] INTEGER, [relation_score] DECIMAL(10, 9)
	)
	''')
connexion.commit()

# Command data
args = getArgs(sys.argv)
logins = getLogins()

loadPage(driver, "https://www.instagram.com/", 3)
instagramLogin(driver, logins, 5)

for account in args["accounts"]:
	url = "https://www.instagram.com/" + account
	loadPage(driver, url, 3)

	# Followers
	followersButton = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span')
	followersButton.click()

	time.sleep(3)

	container = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[2]")

	for i in range(2):
		oldScrollHeight = 0
		newScrollHeight = container.get_attribute("scrollHeight")
		while newScrollHeight != oldScrollHeight:
			driver.execute_script("arguments[0].scrollBy(0, 1000)", container)
			time.sleep(2)
			oldScrollHeight = newScrollHeight
			newScrollHeight = container.get_attribute("scrollHeight")

		related = driver.find_elements(By.CSS_SELECTOR, "._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll")
		
		# Put related in database
		for rel in related:
			username = rel.get_attribute("innerText")
			
			# Increment related number if existing
			nb_related = 1
			cursor.execute("SELECT related FROM users WHERE username = ?", (username,))
			result = cursor.fetchall()
			if len(result) != 0:
				nb_related = result[0]["related"] + 1
				relation_score = nb_related / (2 * len(args["accounts"]))
				cursor.execute("UPDATE users SET related = ? WHERE username = ?", (nb_related, username))
				cursor.execute("UPDATE users SET relation_score = ? WHERE username = ?", (relation_score, username))
			else:
				relation_score = nb_related / (2 * len(args["accounts"]))
				cursor.execute("INSERT INTO users (username, related, relation_score) VALUES (?, ?, ?)", (username, nb_related, relation_score))
			connexion.commit()

		closeButton = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[1]/div/div[3]/div/button")
		closeButton.click()

		# Subscribers
		followersButton = driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div')
		followersButton.click()

		container = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div/div[3]")

cursor.execute("SELECT * FROM users ORDER BY relation_score DESC LIMIT 20")
data = cursor.fetchall()
for user in data:
	print(user["username"], user["relation_score"])