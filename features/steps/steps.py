import subprocess
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from behave import given, when, then

# Global variables to track server and emulator status
sdk_path = r"D:\Android"


@given('I start the Appium server')
def step_given_i_start_appium_server(context, port=4723):
    command = f'start cmd /k appium --use-plugins=relaxed-caps -p {port}'
    context.appium_process = subprocess.Popen(command, shell=True)
    time.sleep(5)


@given('I launch the emulator "{emulator_name}"')
def step_given_i_launch_emulator(context, emulator_name):
    # Launch the emulator with the specified name
    command = f'start cmd /k "{sdk_path}\\emulator\\emulator.exe" -avd {emulator_name} -no-snapshot-load -gpu host'
    context.emulator_process = subprocess.Popen(command, shell=True)
    time.sleep(30)
    wait_for_emulator_to_load()


def wait_for_emulator_to_load():
    print("Waiting for the emulator to boot...")
    while True:
        result = subprocess.run(['adb', 'shell', 'getprop', 'sys.boot_completed'], capture_output=True, text=True)
        if result.stdout.strip() == '1':
            print("Boot completed. Checking for home screen...")
            break
        time.sleep(5)

    while True:
        # Check if the launcher is running
        result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages'], capture_output=True, text=True)
        if 'com.google.android.apps.nexuslauncher' in result.stdout:
            print("Home screen is displayed.")
            break
        time.sleep(5)  # Check every 5 seconds


@when('I set the capabilities')
def step_when_i_set_the_capabilities(context):
    context.desired_caps = {
        'platformName': 'Android',  # Change to 'iOS' for iOS devices
        'platformVersion': '13.0',  # Change to your device's version
        'deviceName': 'Mobile_33',  # Change to your device's name
        'automationName': 'UiAutomator2'  # Use 'XCUITest' for iOS
    }
    context.capabilities_options = UiAutomator2Options().load_capabilities(context.desired_caps)


@when('I start the Appium Driver')
def step_when_i_start_the_appium_driver(context):
    context.driver = webdriver.Remote(command_executor='http://localhost:4723', options=context.capabilities_options)
    context.driver.implicitly_wait(20)


@then('I open the application "{appname}"')
def step_then_i_open_the_application(context, appname):
    context.driver.find_element(by=AppiumBy.XPATH,
                                value=f'//android.widget.TextView[@content-desc="{appname}"]').click()


@then('I click on the "{element}"')
def step_then_i_click_on_the(context, element):
    context.driver.find_element(by=AppiumBy.XPATH,
                                value=f'//android.widget.ImageButton[@content-desc="{element}"]').click()


@then('"{option}" the discovered feed')
def step_then_the_discovered_feed(context, option):
    context.driver.find_element(by=AppiumBy.XPATH,
                                value=f'//android.widget.TextView[@resource-id="com.android.chrome:id/menu_item_text" '
                                      f'and @text="{option}"]').click()
