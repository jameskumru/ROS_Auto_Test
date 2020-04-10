#!/usr/bin/env python
import rospy
import unittest

from hamcrest import assert_that, equal_to
from subprocess import Popen, PIPE
import re
import sys


class TestExecBehave(unittest.TestCase):
    def test_exec_behave_context(self):
        cmd = "behave"

        cmd = "{command} {argument}".format(command=cmd, argument=str(sys.argv[1]))

        p = Popen(cmd, stdout=PIPE, executable="/bin/bash", shell=True)
        out, err = p.communicate()

        failed_scenarios = int(re.search(r"\d scenarios passed, (\d+) failed", out).group(1))

        print(out)
        print(err)

        assert_that(failed_scenarios, equal_to(0))


if __name__ == '__main__':
    import rostest

    rospy.loginfo("-I- exec_behave started")
    rospy.loginfo("-D- sys.argv: %s" % str(sys.argv))
    rostest.rosrun("ros_behave", 'exec_behave', TestExecBehave, sys.argv)
