Feature: simple appium test

  Scenario: Discover feed should be turn off in Chrome
    Given I launch the emulator "Mobile_33"
    And I start the Appium server
    When I set the capabilities
    And I start the Appium Driver
    Then I open the application "Chrome"
    And I click on the "Options for Discover"
    And "Turn off" the discovered feed