#!/usr/bin/env python

from sys import argv, stdout, stderr, stdin, exit
from getopt import *
from subprocess import Popen, PIPE
from socket import *
from re import search, finditer, MULTILINE, DOTALL
from xml.etree import cElementTree as ElementTree
from cProfile import Profile

usage = '''usage: mdpclient [options] [file ...]
options:
  -H h,  --host=h   connect to host h
  -P p,  --port=p   connect to port p
  -v n,  --verbose=n    use verbosity level n;
              n is a number from 0 (verbose mode off) and up;
  -W n,  --warnings=n   determines how warnings are treated;
              0 supresses warnings; 1 displays warnings;
              2 treats warnings as errors
  -h     --help     display this help and exit
  file ...      files containing domain and problem descriptions;
              if none, descriptions are read from standard input
         --profile  enable profiling on match tree structures'''


''' Default Options '''
host = "localhost"
port = 2323
verbosity = 0
warnings = 0
domain_filename = None
problem_filename = None
planner_name = "prob-prp"

''' Profiling Options '''
profiling = False
profiling_call_accumulator = 0
profiling_get_actions_each_call = []
profiling_get_actions_each_number_returned = []
# These are cProfile objects to time how long it takes to:
#  a. Convert state atoms into their variable indices and values
#  b. Call get_actions given the conversion
#  c. Select the optimal action from get_actions
build_state_profiler = None
get_actions_profiler = None
action_select_profiler = None

''' Option and Argument Parsing '''
try:
    opts, args = gnu_getopt(argv, "hH:P:v:W:",
                            ["help", "profile", "host=", "port=",
                             "verbose=", "warnings="])
except GetoptError, e:
    stderr.write("%s: %s\n" % (argv[0], str(e)))
    exit(1)

for opt, arg in opts:
    if (opt in ["-h", "--help"]):
        stdout.write("%s\n" % usage)
        exit(0)
    elif (opt == "--profile"):
        profiling = True
    elif (opt in ["-H", "--host"]):
        host = arg
    elif (opt in ["-P", "--port"]):
        try:
            port = int(arg)
        except ValueError, e:
            stderr.write("%s: port must be a valid integer\n" % argv[0])
            exit(1)
        if (port <= 0):
            stderr.write("%s: port must be non-negative integer\n" % argv[0])
            exit(1)
    elif (opt in ["-v", "--verbose"]):
        try:
            verbosity = int(arg)
        except ValueError, e:
            stderr.write("%s: verbosity must be a valid integer\n" % argv[0])
            exit(1)
        if (verbosity <= 0):
            stderr.write("%s: verbosity must be non-negative integer\n" %
                         argv[0])
            exit(1)
    elif (opt in ["-W", "--warnings"]):
        try:
            warnings = int(arg)
        except ValueError, e:
            stderr.write("%s: warnings must be a valid integer\n" % argv[0])
            exit(1)
        if (warnings <= 0):
            stderr.write("%s: warnings must be non-negative integer\n" %
                         argv[0])
            exit(1)
        if (warnings > 2):
            stderr.write("%s: warnings must be between 0 and 2\n" % argv[0])
            exit(1)

if (profiling):
    build_state_profiler = Profile()
    get_actions_profiler = Profile()
    action_select_profiler = Profile()

if (args[1:]):
    domain_filename = args[1]
if (args[2:]):
    problem_filename = args[2]

reading_stdin = not domain_filename is None

if (not reading_stdin and not problem_filename):
    # Problem is assumed to be specified in same file
    problem_filename = domain_filename

if (verbosity > 0):
    stdout.write("Using host %s, port %d\n" % (host, port))
    if (problem_filename):
        stdout.write("Domain: %s\nProblem: %s\n" %
                     (domain_filename, problem_filename))
    elif (domain_filename):
        stdout.write("Domain and problem: %s\n" % (domain_filename))
        problem_filename = domain_filename
    else:
        stdout.write("Reading stdin\n")
        # Create a temporary file and throw the info into it
        f_pddl = open("stdin.pddl", "w")
        if (not f_pddl):
            stderr.write("Could not create temporary pddl file \"stdin.pddl\"\n")
            exit(1)
        lines = stdin.readlines()
        f_pddl.writelines(lines)
        f_pddl.close()

        domain_filename = "stdin.pddl"
        problem_filename = "stdin.pddl"

