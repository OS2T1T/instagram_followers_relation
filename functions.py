from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import *
import time
import sqlite3
import sys

def getArgs(argv):
	argv = argv[:]
	# Remove program name
	argv.pop(0)
	# Make args
	args = {}
	args["accounts"] = argv[:]
	return args

def getLogins():
	logins = {}
	# Get logins
	with open("logins", 'r') as loginsFile:
	    logins["username"] = loginsFile.readline().split(" = ")[1].replace('\n', '')
	    logins["password"] = loginsFile.readline().split(" = ")[1].replace('\n', '')
	return logins

def loadPage(driver, url, ACTION_DELAY):
	driver.get(url)
	time.sleep(ACTION_DELAY)

def instagramLogin(driver, logins, ACTION_DELAY):
	# Autorize cookies
	allowButton = driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
	allowButton.click()

	# Input logins
	usernameInput = driver.find_element(By.XPATH, "//*[@id=\"loginForm\"]/div/div[1]/div/label/input")
	passwordInput = driver.find_element(By.XPATH, "//*[@id=\"loginForm\"]/div/div[2]/div/label/input")

	usernameInput.send_keys(logins["username"])
	passwordInput.send_keys(logins["password"])
	passwordInput.send_keys(Keys.ENTER)

	time.sleep(ACTION_DELAY)