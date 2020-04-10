import sys

from model.AddTwoIntsClient import AddTwoIntsClient
from model.AddTwoIntsServer import AddTwoIntsServer
from model.Launch import Launch
from model.Odometry import Odometry
from model.Roscore import Roscore
from model.Topic import Topic
from behave import *
from hamcrest import assert_that, greater_than_or_equal_to, less_than_or_equal_to, contains_string


def assert_dimension(expected_dimension, actual_dimension, tolerance):
    assert_that(actual_dimension, less_than_or_equal_to(float(expected_dimension) + float(tolerance)))
    assert_that(actual_dimension, greater_than_or_equal_to(float(expected_dimension) - float(tolerance)))


@given(u'ROS and the AddTwoIntsServer are running')
def step_impl(context):
    # Manually setup environment
    # Setup roscore
    context.roscore = Roscore()
    context.roscore.start_roscore()

    # initiate server node and wait for feedback marker
    context.server_node = AddTwoIntsServer()
    context.server_node.start_node(u"Ready to add two ints.")


@when(u'we request to add "{first_int}" and "{second_int}"')
def step_impl(context, first_int, second_int):
    context.first_int = first_int
    context.second_int = second_int
    clientNode = AddTwoIntsClient()

    # Send request to client node and capture immediate unknown response (handled differently to other nodes)
    context.response = clientNode.start_node_get_immediate_response(args=[first_int, second_int])


@then(u'the service should return the value "{return_value}"')
def step_impl(context, return_value):
    # Check that the captured String exists in the expected String
    expected_string = str(context.first_int + " + " + context.second_int + " = " + return_value)
    assert_that(context.response, contains_string(expected_string))
    assert_that(context.roscore.terminate())


@given(u'the simulation "{file_name}" in the package "{package}" has been launched')
def step_impl(context, file_name, package):
    # Setup Launch object
    context.simulation = Launch(package, file_name)
    # Run the Launch object using a Launch File - Param 1 is the feedback marker
    context.simulation.launch_with_file(u"Simulating feedback")


@given(u'the /odometry/base_raw topic is being monitored')
def step_impl(context):
    # Setup environment
    # Setup Topic object
    context.pose = Topic(u"/odometry/base_raw/pose")
    # Begin capture of Topic Echo for 10 lines
    context.starting_echo = context.pose.echo(10)
    # Map return value from echo to object of type msgs/nav_msgs/Odometry
    starting_position = Odometry(context.starting_echo)
    # Store starting position to shared context
    context.starting_position = starting_position


@when(u'given a velocity command of "{velocity_command}" with an orientation command of "{orientation_command}"')
def step_impl(context, velocity_command, orientation_command):
    context.cmd_vel = Topic(u"/twist_mux/cmd_vel")
    # Publish supplied command to the topic and watch for feedback marker
    context.cmd_vel.rostopic_pub(u"geometry_msgs/Twist", velocity_command, orientation_command,
                                 u"publishing and latching message.")


@then(
    u'the position of the robot should be "{x_pos}, {y_pos}, {z_pos}" (+- {pos_tolerance}) with an orientation of "{x_ori}, {y_ori}, {z_ori}, {w_ori}" (+- {ori_tolerance})')
def step_impl(context, x_pos, y_pos, z_pos, pos_tolerance, x_ori, y_ori, z_ori, w_ori, ori_tolerance):
    ending_echo = context.pose.echo(10)
    ending_position = Odometry(ending_echo)

    # Assert all dimensions are matching the expected result with tolerance
    assert_dimension(x_pos, ending_position.x_pos, pos_tolerance)
    assert_dimension(y_pos, ending_position.y_pos, pos_tolerance)
    assert_dimension(z_pos, ending_position.z_pos, pos_tolerance)
    assert_dimension(x_ori, ending_position.x_ori, ori_tolerance)
    assert_dimension(y_ori, ending_position.y_ori, ori_tolerance)
    assert_dimension(z_ori, ending_position.z_ori, ori_tolerance)
    assert_dimension(w_ori, ending_position.w_ori, ori_tolerance)

    # TODO Fix scientific notation bug in Odometry() mapping

    # Tear down environment
    assert_that(context.simulation.terminate())
    assert_that(context.pose.terminate())
    assert_that(context.cmd_vel.terminate())
