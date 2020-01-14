from AddTwoIntsClient import AddTwoIntsClient
from AddTwoIntsServer import AddTwoIntsServer
from Roscore import Roscore
from behave import *


@given('ROS and the "{server}" are running')
def step_impl(context, server):
    context.roscore = Roscore()
    context.roscore.start_roscore()

    context.server_node = AddTwoIntsServer()
    context.server_node.start_node("Ready to add two ints.")


@when('we request to add "{first_int}" and "{second_int}" on the "{client}"')
def step_impl(context, first_int, second_int, client):
    context.first_int = first_int
    context.second_int = second_int
    clientNode = AddTwoIntsClient()
    context.response = clientNode.start_node_get_immediate_response(args=[first_int, second_int])


@then('the service should return the value "{return_value}"')
def step_impl(context, return_value):
    expected_string = str(context.first_int + " + " + context.second_int + " = " + return_value)
    assert expected_string in context.response
    assert context.roscore.terminate()
