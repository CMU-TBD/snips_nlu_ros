#!/usr/bin/python


import rospy
import io
import json
import actionlib

import alloy.ros

from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu_ros.msg import (
    NLUGoal,
    NLUAction,
    NLUResult
)

class SnipsNLUWrapper():

    def __init__(self):
        #get the path to the dataset
        dataset_path = rospy.get_param('snips_nlu_ros/dataset') 
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
        load_resources(u"en")
        self._nlu_engine = SnipsNLUEngine()
        self._nlu_engine.fit(dataset)

        #start actionlib
        self._nlu_server = actionlib.SimpleActionServer("snips_nlu_ros/parse", NLUAction, self._parse_callback, auto_start=False)
        self._nlu_server.start()
        rospy.loginfo('Snips NLU Started')

    def  _parse_callback(self, goal):
        text = unicode(goal.text,'utf-8')
        parse_result = self._nlu_engine.parse(text)
        nlu_result = NLUResult()
        if parse_result['intent'] is not None:
            nlu_result.intentName = str(parse_result['intent']['intentName'])
            nlu_result.probability = parse_result['intent']['probability'] 
        else:
            nlu_result.intentName = ""
        nlu_result.slot_json_string = json.dumps(parse_result["slots"])
        self._nlu_server.set_succeeded(nlu_result)


def main():
    rospy.init_node('snips_nlu_node')
    snw = SnipsNLUWrapper()
    rospy.spin()

if __name__ == '__main__':
    main()