# Read the problem file to figure out the name of the problem
problem_name = None
with open(problem_filename, "r") as f:
    problem_contents = f.read()
    re_match = search(r'\(problem ([^\)]+)\)', problem_contents)
    if (re_match):
        problem_name = re_match.group(1)
if (not problem_name):
    stderr.write("%s: Could not determine problem name from %s\n" %
                 (argv[0], problem_filename))
    exit(1)

''' Begin interacting with the server   '''
s = socket(AF_INET, SOCK_STREAM)

try:
    s.connect((host, port))
except error, e:
    stderr.write("%s: problem during connection to server:\n\t%s\n" %
                 (argv[0], str(e)))
    exit(1)

if (verbosity > 0):
    stdout.write("Connected to server\n")

def tell_server(msg):
    ''' Send the server a message '''
    if (verbosity > 4):
        stdout.write("Attempting to tell server: %s\n" % str(msg))
    try:
        s.sendall(msg)
    except error, e:
        stderr.write("%s: problem sending message:\n\t%s\n" %
                     (argv[0], str(e)))
        if (verbosity > 0):
            stderr.write("Attempted to send message: %s\n" % str(msg))

def listen_server(sz=16384):
    ''' Returns an array of XML responses from the server - Each
    line is one XML response, ready to be parsed'''
    if (verbosity > 4):
        stdout.write("Listening for %s bytes from server\n" % str(sz))
    return s.recv(sz).strip().split("\n")

buff = []
def get_next_xml_message():
    if (not buff):
        buff.extend(listen_server())
    raw_string = buff.pop(0)
    try:
        return ElementTree.fromstring(raw_string)
    except ElementTree.ParseError as e:
        stderr.write("Exception in parsing server message: %s\n" % (str(e)))
        stderr.write("Original string: %s\n" % (raw_string))

# Identify ourselves to the server
tmp_msg = "<session-request>" + \
    "<name>prob-prp</name>" + \
    "<problem>" + problem_name + "</problem>" + \
    "</session-request>"
tell_server(tmp_msg)

### ----------------------- FOR DEBUGGING --------------------------
def dump_xml_element(e, indent="", stream=stdout):
    stream.write(indent)
    if (e.tag):
        stream.write(e.tag)
    if (e.text):
        stream.write(": " + e.text)
    if (e.attrib):
        stream.write("  " + str(e.attrib))
    stream.write("\n")
    for item in e:
        dump_xml_element(item, indent + "  ")
### ----------------------------------------------------------------

xml_root = get_next_xml_message()
if (xml_root.tag != "session-init"):
    stderr.write("%s: Invalid response from session-request: %s\n" %
                 (argv[0], xml_root.tag))
    if (verbosity > 0):
        stderr.write("Details:\n")
        dump_xml_element(xml_root, "  ", stderr)
    exit(1)

session_id = int(xml_root.find('sessionID').text)
xml_root = xml_root.find('setting')
rounds = int(xml_root.find('rounds').text)
allowed_time = int(xml_root.find('allowed-time').text)
# TODO: Reading allowed turns gives weird values
allowed_turns = int(xml_root.find('allowed-turns').text)

if (verbosity > 0):
    stdout.write("Session created:\n\t"
                 "ID:%d, Rounds: %d, Time limit: %d, Turn limit: %d\n" %
                 (session_id, rounds, allowed_time, allowed_turns))

''' Invoke PRP  '''
prp_options = ["--dump-policy", "1", "--trials", "0", "--random-seed", "888", "--final-fsap-free-round", "1"]
if (allowed_time > 0):
    prp_options.extend(["--jic-limit", str(allowed_time)])
