#!/usr/bin/python3

# take a run directory, and produce a report of times
import sys
import os
import json
from datetime import datetime

run_directory = sys.argv[1]

script_dname_pname = []

def get_script_result(dname, pname):
    errors = set()
    outputs = set()

    # process error file
    with open(run_directory + "/scripts/" + dname_pname_to_script_error_file[(dname, pname)]) as f:
        lines = [x.rstrip() for x in f.readlines()]
        if len(lines):
            # work out the errors
            # TODO address them as the come up
            print("error lines on: " + run_directory + "/scripts/" + dname_pname_to_script_output_file[(dname, pname)])

    # process output file
    with open(run_directory + "/scripts/" + dname_pname_to_script_output_file[(dname, pname)]) as f:
        lines = [x.rstrip() for x in f.readlines()]
        extra_lines = lines[13:]
        if len(extra_lines):
            print("extra lines on: " + run_directory + "/scripts/" + dname_pname_to_script_output_file[(dname, pname)])
        
    return "SUCCESS"
        
def get_log_result(dname, pname):
    result = {}
    with open(run_directory + "/logs/log___" + dname + "___" + pname) as f:
        lines = [x.rstrip() for x in f.readlines()]
        for line in lines:
            if "SAT" in line:
                assert "SAT" not in result
                result["sat"] = True
            if "real " in line:
                assert "total_time" not in result
                result["total_time"] = float(line[5:])
    return result

dname_pname_to_script_error_file = {}
dname_pname_to_script_output_file = {}
dname_pname_to_script_file = {}
dname_pnames = set()

# first find all the scripts and their output files
for filename in os.listdir(run_directory + "/scripts"):
    _, _, dname, pname = filename.split(".")[0].split("___")
    dp = (dname, pname)
    dname_pnames.add(dp)

    if ".e" in filename:
        assert dp not in dname_pname_to_script_error_file.keys()
        dname_pname_to_script_error_file[dp] = filename
    elif ".o" in filename:
        assert dp not in dname_pname_to_script_output_file.keys()
        dname_pname_to_script_output_file[dp] = filename
    else:
        assert dp not in dname_pname_to_script_file.keys()
        dname_pname_to_script_file[dp] = filename

# Then for everything that should have run, work out what happened
dname_pname_to_time = {}
for dname, pname in dname_pnames:
    script_result = get_script_result(dname, pname)
    log_result = get_log_result(dname, pname)
    dname_pname_to_time[(dname, pname)] = log_result["total_time"]

# now that we have the raw data, lets present it nicely
os.mkdir(run_directory + "/reports")
with open(run_directory + "/reports/times.csv", "w") as times_csv:
    for dname, pname in sorted(dname_pname_to_time.keys()):
        times_csv.write(dname + ", " + pname + ", " + str(dnam_pname_to_time) + "\n")
