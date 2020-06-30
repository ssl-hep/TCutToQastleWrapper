## Introduction
[TCut](https://root.cern.ch/doc/master/classTCut.html) selection for ROOT TTree to [Qastle](https://github.com/iris-hep/qastle) wrapper for ServiceX xAOD and Uproot transformer.

## Supported operations
- Arithmetic operators: `+, -, *, /`
- Logical operators: `!, &&, ||`
- Relational and comparison operators: `==, !=, >, <, >=, <=`

## Usage

```
import tcut_to_qastle


# Get Qastle query
query = tcut_to_qastle.translate(<TCut selection>, <Columns to deliver>)

# Get the list of columns in the TCut selection
columns_in_selection = tcut_to_qastle.get_list_of_columns_in_selection(<TCut selection>)
```

## Example

```
>>> import tcut_to_qastle
>>> query = tcut_to_qastle.translate("A && B * C>0", "A,B")
>>> query
"(Select (Where (call EventDataset) (lambda (list event) (and (> (attr event 'A') 0) (> (* (attr event 'B') (attr event 'C')) 0)))) (lambda (list event) (dict (list 'A' 'B') (list (attr event 'A') (attr event 'B')))))"
>>> columns_in_selection = tcut_to_qastle.get_list_of_columns_in_selection("A && B * C>0")
>>> columns_in_selection
['A', 'B', 'C']
```