prp_process = Popen(["./src/prp", domain_filename, problem_filename] 
                    + prp_options,
                    stdout=PIPE, stderr=PIPE)
(prp_stdout_output, prp_stderr_output) = prp_process.communicate()

if (verbosity > 2):
    stdout.write("\n------------- PROB-PRP Output ---------------\n")
    stdout.write(prp_stdout_output)
    stdout.write("\n----------------------------------------\n")
    stderr.write(prp_stderr_output)
elif (verbosity > 0):
    stdout.write("prob-prp finished generating the policy\n")

if (prp_process.returncode == 0):
    policy_strong_cyclic = True
else:
    policy_strong_cyclic = False
# To use the match tree, there needs to be a mapping from atoms to variable
#  indices along with the corresponding value of that variable
# Generate this by reading the file "output" which contains these mappings
atom_to_var_value = dict()
num_var_values_dict = dict()  # Number of potential values
if (profiling):
    # Need to build variables -> atoms to dump useful information
    var_value_to_atom = dict()

with open('output', 'r') as f:
    for (i, match) in enumerate(finditer(r'begin_variable(.*?)end_variable',
                                f.read(),
                                MULTILINE | DOTALL)):
        lines = match.group(1).strip().split("\n")

        assert "-1" == lines[1], \
            "Expected variable %s to be followed by -1" % (lines[0])

        # var_index = int(lines[0][3:]) # Apparently this doesn't match
                                        # up with the policy var indices
        var_index = i                   # So this line makes it explicit

        num_var_values_dict[var_index] = int(lines[2])

        for var_value, raw_atom in enumerate(lines[3:]):
            if (raw_atom.startswith("Atom ")):
                # Note the format of raw_atom: "predicate(term1, term2, ...)""
                atom_to_var_value[(raw_atom[5:])] = [var_index, var_value]
            # The <none of these> case doesn't matter for traversing the tree
            if (profiling):
                var_value_to_atom[(var_index, var_value)] = raw_atom

# Convert num_var_values_dict to a list indexed by the variable index
num_vars = max(num_var_values_dict.keys())+1
num_var_values = []
for i in range(num_vars):
    if i in num_var_values_dict.keys():
        num_var_values.append(num_var_values_dict[i])
    else:
        num_var_values.append(0)

''' Figure out the policy '''

# Create the match tree now
class MatchTreeNode:
    def __init__(self, var_index=-1, num_values=-1):
        self.bucket = []    # A list of [actions, SC?, distance]
        self.var_index = var_index
        if (var_index >= 0):
            self.value_nodes = [None for i in range(num_values)]
        self.star_node = None
        if (profiling):
            self.traversals = 0

    def get_actions(self, var_values):
        if (profiling):
            global profiling_call_accumulator
            self.traversals += 1
            profiling_call_accumulator += 1

        ret = self.bucket[:]    # make a copy
        # var_index may be -1, indicating this is a star node
        if (self.var_index >= 0):
            ret += self.value_nodes[var_values[self.var_index]]\
                .get_actions(var_values)
        if (self.star_node):
            ret += self.star_node.get_actions(var_values)
        return ret

    def get_frequently_accessed_children(self):
        if (not profiling):
            raise Exception("Need to be in profiling mode to use this")
        children = []
        if (self.var_index >= 0):
            for (i, child_node) in enumerate(self.value_nodes):
                children.append((child_node, i, child_node.traversals))
        # The star node always has the same traversasls as this node
        return sorted(children, key=lambda k: k[2], reverse=True)

    def _recursive_str(self, indent=""):
        ret = ""
        if (self.var_index >= 0):
            ret += indent + "Node var" + str(self.var_index) + ":\n"
            indent += "  "
        if (profiling):
            ret += indent + "Traversals: " + str(self.traversals) + "\n"
        ret += indent + "Bucket: " + str(self.bucket)
        if (self.var_index >= 0):
            for (i, subnode) in enumerate(self.value_nodes):
                ret += "\n" + indent + "Value " + \
                    str(i+1) + ":\n" + subnode._recursive_str(indent + "  ")
        ret += "\n" + indent + "Star:\n"

        if (self.star_node):
            ret += self.star_node._recursive_str(indent + "  ")
        else:
            ret += indent + "  None"

        return ret

    def __str__(self):
        return self._recursive_str()

