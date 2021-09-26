# Helpful Links
# Interaction with Checkboxes:
#   https://www.toolsqa.com/selenium-webdriver/selenium-checkbox/
# Answer that solved the issue w/ searching for "col-btn.ng-isolate-scope.mc-select-container"
#   https://stackoverflow.com/questions/11223011/attributeerror-list-object-has-no-attribute-click-selenium-webdriver
# Answer that helped bypass chrome's "Connection unsafe, bpass
#   https://stackoverflow.com/questions/60247155/how-to-bypass-the-message-your-connection-is-not-private-on-non-secure-page-us
# Answer about selecting from lists <li ...>
#   https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
# Answer to switching to another window using Python/Selenium/ChromeWebDriver
#   https://stackoverflow.com/questions/26379560/get-focus-on-the-new-window-in-selenium-webdriver-and-python
# Answer to accessing dropdown option values from select in Selenium
#   https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
# Answer to how to put variable values into string using python:
#   https://pytutorial.com/python-variable-in-string
# If then statements:
#   https://basicpython.org/ifthen/
# numpy arrays
#   https://www.datacamp.com/community/tutorials/python-numpy-tutorial
# alert exception handling
#   https://stackoverflow.com/questions/25605018/object-is-not-callable-error-while-using-selenium-python
# check if alert
#   https://www.tutorialspoint.com/check-if-any-alert-exists-using-selenium-with-python


# Version 5.0 Notes:
# 1. Handled alerts
# 2. Added debug flag (debug mode does not confirm changes)
# 3. FIRST WORKING VERSION

# Goals for future:
# Secure encrypted login credentials locally--pull them--and then type them.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re  # may not be used??
from selenium.webdriver.support.ui import Select # may not be used??
import time
import numpy as np
from numpy import genfromtxt
import csv

# bypass the ssl warnings
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(options=options)

debugMode = True

print("3CX Selenium Automation Tool -- Reception BLF")

# old way to launch browser, replaced with way described above
# browser = webdriver.Chrome('chromedriver.exe')

browser.get('http://phones')

####################
# 1 - Login to 3CX #
####################

time.sleep(2)
# Find username and input
userName = browser.find_element_by_xpath("//input[@placeholder='User name or extension number']")
userName.send_keys('Your Admin Account Name Here')

# Find password and input
password = browser.find_element_by_xpath("//input[@placeholder='Password']")
password.send_keys('Your Admin Account Password Here')

# Find submit button and input
submit = browser.find_element_by_xpath('//button[text()="Login"]')
submit.click()

####################
# 2 - Go to phones #
####################

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "app-container"))
    )
finally:
    print('Debug: Successful AngularJS wait')

# Select the phones option from the left hand menu
extensions = browser.find_element_by_css_selector("a[ui-sref='app.phones']")
extensions.click()

#########################
# 3 - Search for "0000" #
#########################

# Find search bar and input
search = browser.find_element_by_xpath("//input[@placeholder='Search ...']")
search.click()
search.send_keys("0000")
time.sleep(3)  # sleep

#############################
# 4 - Click '0000' checkbox #
#############################

# Find extension result and click
# It's difficult to find out how to select a particular checkbox. Since there will be only one result.
# It is just as profitable to just do 'select all' checkbox and then PhoneUI
# attempt 0: result = browser.find_element_by_xpath("//*[contains(text(), '0000')]")
# we're trying to select the button that is within a td cell.
# attempt 1: result = browser.find_elements_by_class_name("td.col-btn.ng-isolate-scope.mc-select-container")
# That mc-select-container class is repeated with searches that yield more than one row, specified by Row ID
#   It might be good to learn how to select a class based on row id.. or something.. however that works.
#   I am guessing that with the plural version, it generates a list of all results and assigns them an index
#   You might be able to select by index as far as selenium is concerned in the case of redundant elements with same nms
#   TL;DR: read the docs on find_element_by_xpath vs find_elements_by_xpath


result = browser.find_element_by_class_name("col-btn.ng-isolate-scope.mc-select-container")
result.click()


#######################
# 5 - Choose Phone UI #
#######################

print("Debug: Accessing the User Interface for the receptionist phone...")


result = browser.find_element_by_id("btnPhoneUI")
result.click()
time.sleep(5)

###################################################################
# 6 - Choose Advanced -> Proceed to 10.2.1.31 (Unsafe) [Bypassed] #
###################################################################

# step no longer necessary b/c of options you can set in Chrome Web Driver for Python

