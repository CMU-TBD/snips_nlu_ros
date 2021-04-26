#!/usr/bin/env python3

import rospy
import actionlib
from snips_nlu_ros.msg import Intent
from tbd_audio_msgs.msg import Utterance
import json
import alloy.ros

def test_pipeline():
    rospy.init_node('nlu_test_node')

    send_msg = Utterance()
    send_msg.header = alloy.ros.create_ros_header(rospy, "world")
    send_msg.text = "Where is 4221?"

    done = False
    def callback(msg: Intent):
        assert msg.intentName == "campusLocationSlotFill"
        assert msg.header.frame_id == send_msg.header.frame_id
        assert msg.header.stamp == send_msg.header.stamp
        nonlocal done
        done = True
        pass

    # wait 5 seconds for NLU to start
    rospy.sleep(5)

    rospy.Subscriber('intent', Intent, callback=callback, queue_size=1)
    pub = rospy.Publisher("utterance", Utterance, queue_size=1, latch=True)
    for i in range(0,30):
        if done:
            break
        pub.publish(send_msg)
        rospy.sleep(0.1)
    assert done
