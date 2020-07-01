from selenium import webdriver
from PIL import Image

import IPython.display as Imm

# try:
#     from PIL import Image
# except ImportError:
#     import Image
import pytesseract

import shutil

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
# import loguru

success = False

import time
from threading import Thread



while success != True:
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("window-size=1200x600")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://lvr.land.moi.gov.tw/homePage.action")
    # print(driver.find_elements_by_class_name("ui-dialog-titlebar-close ui-corner-all"))
    # time.sleep(5)
    # print(driver.window_handles)
    # driver.switch_to_window(driver.window_handles[0])
    # print(driver.find_elements_by_class_name("ui-dialog-titlebar-close ui-corner-all"))
    # driver.find_elements_by_class_name("ui-dialog-titlebar-close ui-corner-all").click()
    driver.find_element_by_id("land").click()
    driver.save_screenshot('capture.png')
    vfImg = driver.find_element_by_id("checknum")

    left = vfImg.location['x']+470
    right = left + vfImg.size['width']+100
    top = vfImg.location['y']+280
    bottom = top + vfImg.size['height']+80

    img = Image.open('capture.png')
    img = img.crop((left, top, right, bottom))
    img.save('vfImg.png', 'png')
    os.remove('capture.png')
    # time.sleep(5)
    
    # time.sleep(3)
    # driver.close()
    # code = pytesseract.image_to_string(Image.open('vfImg.png'))
    code = pytesseract.image_to_string(Image.open('vfImg.png'), lang='eng', \
            config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    print(f'code: {code}')
    os.remove('vfImg.png')
    code = ''.join(c for c in code if c.isdigit())
    # if len(code) != 4:
    #     driver.close()
    #     continue
    # print(f'code: {code}')
    # elem_vf = driver.find_element_by_id("rand_code")
    # elem_vf.send_keys(code)
    time.sleep(5)

    driver.find_element_by_id("Image2").click()
    
    # elem_user = driver.find_element_by_id("userid-inputEl")
    # elem_user.send_keys(personalInf.studentID)
    # elem_pwd = driver.find_element_by_name("password")
    # elem_pwd.send_keys(personalInf.password)
    # elem_vf = driver.find_element_by_id("validateCode-inputEl")
    # elem_vf.send_keys(code)
    # driver.find_element_by_id("Chkb_Qry_paytype").click()
    # driver.find_element_by_class_name("close_btn").send_keys(Keys.COMMAND, Keys.OPTION, i)
    
    try:
        driver.find_element_by_class_name("close_btn").click()
        # driver.find_element_by_id("Chkb_Qry_paytype").click()
    except:
        # print("Loading too much time!")
        print("Err")
        driver.close()
        continue
    select = Select(driver.find_element_by_id('Qry_city'))

    # select by visible text
    # select.select_by_visible_text('Banana')
    
    

    # select by value 
    time.sleep(1)
    select.select_by_value('A')
    # driver.find_element_by_xpath("//select[@id='Qry_city']/option[@value='A']").click()
    time.sleep(1)
    select_box = driver.find_element_by_xpath("//select[@id='Qry_area_office']")
    options = [x.get_attribute("value")  for x in select_box.find_elements_by_tag_name("option")]
    print(options)
    # for element in options:
    #     print(element.get_attribute("value"))

    select = Select(driver.find_element_by_id('Qry_area_office'))
    f = str(options[3])
    print(f'f{f}')
    select.select_by_value(f)
    driver.find_element_by_id('search_s_btn').click()

    time.sleep(5)
    # page_tol
    print(driver.find_element_by_id('hiddenresult').get_attribute('innerHTML'))

    time.sleep(10)
    driver.close()
    break

#     delay = 10 # seconds
#     try:
#         fastrack = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'button-1017-btnWrap')));
#         fastrack.click()
#         cookieValue = str(driver.get_cookies()[0]["value"])
#         print('cookieValue: \n', cookieValue)
#         while True:
#             q = input("Press \"q\" to exit: ")

#             if q == "q":
#                 success = True

#                 # driver.close()
#                 break

# #         driver.close()
#     except TimeoutException:
#         print("Loading too much time!")
#         driver.close()
#         print("Reloading Page")
#         continue
#     except UnexpectedAlertPresentException as err:
#         # print("Loading took too much time!")
#         # print(type(err))    # the exception instance
#         # print("aa", err.args)     # arguments stored in .args
#         # print("bb", err.args)
#         print("code: ", code)
#         print(err)
#         driver.close()
#         print("Reloading Page")
#         continue
#     except:
#         print("Error")
#         driver.close()
#         print("Reloading Page")
#         continue

# try:
#     # t.raise_exception()

#     # t.join()
#     driver.close()
#     print("\nClosing browser!!\n")
#     # sys.exit()
    
# except:
#     print("Close browser!!")