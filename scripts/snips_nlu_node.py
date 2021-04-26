#!/usr/bin/env python3

import rospy
import io
import json
import actionlib

import alloy.ros

from snips_nlu import load_resources, SnipsNLUEngine
# from snips_nlu_ros.msg import (
#     NLUGoal,
#     NLUAction,
#     NLUResult
# )

from tbd_audio_msgs.msg import Utterance
from snips_nlu_ros.msg import Intent

class SnipsNLUWrapper():

    def __init__(self):
        #get the path to the dataset
        dataset_path = rospy.get_param('~dataset') 
        #try to reslove the path
        dataset_path = alloy.ros.resolve_res_path(dataset_path,'snips_nlu_ros','dataset')
        #load the dataset into memory
        try:
            fs = io.open(dataset_path)
        except IOError:
            rospy.logerr('Snips NLU dataset path invalid. Given: {}'.format(dataset_path))
            raise RuntimeError()
        dataset = json.load(fs)
        #fit the dataset
        self._nlu_engine = SnipsNLUEngine()
        self._nlu_engine.fit(dataset)

        # #start actionlib
        # self._nlu_server = actionlib.SimpleActionServer("snips_nlu_ros/parse", NLUAction, self._parse_callback, auto_start=False)
        # self._nlu_server.start()

        # start the subscriber
        self._nlu_subscriber = rospy.Subscriber("utterance", Utterance, self._parse_callback)

        # create the publisher
        self._nlu_publisher = rospy.Publisher("intent", Intent, queue_size=10)
        

        rospy.loginfo('Snips NLU Started')

    def  _parse_callback(self, msg):
        # print(msg.text)
        parse_result = self._nlu_engine.parse(msg.text)
        intent = Intent()
        intent.header = msg.header
        # print(parse_result)
        if parse_result['intent'] is not None:
            intent.intentName = str(parse_result['intent']['intentName'])
            intent.probability = parse_result['intent']['probability'] 
        else:
            intent.intentName = ""
        intent.slot_json_string = json.dumps(parse_result["slots"])
        # print(intent)
        # self._nlu_server.set_succeeded(nlu_result)
        self._nlu_publisher.publish(intent)


def main():
    rospy.init_node('snips_nlu_node')
    snw = SnipsNLUWrapper()
    rospy.spin()

if __name__ == '__main__':
    main()
