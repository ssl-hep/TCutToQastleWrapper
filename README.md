## Introduction
[TCut](https://root.cern.ch/doc/master/classTCut.html) selection for ROOT TTree to [Qastle](https://github.com/iris-hep/qastle) wrapper for ServiceX xAOD and Uproot transformer.

## Supported operations
- Arithmetic operators: `+, -, *, /`
- Logical operators: `!, &&, ||`
- Relational and comparison operators: `==, !=, >, <, >=, <=`

## Usage

```
import tcut_to_qastle

# Load
tq = tcut_to_qastle.Translate(<TCut selection>, <Columns to deliver>)

# Get Qastle query
query = tq.to_qastle() 

# Get the list of columns in the TCut selection
columns_in_selection = tq.list_of_columns_in_selection
```

## Example

```
>>> import tcut_to_qastle
>>> tq = tcut_to_qastle.Translate("A && B * C>0", "A,B")
>>> tq.to_qastle()
"(Select (Where (call EventDataset) (lambda (list event) (and (> (attr event 'A') 0) (> (* (attr event 'B') (attr event 'C')) 0)))) (lambda (list event) (dict (list 'A' 'B') (list (attr event 'A') (attr event 'B')))))"
>>> tq.list_of_columns_in_selection
['A', 'B', 'C']
```