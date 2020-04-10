Feature: Basic testing of the movement of thorvald using the topic /twist_mux/cmd_vel

  Scenario: Move in the x direction for 1 second with a velocity of 0.1
    Given the simulation "thorvald_ii_4wd4ws_std_sim.launch" in the package "thorvald_example_robots" has been launched
    And the /odometry/base_raw topic is being monitored
    When given a velocity command of "[0.1, 0.00, 0.00]" with an orientation command of "[0.00, 0.00, 0.00]"
    Then the position of the robot should be "0.02, 0.00, 0.00" (+- 0.01) with an orientation of "0.00, 0.00, 0.00, 1.0" (+- 0.01)

  Scenario: Move in the y direction for 1 second with a velocity of 0.1
    Given the simulation "thorvald_ii_4wd4ws_std_sim.launch" in the package "thorvald_example_robots" has been launched
    And the /odometry/base_raw topic is being monitored
    When given a velocity command of "[0.00, 0.1, 0.00]" with an orientation command of "[0.00, 0.00, 0.00]"
    Then the position of the robot should be "0.01, 0.02, 0.00" (+- 0.01) with an orientation of "0.00, 0.00, 0.00, 1.0" (+- 0.01)

  Scenario: Move in the z direction for 1 second with a velocity of 0.1
    Given the simulation "thorvald_ii_4wd4ws_std_sim.launch" in the package "thorvald_example_robots" has been launched
    And the /odometry/base_raw topic is being monitored
    When given a velocity command of "[0.00, 0.00, 0.1]" with an orientation command of "[0.00, 0.00, 0.00]"
    Then the position of the robot should be "0.00, 0.00, 0.00" (+- 0.01) with an orientation of "0.00, 0.00, 0.00, 1.0" (+- 0.01)

