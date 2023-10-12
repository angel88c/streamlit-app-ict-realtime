
#from batch_object import Batch
#from test_object import Test
#from btest_object import BTest
import re

FILE = r"./Logs/1-210122135745I30704CE9251D9W1"

def get_factor(test):
    global name
    value = ""
    sfactor = ""
    rfactor = 0.0
    
    vaue = test["nominal"]
    try:
        real_value = float(value)
        if real_value >= 1E+06 and real_value < 1E+09: 
            sfactor = "M"; 
            rfactor = 1E-06
        elif real_value >= 1E+03 and real_value < 1E+06: 
            sfactor = "K"; 
            rfactor = 1E-03
        elif real_value >= 1E+00 and real_value < 1E+03: 
            sfactor = "";  
            rfactor = 1E+00
        elif real_value >= 1E-03 and real_value < 1E+03: 
            sfactor = "m"; 
            rfactor = 1E+03
        elif real_value >= 1E-06 and real_value < 1E+03: 
            sfactor = "u";  
            rfactor = 1E+06
        elif real_value >= 1E-09 and real_value < 1E+03: 
            sfactor = "n";  
            rfactor = 1E+09
        elif real_value >= 1E-12 and real_value < 1E+03:
            sfactor = "p";  
            rfactor = 1E+12
        elif real_value < 1E-12 and real_value > 0: 
            sfactor = "p";  
            rfactor = 1E+12
        else:
            sfactor = ""
            rfactor = 1.0
                
    except Exception as e:
        msg =  e
        sfactor = ""
        return test
    
    test["units"]       = rfactor + test["units"]
    test["measurement"] = rfactor * test["measurement"]
    test["nominal"]     = rfactor * test["nominal"]
    test["high_limit"]  = rfactor * test["high_limit"]
    test["low_limit"]   = rfactor * test["low_limit"]
    
    return test

def get_test_data(ln, type):
    pv = []
    PMEAS = 2
    PNOMINAL = 3
    PHLIMIT = 4
    PLLIMIT = 5
    is_open_test = False
    
    test = {}
    test["measurement"] = 0.0
    test["nominal"] = 0.0
    test["high_limit"] = 0.0
    test["low_limit"] = 0.0
    test["status"] = 1
    test["units"] = ""
    
    if "@LIM2" in ln:
        ln = ln.replace("@LIM2", "")
        pv = ln.split('|')
        
        if len(pv) == 6: 
            test["name"] = f'{name}%{pv[3]}'
        else:
            test["name"] = name
            PHLIMIT = 3
            PLLIMIT = 4
        
        is_open_test = True if "E+99" in pv[PHLIMIT] else False
        
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"]  = float(pv[PHLIMIT])
        test["low_limit"]   = float(pv[PLLIMIT])
        test["nominal"]     = (test["high_limit"] + test["low_limit"]) / 2 
        if is_open_test:
            test["high_limit"]  = 999999999
        
        test["status"] = int(pv[1])
        
    elif "@LIM3" in ln:
        ln = ln.replace("@LIM3", "")
        pv = ln.split("|")
        
        if len(pv) == 7:
            test["name"] = f'{name}%{pv[3]}'
            PNOMINAL = 4
            PHLIMIT = 5
            PLLIMIT = 6
        else:
            test["name"] = name
            PNOMINAL = 3
            PHLIMIT = 4
            PLLIMIT = 5
            
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = float(pv[PHLIMIT])
        test["low_limit"] = float(pv[PLLIMIT])
        test["nominal"] = float(pv[PNOMINAL])
        test["status"] = int(pv[1])
        
    elif "@TJET" in ln:
        PMEAS = 1
        pv = ln.split("|")
        test["name"] = f'{name}%{pv[3]}'
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = 0.0
        test["low_limit"] = 0.0
        test["nominal"] = 0.0
        test["status"] = int(pv[PMEAS])
        
    elif "@PCHK" in ln:
        PMEAS = 1
        test["name"] = f'{name}%{pv[2]}'
        test["name"] = pv[5]
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = 0.0
        test["low_limit"] = 0.0
        test["nominal"] = 0.0
        test["status"] = int(pv[PMEAS])
        
    elif "@D-T" in ln:
        PMEAS = 1
        pv = ln.split("|")
        test["name"] = pv[5]
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = 0.0
        test["low_limit"] = 0.0
        test["nominal"] = 0.0
        test["status"] = int(pv[PMEAS])
        
    elif "@TS|" in ln:
        PMEAS = 1
        pv = ln.split("|")
        test["name"] = pv[5]
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = 0.0
        test["low_limit"] = 0.0
        test["nominal"] = 0.0
        test["status"] = int(pv[PMEAS])
        
    elif "@PF" in ln:
        PMEAS = 2
        pv = ln.split("|")
        test["name"] = pv[1]
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = 0.0
        test["low_limit"] = 0.0
        test["nominal"] = 0.0
        test["status"] = int(pv[PMEAS])
        
    else:
        pv = ln.split("|")
        
        test["name"] = f'{name}%{pv[3]}' if len(pv) == 4 else name
        
        test["measurement"] = float(pv[PMEAS])
        test["high_limit"] = -1.0
        test["low_limit"] = -1.0
        test["nominal"] = -1.0
        test["status"] = int(pv[1])

    test["type"] =  type.upper()
    return test

