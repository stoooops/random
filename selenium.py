#!/usr/bin/env python3

from selenium import webdriver

# Create a webdriver object
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://example.com")

# Keep the webdriver open so you can interact with the website in your browser
input("Press Enter to close the webdriver.")

# Close the webdriver
driver.close()
