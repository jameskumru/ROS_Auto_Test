from Node import Node
import os


class AddTwoIntsServer(Node):

    def __init__(self):
        super(AddTwoIntsServer, self).__init__("add_two_ints_server", "auto_test", os.environ['CATKIN_WS'] + "/devel/setup.sh")