def read_batches(file_name: str):
    global name
    batches = []
    actual_line = ''
    try:
        #print('processing ' + file_name)
        with open(file_name, mode="r") as file:
            lines = file.readlines()
        
        name    = ""
        tr      = {}
        batch   = {}
        for line in lines:
        
            #print(line)
            actual_line = line
            line = re.sub(r"{|}", "", line)
            
            if line.strip() == "":    
                continue
        
            pv = line.split('|')
            
            if "@BATCH" in pv[0]:
                batch = {
                    "uut_type" : pv[1],
                    "uut_type_rev" : pv[2],
                    "fixture_id" : int(pv[3]),
                    "testhead_number" : int(pv[4]),
                    "testhead_type" : pv[5],
                    "process_step" : pv[6],
                    "id" : pv[7],
                    "operator_id" : pv[8],
                    "controller" : pv[9],
                    "testplan_id" : pv[10],
                    "testplan_rev" : pv[11],
                    "parent_panel_type" : pv[12],
                    "parent_panel_type_rev" : pv[13],
                    "version_label" : pv[14],
                    "board_records" : []
                }
                batches.append(batch)
            if "@BTEST" in pv[0]:
                board = {
                    "id": pv[1],
                    "test_status": pv[2],
                    "start_time": pv[3],
                    "duration": pv[4],
                    "is_multiple_test": (pv[5] == "1"),
                    "log_level": pv[6],
                    "log_set": 0,
                    "is_learning_on": (pv[8] == "1"),
                    "is_known_good": (pv[9] == "1"),
                    "end_time": pv[11],
                    "status_qualifier": pv[11],
                    "number": int(pv[12]),
                    "parent_panel": 0, 
                    "tests": []
                }
                if len(pv) > 13:
                    board["parent_panel"] = pv[13]
                
                batch["board_records"].append(board)
                batch["board_records"][-1]["tests"] = []
                
            elif "@BLOCK" in  pv[0]:
                name = pv[1]

            elif "@A-RES" in pv[0]:
                tr = get_test_data(line, "RESISTOR")
                tr["units"] = tr["units"] + "Ohms"
                batch["board_records"][-1]["tests"].append(tr)
                
            elif "@A-JUM" in pv[0]:
                tr = get_test_data(line, "JUMPER")
                tr["units"] = tr["units"] + "Ohms"
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@A-CAP" in pv[0]:
                tr = get_test_data(line, "CAPACITOR")
                tr["units"] = tr["units"] + "F"
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@A-IND" in pv[0]:
                tr = get_test_data(line, "CAPACITOR")
                tr["units"] = tr["units"] + "H"
                batch["board_records"][-1]["tests"].append(tr)
                
            elif "@A-DIO" in pv[0]:
                tr = get_test_data(line, "DIODE")
                tr["units"] = tr["units"] + "V"
                batch["board_records"][-1]["tests"].append(tr)
                
            elif "@A-MEA" in pv[0]:
                tr = get_test_data(line, "MEASUREMENT")
                tr["units"] = tr["units"] + ""
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@A-ZEN" in pv[0]:
                tr = get_test_data(line, "ZENER")
                tr["units"] = tr["units"] + "V"
                batch["board_records"][-1]["tests"].append(tr)  
        
            elif "@D-T" in pv[0]:
                tr = get_test_data(line, "DIGITAL")
                tr["units"] = tr["units"] + "V"
                batch["board_records"][-1]["tests"].append(tr)
                        
            elif "@TJET" in pv[0]:
                tr = get_test_data(line, "TESTJET")
                tr["units"] = tr["units"] + "V"
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@TS" in pv[0]:
                tr = get_test_data(line, "SHORTS")
                tr["units"] = tr["units"] + ""
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@PF" in pv[0]:
                tr = get_test_data(line, "PINS")
                tr["units"] = tr["units"] + ""
                batch["board_records"][-1]["tests"].append(tr)
            
            elif "@PCHK" in pv[0]:
                tr = get_test_data(line, "POLARITY")
                tr["units"] = tr["units"] + ""
                batch["board_records"][-1]["tests"].append(tr)
                
        return batches
    except Exception as e:
        print("Error reading file " + e)
        print("Line: "+ actual_line)
        return {}

def read_tests_by_component(file_name: str):
    objects = {}
    components = []
    
    try:
        batches = read_batches(file_name)
        all_tests = batches[-1]["board_records"][-1]["tests"]

        for test in all_tests:
            if not test["name"] in components:
                components.append(test["name"])
        
        for test in all_tests:
            if not test["name"] in objects.keys():
                objects[test["name"]] = []
            
            objects[test["name"]].append(test)
        
        return objects
    except Exception as e:
        print("Error reading file." + e)
        return {}

def get_btests(file_name: str):
    
    btests = []
    batches = read_batches(file_name)
    for batch in batches:
        btests.append(batch["board_records"])
    
    return btests

def get_all_tests(file_name: str):
    tests = []
    batches = read_batches(file_name)
    for batch in batches:
        for btest in batch["board_records"]:
            tests.extend(btest["tests"])

    return tests

def get_measurements_by_component(file_name):
    
    measurements = {}
    print(measurements.keys())
    
    tests = get_all_tests(file_name)
    
    for test in tests:
        if not test["name"] in measurements.keys():
            measurements[test["name"]] = []
        measurements[test["name"]].append(test["measurement"])

    return measurements