def lookup(question_path, user_name, user_id,job_id):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.chrome.options import Options
    import time
    from PIL import Image
    from selenium.webdriver.support.ui import Select
    from random import randint
    from datetime import datetime
    import os
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    delay = 17
    def job_repush(question_path, user_name, user_id, job_id):
        print('-'*100)
        print('[Browser Job Repush] | Link: '+str(question_path))
        print('[Browser Job Repush] | User: '+str(user_name))
        print('[Browser Job Repush] | User ID: '+str(user_id))
        repush = open('job_repush.txt','a')
        data = question_path+'<repush>'+user_name+'<repush>'+str(user_id)+'<repush>'+job_id+'\n'
        repush.write(data)
        repush.close()
        print('[Browser Job Repush] | Status: Done')
        print('-'*100)
    
    def check(element):
        time.sleep(1)
        try:
            driver.find_element_by_xpath(element)
        except NoSuchElementException:
            return False
        return True
    def checking_sign_in():
        status = False
        # sign_in = check('//*[@id="root"]/div/header/nav/ul/li[4]/button/span/span[contains(text(),"Sign in")]')
        account = check('//*[@id="root"]/div/header/nav/ul/li[4]/button/span[contains(text(),"dzou23@uwo.ca")]')
        logo = check('//*[@id="root"]/div/div/div/div/a/img[@alt="WolframAlpha Pro"]')
        count = 0
        stats = 'not fail'
        while account == False and logo == False and status == False:
            count+=1
            stats = ''
            if count < 5:
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/header/nav/ul/li[4]/button/span/span[contains(text(),"Sign in")]')))
                except TimeoutException:
                    print ("[Browser] |Loading took too much time!|")
                    job_repush(question_path, user_name, user_id, job_id)
                else: 
                    try:
                        time.sleep(5)
                        driver.find_element_by_xpath('//*[@id="root"]/div/header/nav/ul/li[4]/button/span/span[contains(text(),"Sign in")]').click()
                    except Exception:
                        status = False
                        print('[Browser] |Retrying login|')
                        account = check('//*[@id="root"]/div/header/nav/ul/li[4]/button/span[contains(text(),"dzou23@uwo.ca")]')
                        logo = check('//*[@id="root"]/div/div/div/div/a/img[@alt="WolframAlpha Pro"]')
            else:
                stats = 'fail'
                break
        if stats == 'fail':
            job_repush(question_path, user_name, user_id, job_id)
            name = job_id+'_______FAILLL.png'
            screen = driver.save_screenshot(name)
            driver.close()
            print('[Browser] |Failed|')
            return False
            
    def saving(specific_name):
        now = datetime.now()
        if len(specific_name) == 0:
            name = job_id+'result.png'
            screen = driver.save_screenshot(name)
            im = Image.open(name)
            width, height = im.size
            left = 0
            top = 50
            right = width
            bottom = height
            new = im.crop((left, top, right, bottom))
            new.save(name)
            job_status = open('job_status.txt','r')
            if job_status.readline() != 'writing':
                job_status.close()
                job_status = open('job_status.txt','w')
                job_status.write('temp writing')
                job_status.close()
                job = open('job.txt','a')
                print('[Browser] |Job Creating|')
                job.write(str([name,user_id,question_path])+'\n')
                job.close()
                job_status = open('job_status.txt','w')
                job_status.write('not writing')
                job_status.close()
        else:
            name = job_id+'no_step_by_step.png'
            job_status = open('job_status.txt','r')
            if job_status.readline() != 'writing':
                job_status.close()
                job_status = open('job_status.txt','w')
                job_status.write('temp writing')
                job_status.close()
                job = open('job.txt','a')
                print('[Browser] |Job Creating|')
                job.write(str([name,user_id,question_path])+'\n')
                job.close()
                job_status = open('job_status.txt','w')
                job_status.write('not writing')
                job_status.close()
    ############################################
    with open('jq.js', 'r') as jquery_js:
        jquery = jquery_js.read()  
    
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)
    total_height = 5000
    driver.set_window_size(1920, total_height)
    driver.get(question_path)
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '_2HkkNXzH._1MOABRzM.gWLqKuPt')))
        now = datetime.now()
        print("[Browser] |Job ID: "+job_id)
        print("[Browser] |Program Start time:", now)
        print('[Browser] |Opening Wolfram|')
    except TimeoutException:
        print ("Loading took too much time!")
        job_repush(question_path, user_name, user_id, job_id)
    finally:
        driver.execute_script(jquery)
        driver.execute_script('$("._2HkkNXzH._1MOABRzM.gWLqKuPt").click()')
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'wa-logo')))
            print('[Browser] |Loging In|')
        except TimeoutException:
            print ("[Browser] |Loading took too much time!|")
            job_repush(question_path, user_name, user_id, job_id)
        driver.execute_script(jquery)
        driver.execute_script('$("#wolfram-id input").val("dzou23@uwo.ca")')
        driver.execute_script('$("#pw input").val("Jimolkio0~")')
        driver.execute_script('$("#sign-in-btn").click()')
        existing = ''
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'BkQEt310')))
        except TimeoutException:
            print ("[Browser] |Loading took too much time!|")
            job_repush(question_path, user_name, user_id, job_id)
            driver.close()
        else:
            existing = checking_sign_in()
        if existing != False:
            if check('//*[@id="root"]/div/header/nav/ul/li[4]/button/span[contains(text(),"dzou23@uwo.ca")]'):
                print('[Browser] |Login Sucessful|')
                # driver.get(question_path)
                try:
                    delays = 6
                    myElem = WebDriverWait(driver, delays).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Step-by-step solution")]')))
                except TimeoutException:
                    print ("[Browser] |Does not have step by step solution|")
                    saving('no_exist')
                    driver.close()
                else:
                    print('[Browser] |Question loaded|')
                    driver.find_element_by_xpath('//span[contains(text(),"Step-by-step solution")]').click()
                    try:
                        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//h3[contains(text(),"STEP 1")]')))
                    except TimeoutException:
                        print ("[Browser] |Loading took too much time!|")
                        job_repush(question_path, user_name, user_id, job_id)
                        driver.close()
                    else:
                        print('[Browser] |Step-by-step solution Expanding|')
                        try:
                            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Show all steps")]')))
                        except TimeoutException:
                            print ("[Browser] |Loading took too much time!|")
                            job_repush(question_path, user_name, user_id, job_id)
                            driver.close()
                        else:   
                            driver.find_element_by_xpath('//span[contains(text(),"Show all steps")]').click()
                            time.sleep(7)
                            if check('//span[contains(text(),"Got It")]') == True:
                                driver.find_element_by_xpath('//span[contains(text(),"Got It")]').click()
                            
                            saving('')
                            print('-'*100)
                            print('[Browser] |Done Job:',job_id,'|')
                            driver.close()
                            now = datetime.now()
                            print('[Browser] |Broswer Closing|')
                            print("[Browser] |Program End time:", now)
                            print('-'*100)
                            return True
            else:
                checking_sign_in('yes')
                return True