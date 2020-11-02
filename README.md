## Introduction
[TCut](https://root.cern.ch/doc/master/classTCut.html) selection for ROOT TTree to [Qastle](https://github.com/iris-hep/qastle) wrapper for ServiceX uproot backends. 

## Supported operations
- Arithmetic operators: `+, -, *, /`
- Logical operators: `!, &&, ||`
- Relational and comparison operators: `==, !=, >, <, >=, <=`

## Usage

- `<tree_name>`: Tree name of input flat ROOT ntuple (required only for uproot)
- `<selected_columns>`: List of selected branches (or columns) to deliver. Branches are separated by comma. Deliver all branches if nothing specified.
- `<tcut_selection>`: Selection expression with a combination of the branches. No selection is applied if nothing specified.

```
import tcut_to_qastle

# Get Qastle query
query = tcut_to_qastle.translate(<tree_name>, <selected_columns>, <tcut_selection>)

# Get the list of columns in the TCut selection
columns_in_selection = tcut_to_qastle.get_list_of_columns_in_selection(<TCut selection>)
```

## Example

```
>>> import tcut_to_qastle
>>> query = tcut_to_qastle.translate("tree", "A,B", "A && B * C>0")
>>> query
"(Select (Where (call EventDataset 'ServiceXDatasetSource' 'tree') (lambda (list event) (and (> (attr event 'A') 0) (> (* (attr event 'B') (attr event 'C')) 0)))) (lambda (list event) (dict (list 'A' 'B') (list (attr event 'A') (attr event 'B')))))"
>>> columns_in_selection = tcut_to_qastle.get_list_of_columns_in_selection("A && B * C>0")
>>> columns_in_selection
['A', 'B', 'C']
```

## Compatibility
Current version is compatible with the following docker image tag of the uproot transformer
- `sslhep/servicex_func_adl_uproot_transformer:v1.0.0-rc.3`