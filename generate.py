#!/usr/bin/python3

# A script to generate a new run, with everything needed in it own directory
import sys
import os
import json
from datetime import datetime

def trail_str(x):
    base = str(x)
    extra = 4 - len(base)
    assert extra >= 0
    return "0"*extra + base

if len(sys.argv) == 3:
    check_generate, benchmarks_relative_directory, solver = sys.argv
    optional_name_start = ""
elif len(sys.argv) == 4:
    check_generate, benchmarks_relative_directory, solver, optional_name = sys.argv
    optional_name_start = optional_name + "___"
else:
    print("usage: generate.py, benchmarks_relative_directory, solver, optional_name")
    exit(0)

if check_generate != "generate.py":
    print("ERROR, has to be run from this directory")
    exit(1)

with open("settings.json") as settings_json:
    settings = json.load(settings_json)

pwd = os.getcwd()

benchmarks_absolute_directory = pwd + "/" + benchmarks_relative_directory

datetime_string = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

hostname = settings["hostname"]

run_directory = pwd + "/runs/" + hostname + "___" + optional_name_start + datetime_string
logs_directory = run_directory + "/logs"
scripts_directory = run_directory + "/scripts"

os.mkdir(run_directory)
os.mkdir(logs_directory)
os.mkdir(scripts_directory)

solver_location = settings[solver + "_location"]
cd_line = "cd " + solver_location

#branch depending on the solver
if hostname == "gadi":
    if solver == "parallel-pdr":
        set_location = run_directory + "/set"
        os.system("cp set " + set_location)
        # this solver supports mpi parallelism, so read the settings file
        with open("set") as set_file:
            for line in set_file.readlines():
                parts = line.rstrip().split(" ")
                key = parts[0]
                if key == "dagster":
                    mpi_parallel = parts[1] == "1"
    
        if mpi_parallel:
            with open(benchmarks_absolute_directory + "/pddls_names") as pddls_names:
                unique_number = 0
                for line in pddls_names.readlines():
                    # for each of these, create a pbs run script 
                    unique_number+=1
                    unique_number_string = trail_str(unique_number)
                    relative_domain_pddl, relative_problem_pddl, domain_name, problem_name = line.rstrip().split(" ")

                    absolute_domain_pddl = benchmarks_absolute_directory + "/" + relative_domain_pddl
                    absolute_problem_pddl = benchmarks_absolute_directory + "/" + relative_problem_pddl

                    unique_name = domain_name + "___" + problem_name
                    script_location = scripts_directory + "/script___" + unique_number_string + "___" + unique_name
                    run_line = "timeout -s2 " + str(settings["timeout"] + 10) + " " + absolute_domain_pddl + " " + absolute_problem_pddl + " " + set_location + " &> " + logs_directory + "/log___" + unique_name
                    os.system("cp gadi_meta " + script_location)
                    with open(script_location, "a") as script:
                        script.write(cd_line + "\n")
                        script.write(run_line + "\n")
    
        else:
            print("don't know what to do with this...")
            exit(1)

    else:
        print("unsupported solver " + solver)
else:
    print("unknown hostname " + hostname)
