######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
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
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = "customer_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    WebDriverWait(context.driver, 20).until( 
        EC.presence_of_element_located((By.ID, 'known_element_id_after_load'))
    )
    # Uncomment next line to take a screenshot of the web page
    context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    WebDriverWait(context.driver, 10).until(EC.title_contains(message))
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(" ", "_") + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "search_results"), name
        )
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    assert found


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
