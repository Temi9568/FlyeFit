from selenium import webdriver
from selenium.webdriver.firefox.options import  Options
import shelve
import schedule
import time
import datetime


def login_(email, password, booking_time: str):

    start_time = time.perf_counter()
    url = "https://myflye.flyefit.ie/login"

    options = Options()
    options.headless = True  # Ensures Firefox does not actually open. Alternative is MOZ_HEADLESS=1 ON the commandline
    browser = webdriver.Firefox(options=options)
    browser.get(url)

    email_elem = browser.find_element_by_css_selector('input[name="email_address"]')
    email_elem.send_keys(email)

    pass_elem = browser.find_element_by_css_selector('input[name="password"]')
    pass_elem.send_keys(password)

    submit = browser.find_element_by_css_selector('input[name="log_in"]')
    submit.click()

    browser.implicitly_wait(5)
    browser.switch_to.window(browser.window_handles[0])

    link = str(browser.find_element_by_css_selector('a[href="/myflye/book-workout"]').get_attribute('href'))
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    link += "/167/14/" + tomorrow  # Getting tomorrow's date in order to get link for next day's booking page
    browser.get(link)

    browser.implicitly_wait(2)
    browser.switch_to.window(browser.window_handles[0])

    try:
        book_elems = browser.find_elements_by_css_selector('p[class="btn-primary ff_class "]')
        for elem in book_elems:
            if booking_time in str(elem.get_attribute("data-course-time")):
                elem.click()

                browser.implicitly_wait(2)
                browser.switch_to.window(browser.window_handles[0])

                book_elem = browser.find_element_by_css_selector('a[name="book_class"]')
                book_elem.click()

                browser.implicitly_wait(2)
                # browser.switch_to.window(browser.window_handles[0])
                browser.close()

                # bookings_page = browser.find_element_by_css_selector('a[href="/myflye/your-bookings"]').click()
                # browser.get("")

                print("Booking is successful")

    except:
        print("Booking not successful")

    finally:
        end_time = time.perf_counter()
        print("Done in {} seconds".format(int(end_time - start_time))) # Inacse try & except block does not get reached, this stops code from being stuck indefintely. Also times how long it took.



user = "YOUR EMAIL"
key = "YOUR PASSWORD"
time_ = "11:30" # Assuming you want to book the 11:30 sesssion 

schedule.every().day.at("11:32").do(login_, user, key, time_)

while True:
    schedule.run_pending()  # Checks if a task is pending and if so does not exit script until task has been executed
    time.sleep(5)
