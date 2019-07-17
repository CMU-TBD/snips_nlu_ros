#!/usr/bin/python

import rospy
import actionlib
from snips_nlu_ros.msg import (
    NLUGoal,
    NLUAction
)
import json

class SnipsNLU():

    def __init__(self):
        self._nlu_client = actionlib.SimpleActionClient("snips_nlu_ros/parse", NLUAction)
        self._nlu_client.wait_for_server()


    def parse(self, text):
        """
        Parse the string and return intent
        """

        goal = NLUGoal()
        goal.text = str(text)
        self._nlu_client.send_goal_and_wait(goal)
        result = self._nlu_client.get_result()

        #no intent found, return None 
        if result.intentName == "":
            return None, None, None
        else:
            #parse
            slot_info = json.loads(result.slot_json_string)
            return result.intentName, result.probability, slot_info