#################################
# 7a - Change to New Tab/Window #
#################################


another_window = list(set(browser.window_handles) - {browser.current_window_handle})[0]
browser.switch_to.window(another_window);

print("Debug: Switched to new tab.")

print("Debug: Current URL: " + browser.current_url)

#######################
# 7b - Click 'Dsskey' #
#######################

# result = browser.find_element_by_xpath("//label[contains(.,'Dsskey')]")
# browser.moveToElement(result).click()
# ** after 70 minutes of troubleshooting. Running the 'browser.current_url' yielded the url of the first tab
#   which revealed to me, I have been searching the first tab for the dsskey string this whole time
#   which revealed to me why I couldn't find the dsskey string no matter what I did
#   this other solution of navigating to the direct url can work too, but I have to figure out how to change focus
#   of selenium to the new tab

# This command closes the tab being focused on. not a good fix because it still doesn't switch to new tab (selenium)
# browser.close()
# statusPageExtra = len("/servlet?m=mod_data&p=status&q=load")

result = browser.find_element_by_id("DSSKey").click()
print("Debug: Navigated to Dsskey tab")

#######################
# 8 - Click 'Ext Key' #
#######################

result = browser.find_element_by_id("dsskey-extkey").click()
print("Debug: Navigated to Dsskey tab")

#############################################
# 9 - Store Datas in a CSV that makes sense #
#############################################

#   Engineer a way to pull the data from a CSV and funnel it into the extension.

# Data stored in receptionBLF.csv
# csv format: [KEY], [TYPE], [VALUE], [LABEL], [LINE], [EXTENSION], [KEY]
# the rows are broken into the following extension columns:
# 000 - 039 | Extension 1
# 040 - 079 | Extension 2
# 080 - 119 | Extension 3
# 120 - 159 | Extension 4
# 160 - 199 | Extension 5


receptionBLF = list(csv.reader(open("receptionBLF.csv")))



###################################################
# 10a - Document how data is stored on the pages  #
###################################################
#   ON SELECTING PANELS
#       The web page has the expansion key as a dropdown w/ name "ExpansionKey"
#       There are four sub entries with the following option values
#           <option value="0">Expansion1</option>
#           <option value="1">Expansion2</option>
#           <option value="2">Expansion3</option>
#           <option value="3">Expansion4</option>
#           <option value="4">Expansion5</option>
#   ON SELECTING PANEL KEYS
#       The web page considers each extension key an item. Each item has an id associated with it that conforms to the
#       following naming scheme: "item_1", "item_2", and so on.
#   ON SELECTING PANEL KEY VALUES
#       The web page sorts the keys with ids unique to each PANEL KEY VALUE
#       The following naming scheme is used:
#       id(s): "type_1", "value_1", "label_1", "line_1", "extern_1"
#   ON SELECTING PANEL KEY VALUE: TYPE "type_#"
#       it's an option selection. The only options you care about are:
#           value="13" | this i the SpeedDial selection
#           value="16" | this is the BLF selection
#           value="40" | this is the prefix selection
#
#   ON SELECTING PANEL KEY VALUE: VALUE "value_#"
#       it's a text value
#
#   ON SELECTING PANEL KEY VALUE: LABEL "label_#"
#       it's a text value
#
#   ON SELECTING PANEL KEY VALUE: LINE "line_#"
#       Option selection, only option you are care is:
#           option value="0" | this is line1
#
#   ON SELECTING PANEL KEY VALUE: EXTENSION "extern_#"
#       This is a text input
#

############################################################################################################
# 10b - Write a loop that puts the data into the Extensions / Panels / Keys / Indexes and confirms changes #
############################################################################################################
# Pseudo Code
# 1. Begin loop until 5th iteration
#   a. Select desired Expansion Key
#   b. Wait until page loads (time or load check)
#   c. Select top left type
#       1. Begin Loop until 40th iteration
#           a. Supply Five bits of information
#           b. jump down to next column
#           c. +1
#       2. Confirm Changes
#       3. Wait five seconds (or until page reload)
#       4. +1

