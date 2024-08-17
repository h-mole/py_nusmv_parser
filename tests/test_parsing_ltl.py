import json
from py_nusmv_parser import parse_nusmv_string
import json


def test_parse_demo1():
    DEMO1 = """
MODULE main
VAR
    request : boolean;
    state   : {ready, busy};
ASSIGN
    init(state) := ready;
    next(state) := case
                        state = ready & request = TRUE : busy;
                        TRUE : {ready, busy}; 
                   esac;
"""
    item = parse_nusmv_string(DEMO1)
    print(json.dumps(item.to_dict(), indent=2))
    print(item.unparse())

def test_parse_demo2():
    DEMO2 = """
    MODULE main
    VAR c : boolean;
    VAR d : counter(init_value1, self);
    ASSIGN
        c := init_value;
    """
    item = parse_nusmv_string(DEMO2)
    print(json.dumps(item.to_dict(), indent=2))
    print(item.unparse())

