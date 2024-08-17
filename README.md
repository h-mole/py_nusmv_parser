# PyNuSMVParser

A parser & unparser for NuSMV model

## Installation

(Will be deployed to pypi soon...)

```cmd
python -m pip install py_nusmv_parser
```

## Packup

```python
pip wheel --wheel-dir ./dist .
```

## Usage

```python
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
```

output:

```json
{
  "_cls": "Module",
  "name": {
    "_cls": "Identifier",
    "name": "main"
  },
  "body": [
    {
      "_cls": "VarDeclaration",
      "var_list": [
        {
          "_cls": "VarDeclItem",
          "identifier": {
            "_cls": "Identifier",
            "name": "request"
          },
          "type_specifier": {
            "_cls": "BooleanType"
          }
        },
        {
          "_cls": "VarDeclItem",
          "identifier": {
            "_cls": "Identifier",
            "name": "state"
          },
          "type_specifier": {
            "_cls": "EnumerationType",
            "body": [
              {
                "_cls": "EnumerationTypeValue",
                "identifier": {
                  "_cls": "Const",
                  "value": "ready",
                  "type": "symbolic"
                }
              },
              {
                "_cls": "EnumerationTypeValue",
                "identifier": {
                  "_cls": "Const",
                  "value": "busy",
                  "type": "symbolic"
                }
              }
            ]
          }
        }
      ]
    },
    {
      "_cls": "AssignConstraint",
      "assigns_list": [
        {
          "_cls": "Assign",
          "target": {
            "_cls": "Identifier",
            "name": "state"
          },
          "expr": {
            "_cls": "Identifier",
            "name": "ready"
          },
          "modifier": "init"
        },
        {
          "_cls": "Assign",
          "target": {
            "_cls": "Identifier",
            "name": "state"
          },
          "expr": {
            "_cls": "CaseExpr",
            "case_body": [
              {
                "_cls": "CaseBodyItem",
                "condition": {
                  "_cls": "BinaryOperator",
                  "left": {
                    "_cls": "BinaryOperator",
                    "left": {
                      "_cls": "Identifier",
                      "name": "state"
                    },
                    "operator": "=",
                    "right": {
                      "_cls": "Identifier",
                      "name": "ready"
                    }
                  },
                  "operator": "&",
                  "right": {
                    "_cls": "BinaryOperator",
                    "left": {
                      "_cls": "Identifier",
                      "name": "request"
                    },
                    "operator": "=",
                    "right": {
                      "_cls": "Const",
                      "value": true,
                      "type": "boolean"
                    }
                  }
                },
                "expr": {
                  "_cls": "Identifier",
                  "name": "busy"
                }
              },
              {
                "_cls": "CaseBodyItem",
                "condition": {
                  "_cls": "Const",
                  "value": true,
                  "type": "boolean"
                },
                "expr": {
                  "_cls": "SetExpr",
                  "set_body": [
                    {
                      "_cls": "Identifier",
                      "name": "ready"
                    },
                    {
                      "_cls": "Identifier",
                      "name": "busy"
                    }
                  ]
                }
              }
            ]
          },
          "modifier": "next"
        }
      ]
    }
  ]
}
```

```python
print(item.unparse())
```

output:

```smv
MODULE main

VAR
    request : boolean ;
    state : {ready, busy} ;

ASSIGN
    init(state) := ready;
    next(state) :=
    case
        state = ready & request = TRUE : busy ;
        TRUE : {ready, busy} ;
    esac
    ;
```

## Development

```cmd
pip install autoflake black isort pytest
pytest -s
pip install build
python3 -m build
```