# Helper function for gen_match_tree
def gen_bucket_from_check(lines):
    line = lines.pop(0)
    assert line.startswith("check"), \
        "Error in building match tree: Expected \"check\", got %s" % line
    num_items = int(line[6:])
    ret_bucket = []  # List of (action, SC?, d) tuples
    for j in range(num_items):
        line = lines.pop(0)

        # The line is currently in the form "action / SC? / d=distance"
        raw_atom, raw_sc, raw_distance = line.split(" / ")

        if (raw_sc == "SC"):
            is_sc = True
        else:
            is_sc = False

        distance = int(raw_distance.split("=")[1].strip())

        ret_bucket.append((raw_atom, is_sc, distance))

    return ret_bucket

# Creates the match tree recursively
def gen_match_tree(lines):  # Lines must be popped for recursion!
    line = lines.pop(0)
    assert line.startswith("switch"), \
        "Error in building match tree: Expected \"switch\", got %s" % line
    var_index = int(line[7:])
    num_values = num_var_values[var_index]

    ret = MatchTreeNode(var_index, num_values)

    # First read the default bucket
    ret.bucket = gen_bucket_from_check(lines)

    # Now read the node for each value
    for i in range(num_values):
        if (lines[0].startswith("switch")):
            # Recursively build the next match tree
            ret.value_nodes[i] = gen_match_tree(lines)
            continue

        # If it's not another switch, it's expected to be a check
        ret_matchtree_child = MatchTreeNode()
        ret_matchtree_child.bucket = gen_bucket_from_check(lines)

        ret.value_nodes[i] = ret_matchtree_child

    # Lastly, read the star node
    if (lines[0].startswith("switch")):
        ret.star_node = gen_match_tree(lines)
    else:
        ret_matchtree_child = MatchTreeNode()
        ret_matchtree_child.bucket = gen_bucket_from_check(lines)

        ret.star_node = ret_matchtree_child

    return ret

# Build the policy from the policy file produced by PRP
policy = None
with open('policy.out', 'r') as f:
    policy = gen_match_tree(f.readlines())

de_policy = None
with open('policy.out.de', 'r') as f:
    de_policy = gen_match_tree(f.readlines())

if (not policy) or (not de_policy):
    stderr.write("%s: Error in building policy\n" % (argv[0]))
    exit(1)

if (verbosity > 3):
    stdout.write("\n-----------Policy Match Tree------------\n")
    stdout.write(str(policy))
    stdout.write("\n----------------------------------------\n")

