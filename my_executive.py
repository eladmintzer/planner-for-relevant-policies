# Elad Mintzer 203768460

import sys
import subprocess
import os
import json
import random
import itertools

from pddlsim.executors.executor import Executor
from pddlsim.local_simulator import LocalSimulator

class MYPlanner(Executor):
    def __init__(self,policy_file_name):
        super(MYPlanner, self).__init__()
        if ".json" not in policy_file_name:
            print "Error, expect to json policy file, got:" +  policy_file_name
        file = open(policy_file_name, mode='r')
        f_policy = json.load(file)
        file.close()

        self.policy = {}
        for key,item in f_policy.items():
            self.policy[key] = (set(item[0]),item[1])
        self.prev_action_list = []
        self.current_state = None
        self.prob_dict = None
        self.goals = []
        self.randomized_chosen = False
        self.curr_state_set = set()

    def initialize(self, services):
        super(MYPlanner, self).initialize(services)
        self.services = services
        self.goals = self.services.parser.goals[0].parts
    def update_state_set(self):
        self.curr_state_set = set()
        for ke,item in self.current_state.items():
            if ke == "=":
                continue
            for literal in item:
                if len(literal) != 0:
                    var = "{}(".format(ke)
                    var += ", ".join(literal)
                    var += ")"
                    self.curr_state_set.add(var)
    def update_probalistic_dict(self):
        if self.prob_dict != None:
            return
        self.prob_dict = {}
        all_action_dict = self.services.valid_actions.provider.parser.actions

        for ke,item in all_action_dict.items():
            try:
                add_list = list(item.addlist)
            except AttributeError:
                add_list = list(item.addlists)

            if len(add_list[-1]) == 0:
                add_list.pop(-1)
            if len(add_list) != 2:
                continue
            src = [None,None]
            dst = [None,None]
            l1 = list(itertools.chain(*add_list[0]))
            l1 = list(itertools.chain(*l1))
            l2 = list(itertools.chain(*add_list[1]))
            l2 = list(itertools.chain(*l2))
            for var1,var2 in zip(l1,l2):
                if var1 != var2:
                    src[0] = var1
                    dst[0] = var2

            for ind, literal in enumerate(item.signature):
                if literal[0] == src[0]:
                    src[1] = ind
                if literal[0] == dst[0]:
                    dst[1] = ind
            if dst[1] != None and src[1] != None:
                try:
                    item.prob_list
                except AttributeError:
                    pass
                else:
                    if item.prob_list[0] > item.prob_list[1]:
                        self.prob_dict[ke] = [dst[1],src[1]]
                    else:
                        self.prob_dict[ke] = [src[1], dst[1]]

    def next_action(self):
        if self.services.goal_tracking.reached_all_goals():
            return None

        self.prev_state = self.current_state
        self.current_state = self.services.perception.get_state()

        self.update_state_set()

        # In case that nothing change, repeat action.
        if (self.current_state == self.prev_state and
            not self.randomized_chosen):
            return self.prev_action_list[-1]

        valid_actions = self.action_list_str_to_set_str(self.services.valid_actions.get())

        action = self.choose(valid_actions)
        self.prev_action_list.append(action)
        return action

    def choose(self,valid_actions):
        init_optional_actions = []
        optional_actions = []
        activated_actions = []

        self.update_probalistic_dict()

        for c_act,item in self.policy.items():
            if c_act in valid_actions:
                ex = item[0] - self.curr_state_set

                # In case that literal from policy satisfiy..
                if len(ex) == 0:
                    it = (c_act, item[0], item[1])
                    init_optional_actions.append(it)

        init_optional_actions.sort(key=lambda tup: tup[-1])

        for it in init_optional_actions:
            if not it[0] in self.prev_action_list:
                optional_actions.append(it)
            else:
                activated_actions.append(it)
        self.randomized_chosen = True
        ac_tuple = ["",0,0]
        if len(optional_actions) != 0:
            self.randomized_chosen = False

            ac_tuple = optional_actions[-1]
        elif len(activated_actions) != 0:
            ac_tuple = random.choice(activated_actions)
        else:
            ac_tuple[0] = random.choice(list(valid_actions))

        return self.optimizeActionProb(ac_tuple[0], valid_actions)

    def optimizeActionProb(self, full_action_name, valid_actions):
        retAction = full_action_name

        action_name = full_action_name[1:].split(" ")[0]
        if action_name in self.prob_dict:
            pref_action_name = "({} ".format(action_name)

            action_literals = full_action_name.replace(pref_action_name,"")[:-1].split(" ")

            action_literals[self.prob_dict[action_name][0]] = action_literals[self.prob_dict[action_name][1]]
            lit_str = " ".join(action_literals)
            curr_action = "({} {})".format(action_name, lit_str)
            if curr_action in valid_actions:
                retAction = curr_action

        return retAction

    def action_list_str_to_set_str(self, list_str_actions):
        set_actions = set()

        for str_action in list_str_actions:
            set_actions.add(str_action)

        return set_actions

    def action_str_to_tuple(self, str_action):
        return tuple(str_action[1:-1].split())

# Define the main function
def main():
    mode = sys.argv[1]
    domain_file = sys.argv[2]
    problem_file = sys.argv[3]
    policy_file = sys.argv[4]

    problem_pref = "#"+ domain_file.split("/")[-1]+"#"+problem_file.split("/")[-1]
    problem_pref= problem_pref.replace(".pddl","")
    final_policy_file = policy_file + problem_pref
    human_policy_out = final_policy_file + ".out"
    human_policy_json = final_policy_file + ".json"

    if mode == "-L":

        call1 = ["src/prp",
               os.path.abspath(domain_file),
               os.path.abspath(problem_file),
                "--dump-policy",
                 "2"]
        call1.extend(["--trials","100","--forgetpolicy","0"])

        print "run: " + " ".join(call1)
        subprocess.call(call1)
        call2=["mv",  "policy.out",  human_policy_out]
        print "run: " + " ".join(call2)
        subprocess.call(call2)
        call3 = ["python2.7","prp-scripts/translate_policy.py",
                 os.path.abspath(human_policy_out)]
        print "run: " + " ".join(call3)
        subprocess.call(call3)
        print("Finish training..")
    elif mode == "-E":
        print("Execute Mode mode")
        if not os.path.exists(human_policy_json):
            print "missing ploicy file, first run -L"
            exit(-1)
        print LocalSimulator().run(domain_file, problem_file, MYPlanner(human_policy_json))
    else:
        print("Invalid mode")

if __name__ == '__main__':
    main()