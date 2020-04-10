Feature: Test simple addition service

  Scenario: run a simple test
     Given ROS and the AddTwoIntsServer are running
      When we request to add "2" and "2"
      Then the service should return the value "3"

  Scenario: run a simple test
     Given ROS and the AddTwoIntsServer are running
      When we request to add "3" and "4"
      Then the service should return the value "7"