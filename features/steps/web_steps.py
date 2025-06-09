######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'product_'


@when('I visit the "{page}" Page')
def step_visit_page(context, page):
    """Navigate to a named page"""
    if page.lower() == "home page":
        context.driver.get(context.base_url)
    else:
        # extend for other pages by name if needed
        context.driver.get(context.base_url + "/" + page.replace(" ", "_").lower())

@when('I set the "{field}" to "{value}"')
def step_set_field(context, field, value):
    """Set the value of an input field by its label name"""
    elem = context.driver.find_element_by_id(f"{field.lower()}-input")
    elem.clear()
    elem.send_keys(value)

@when('I select "{option}" in the "{dropdown}" dropdown')
def step_select_dropdown(context, option, dropdown):
    """Select an option in a select element"""
    elem = context.driver.find_element_by_id(f"{dropdown.lower()}-dropdown")
    select = Select(elem)
    select.select_by_visible_text(option)

@when('I press the "{button}" button')
def step_press_button(context, button):
    """Click a button by its name"""
    btn = context.driver.find_element_by_id(f"{button.lower()}-btn")
    btn.click()

@when('I copy the "{field}" field')
def step_copy_field(context, field):
    """Copy the value of a field into context.clipboard"""
    elem = context.driver.find_element_by_id(f"{field.lower()}-input")
    context.clipboard = elem.get_attribute("value")

@when('I paste the "{field}" field')
def step_paste_field(context, field):
    """Paste the stored clipboard value into a field"""
    elem = context.driver.find_element_by_id(f"{field.lower()}-input")
    elem.clear()
    elem.send_keys(context.clipboard)

@when('I change "{field}" to "{value}"')
def step_change_field(context, field, value):
    """Alias for setting a field"""
    # reuse set logic
    step_set_field(context, field, value)

@then('I should see "{text}" in the results')
def step_see_in_results(context, text):
    """Assert that text appears in the search results container"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, 'search_results'), text)
    )
    assert found, f"Expected '{text}' to be in results"

@then('I should not see "{text}" in the results')
def step_not_see_in_results(context, text):
    """Assert that text does not appear in the search results"""
    elem = context.driver.find_element_by_id('search_results')
    assert text not in elem.text, f"Did not expect '{text}' in results"

@then('I should see the message "{message}"')
def step_see_message(context, message):
    """Assert that a flash message appears"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, 'flash_message'), message)
    )
    assert found, f"Expected flash message '{message}'"

@then('I should see "{value}" in the "{field}" field')
def step_field_value(context, value, field):
    """Assert that an input field shows a given value"""
    elem = context.driver.find_element_by_id(f"{field.lower()}-input")
    actual = elem.get_attribute('value')
    assert actual == value, f"Expected {field}='{value}', but got '{actual}'"