''' Begin Simulation '''
for round in range(1, rounds+1):
    if (verbosity > 1):
        stdout.write("Starting round %d\n" % round)

    tell_server("<round-request/>")

    xml_root = get_next_xml_message()

    # Validate round information
    if (xml_root.tag != "round-init"):
        stderr.write("%s: Invalid response from round-request: %s\n" %
                     (argv[0], xml_root.tag))
        if (verbosity > 0):
            stderr.write("Details:\n")
            dump_xml_element(xml_root, "  ", stderr)
        exit(1)
    assert int(xml_root.find('sessionID').text) == session_id,\
        "Server supplied sessionID must match our sessionID"
    assert int(xml_root.find('round').text) == round,\
        "Server supplied round must match our current round"

    # Simulate round
    turns_used = 0
    while (True):
        xml_root = get_next_xml_message()
        if (profiling):
            build_state_profiler.enable()

        # Check if the round is over
        if (xml_root.tag == "end-round"):
            assert int(xml_root.find('sessionID').text) == session_id,\
                "Server supplied sessionID must match our sessionID"
            assert int(xml_root.find('round').text) == round,\
                "Server supplied round must match our current round"
            if (verbosity > 1):
                stdout.write("End of round %d" % round)
            if (xml_root.find("goal-reached") is not None):
                if (verbosity > 2):
                    stdout.write(" (Successful)")
            elif (turns_used >= allowed_turns):
                if (verbosity > 2):
                    stdout.write(" (Ran out of turns)")
            if (verbosity > 1):
                stdout.write("\n")
            break

        # Validate state information
        if (xml_root.tag != "state"):
            stderr.write("%s: Invalid state response: %s\n" %
                         (argv[0], xml_root.tag))
            if (verbosity > 0):
                stderr.write("Details:\n")
                dump_xml_element(xml_root, "  ", stderr)
            exit(1)

        if (verbosity > 3):
            stdout.write("Current state information:\n")
            dump_xml_element(xml_root, "  ")

        # Build state information
        #  default is <none of these> for all variables
        state_variables = [num_var_values[i] - 1 for i in range(num_vars)]
        for state_item in xml_root:
            assert state_item.tag == 'atom',\
                "Cannot handle non-atom state items yet (got %s)" % \
                (state_item.tag)
            current_atom = state_item.find('predicate').text + "(" + \
                ", ".join([t.text for t in state_item.findall('term')]) + ")"
            assert current_atom in atom_to_var_value,\
                "SAS+ variable for %s unknown" % current_atom
            var_index, var_value = atom_to_var_value[current_atom]
            state_variables[var_index] = var_value

        if (profiling):
            build_state_profiler.disable()

        if (verbosity > 3):
            stdout.write("Current state variables:\n")
            for (i, sv) in enumerate(state_variables):
                stdout.write("\tvar%d: %d\n" % (i, sv))

        if (profiling):
            profiling_call_accumulator = 0
            get_actions_profiler.enable()

        action = None
        actions_to_consider = policy.get_actions(state_variables)
        actions_to_avoid = de_policy.get_actions(state_variables)
        actions_valid = [a for a in actions_to_consider if a[0] not in map(lambda x: x[0], actions_to_avoid)]

        # if no valid actions, still return one even if needs to be avoided
        if len(actions_valid) == 0:
            actions_valid = actions_to_consider
        
        if (profiling):
            get_actions_profiler.disable()
            profiling_get_actions_each_call.append(profiling_call_accumulator)
            profiling_get_actions_each_number_returned\
                .append(len(actions_valid))

        if (verbosity > 3):
            stdout.write("Actions generated by match tree:\n")
            for a in actions_to_consider:
                split_a = a[0].split(" ")
                stdout.write("\t%s / " %
                             (split_a[0] + "(" + ", ".join(split_a[1:]) + ")"))
                if (a[1]):
                    stdout.write("SC")
                else:
                    stdout.write("NSC")
                stdout.write(" / d=%d\n" % (a[2]))

        # First sort all the SC actions based on distance
        if (profiling):
            action_select_profiler.enable()
        SC_actions = sorted([a for a in actions_valid if a[1]],
                            key=lambda k: k[2])
        if (SC_actions):
            # If an SC action exists, this is the one with the
            # minimum distance-to-goal
            action = SC_actions[0][0]
        else:
            # No SC actions available, so just pick the
            # minimum distance-to-goal
            sorted_actions = sorted(actions_valid, key=lambda k: k[2])
            if sorted_actions:
                action = sorted_actions[0][0]

        if (profiling):
            action_select_profiler.disable()
        if (action is None):
            if (policy_strong_cyclic):
                # This shouldn't happen with strong cyclic... so error
                stderr.write("%s: Strong cyclic policy did not provide "
                             "action for supplied state\n" % argv[0])
                stderr.write("Policy: \n%s\nPredicates: %s\n" %
                             (str_policy("  "), ", ".join([str(t) for
                              t in state_predicate_terms])))
                tell_server("<done/>")
                exit(1)
            else:
                if (verbosity > 3):
                    stdout.write("No action available for this state\n\n")
                tell_server("<done/>")
                continue

        # Got the action, now send it
        if (action == 'goal'):
            # Note: The control flow never reaches here in the current
            #       server implementation
            if (verbosity > 3):
                stdout.write("Achieved the goal!\n\n")
            tell_server("<done/>")
            continue
        elif (turns_used >= allowed_turns):
            if (verbosity > 3):
                stdout.write("Ran out of turns\n\n")
            tell_server("<done/>")
            continue

        actions = action.split()

        if (verbosity > 3):
            stdout.write("Perform action: %s\n\n" % (actions[0] + "(" +
                         ", ".join(actions[1:]) + ")"))

        tmp_msg = "<act><action><name>" + \
            actions[0] + "</name>"
        for term in actions[1:]:
            tmp_msg += "<term>" + term + "</term>"
        tmp_msg += "</action></act>"

        tell_server(tmp_msg)
        turns_used += 1

