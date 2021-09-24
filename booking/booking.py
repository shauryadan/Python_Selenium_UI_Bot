import booking.constants as const
from selenium import webdriver
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    def __init__(self,
                 driver_path=r"C:\Users\Shaurya\PersonalProjects\PythonSeleniumUIBotTutorial\chromedriver.exe",
                 chrome_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 teardown=False):
        self.driver_path = driver_path
        self.options = webdriver.ChromeOptions()
        self.teardown = teardown
        self.options.binary_location = chrome_path
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.driver.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.driver.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.driver.find_element_by_id("ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.driver.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.driver.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.driver.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.driver.find_element_by_id('xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.driver.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            adults_value_element = self.driver.find_element_by_id('group_adults')
            adults_value = adults_value_element.get_attribute(
                'value'
            ) #gives back adults count

            if int(adults_value) == 1:
                break

        increase_adults_element = self.driver.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(count-1):
            increase_adults_element.click()

    def click_search(self):
        search_button = self.driver.find_element_by_css_selector(
            'button[type="submit"]'
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self.driver)
        filtration.apply_star_rating(3,4,5)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.driver.find_element_by_id(
            'hotellist_inner'
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names = ["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table )

    def refresh(self):
        self.driver.refresh()