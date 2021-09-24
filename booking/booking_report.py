# This file includes methods that parse specific data we need from each of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement

class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements_by_class_name(
            'sr_property_block'
        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # pull hotel name
            hotel_name = deal_box.find_element_by_class_name(
                'sr-hotel__name'
            ).get_attribute('innerHTML').strip()

            # pull hotel price
            hotel_price = deal_box.find_element_by_class_name(
                'prco-valign-middle-helper'
            ).get_attribute('innerHTML').strip()

            # pull hotel score
            hotel_score = deal_box.get_attribute(
                'data-score'
            ).strip()

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        return collection