xml_root = get_next_xml_message()

simulator_successes = 0
simulator_failures = 0
metric_average = 0
time_average = 0
turn_average = 0

if (xml_root.tag == "end-session"):
    assert int(xml_root.find('sessionID').text) == session_id, \
        "Server supplied sessionID must match our sessionID"
    assert int(xml_root.find('rounds').text) == rounds, \
        "Server supplied rounds must match our rounds"
    metric_average = xml_root.find('metric-average').text

    xml_root = xml_root.find('goals')

    simulator_failures = int(xml_root.find('failed').text)

    xml_root = xml_root.find('reached')

    simulator_successes = int(xml_root.find('successes').text)

    if (simulator_successes > 0):
        time_average = xml_root.find('time-average').text
        turn_average = xml_root.find('turn-average').text

if (verbosity > 0):
    stdout.write("Finished simulation\n\t"
                 "Metric: %s\t(Successes: %d, Failures: %d)\n" %
                 (metric_average, simulator_successes, simulator_failures))
    if (simulator_successes > 0):
        stdout.write("\tTime average: %s, Turn average: %s\n" %
                     (time_average, turn_average))

if (profiling):
    average_calls = sum(profiling_get_actions_each_call) / \
        float(len(profiling_get_actions_each_call))
    average_len_reg = sum(profiling_get_actions_each_number_returned) / \
        float(len(profiling_get_actions_each_number_returned))
    total_planning_phases = len(profiling_get_actions_each_call)
    most_frequent_chain = []
    root_node = policy
    while (not root_node is None):
        children = root_node.get_frequently_accessed_children()
        if (len(children) > 0):
            most_frequent_chain.append(children[0])
            root_node = children[0][0]
        else:
            root_node = None

    stdout.write("\n---------------Profiling----------------\n")
    stdout.write("Profiler information:\n")
    stdout.write("State building profiler:\n")
    build_state_profiler.print_stats()
    stdout.write("Get actions profiler:\n")
    get_actions_profiler.print_stats()
    stdout.write("Action selection profiler:\n")
    action_select_profiler.print_stats()
    stdout.write("Average number of calls to get_action "
                 "per planning step: %.2f\n" % (average_calls))
    stdout.write("Average number of regressions returned "
                 "per planning step: %.2f\n" % (average_len_reg))
    stdout.write("Total number of planning phases: %d\n" %
                 (total_planning_phases))
    stdout.write("Trace of most frequently traversed path:\n")
    root_node = policy
    for node_tuple in most_frequent_chain:
        var_index = root_node.var_index
        var_value = node_tuple[1]
        condition_string = "If var %d = %s" % (var_index, str(var_value))
        condition_string += " (%s)" % (var_value_to_atom[(var_index, var_value)])
        stdout.write("%s\n" % (condition_string))
        root_node = node_tuple[0]
    stdout.write("Traversals on this path: %d\n" % (root_node.traversals))
    stdout.write("Traversals for all calls to get_action:\n")
    stdout.write("%s\n" % (str(profiling_get_actions_each_call)))
    stdout.write("Number of regressions returned per planning step:\n")
    stdout.write("%s\n" % (str(profiling_get_actions_each_number_returned)))
    stdout.write("----------------------------------------\n")