extensionPanelCounter = 0
extensionPanelKeyCounter = 0
extensionPanelKeyIndexCounter = 0
while extensionPanelCounter <= 4:
    print("Debug: Extension Panel Selection #" + str(extensionPanelCounter), "starting...")
    select = Select(browser.find_element_by_name("ExpansionKey"))
    # select by value
    print("Debug: Extension Panel Counter: ", extensionPanelCounter)
    select.select_by_value('%s' % str(extensionPanelCounter))

    if debugMode:
        try:
            WebDriverWait(browser, 5).until(EC.alert_is_present())
            alert = browser.switch_to.alert.accept()
        except TimeoutException:
            print("Debug: Alert does not exist in page.")

    time.sleep(2)
    print("Debug: Extension Panel #:", extensionPanelCounter, "selected.")

    # set receptionBLF to contain the specific Panel's information
    # rewrite: select values for rows by extension panel counter
    # You have to access rows:
    # You could access these rows via a multiplier
    # 00-39, 40-79, 80-119, 120-159, 160-199
    # For panel 0, index [n*40+extensionPanelCounter]

    # this used to reference the subsections.
    if extensionPanelCounter == 0:
        receptionBLF = receptionBLF
    elif extensionPanelCounter == 1:
        receptionBLF = receptionBLF
    elif extensionPanelCounter == 2:
        receptionBLF = receptionBLF
    elif extensionPanelCounter == 3:
        receptionBLF = receptionBLF
    elif extensionPanelCounter == 4:
        receptionBLF = receptionBLF

    while extensionPanelKeyCounter <= 39:
        print("Debug:   Extension Panel Key #:", extensionPanelKeyCounter, "selected.")
        print("Debug:       index #" + str(extensionPanelKeyIndexCounter) + " selected.")
        #select type [#,1]
        if receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][1] == "N\\A":
            selectType = Select(browser.find_element_by_id("type_%d" % (extensionPanelKeyCounter + 1)))
            selectType.deselect_all()

            # select value [#,2]
            # N/A

            # select label [#,3]
            # N/A

            # select line
            # N/A

            # select extension
            # N/A

        elif receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][1] == "Prefix":
            selectType = Select(browser.find_element_by_id("type_%d" % (extensionPanelKeyCounter + 1)))
            selectType.select_by_value('40')

            # select value [#,2]
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1)).clear()
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1))
            findValue.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][2])

            # select label [#,3]
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1)).clear()
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1))
            findLabel.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][3])

            # select line
            # N/A

            # select extension
            # N/A

        elif receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][1] == "BLF":
            selectType = Select(browser.find_element_by_id("type_%d" % (extensionPanelKeyCounter + 1)))
            selectType.select_by_value('16')

            # select value [#,2]
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1)).clear()
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1))
            findValue.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][2])

            # select label [#,3]
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1)).clear()
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1))
            findLabel.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][3])

            # select line [#,4]
            selectLine = Select(browser.find_element_by_id("line_%d" % (extensionPanelKeyCounter + 1)))
            selectLine.select_by_value('0')

            # select extension [#,5]
            findExtension = browser.find_element_by_id("extern_%d" % (extensionPanelKeyCounter + 1)).clear()
            findExtension = browser.find_element_by_id("extern_%d" % (extensionPanelKeyCounter + 1))
            findExtension.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][5])


        elif receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][1] == "SpeedDial":
            # select value [#,1] This selects Speed Dial
            selectType = Select(browser.find_element_by_id("type_%d" % (extensionPanelKeyCounter + 1)))
            selectType.select_by_value('13')

            # select value [#,2] This is the Cell Phone #
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1)).clear()
            findValue = browser.find_element_by_id("value_%d" % (extensionPanelKeyCounter + 1))
            findValue.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][2])

            # select label [#,3] This supplies a label for the key
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1)).clear()
            findLabel = browser.find_element_by_id("label_%d" % (extensionPanelKeyCounter + 1))
            findLabel.send_keys(receptionBLF[ ( ( extensionPanelCounter * 40 ) + extensionPanelKeyCounter ) ][3])

            # select line [#,4] This selects Line#1
            selectLine = Select(browser.find_element_by_id("line_%d" % (extensionPanelKeyCounter + 1)))
            selectLine.select_by_value('0')

            # select line [#,5] is null

        extensionPanelKeyCounter = extensionPanelKeyCounter + 1

    if not debugMode:
        confirmation = browser.find_element_by_id("btn_confirm1")
        confirmation.click()
        time.sleep(5)

    extensionPanelKeyCounter = 0  # restart the key counter
    extensionPanelCounter = extensionPanelCounter + 1

#  Function to Switch to Old Tab

# Gracefully close

print("\nDebug: Gracefully closing in 2 seconds...")
time.sleep(2)
browser.quit()

