#!/usr/bin/env python3

import rospy
import actionlib
from snips_nlu_ros.msg import (
    NLUGoal,
    NLUAction
)
import json

def parse(client, text):
    goal = NLUGoal
    goal.text = text
    client.send_goal_and_wait(goal)
    result = client.get_result()
    print(json.loads(result.slot_json_string))
    return result

def main():
    rospy.init_node('nlu_test_node')
    
    nlu_client = actionlib.SimpleActionClient("snips_nlu_ros/parse", NLUAction)
    nlu_client.wait_for_server()
    print('\n - parsing - "Hi" -\n')
    print(parse(nlu_client,"Hi"))
    print('\n - parsing - "My name is Alex" -\n')    
    print(parse(nlu_client,"My name is Alex"))
    print('\n - parsing - "Direction to Room A507" -\n')
    print(parse(nlu_client,"Direction to Room A507"))


if __name__ == '__main__':
    main()