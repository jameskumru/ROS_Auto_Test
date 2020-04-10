from Node import Node
import os


class AddTwoIntsClient(Node):

    def __init__(self):
        super(AddTwoIntsClient, self).__init__("add_two_ints_client", "auto_test", os.environ['CATKIN_WS'] + "/devel/setup.sh")
