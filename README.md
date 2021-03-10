## Introduction
[TCut](https://root.cern.ch/doc/master/classTCut.html) selection for ROOT TTree to [Qastle](https://github.com/iris-hep/qastle) wrapper for ServiceX uproot backends. 

## Supported expressions
- Arithmetic operators: `+, -, *, /`
- Logical operators: `!, &&, ||`
- Relational and comparison operators: `==, !=, >, <, >=, <=`
- Mathematical function: `sqrt`

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
- `sslhep/servicex_func_adl_uproot_transformer:develop`


## Development

<!-- ### Verbose mode -->

Verbose mode shows intermediate steps from TCut syntax to qastle. The last arguement of the function `translate()` is a flag to enable the verbose mode. It prints the input TCut selection expression, translated func-adl selection expression, full func-adl query which includes the name of tree and selected branches, and full qastle query.
```
>>> query = tcut_to_qastle.translate("tree", "A,B", "A && B * C>0", verbose=True)
TCut selection syntax:
A && B * C>0


Translated func-adl selection syntax:
 event.A > 0 and event.B * event.C > 0


Full func-adl query:
EventDataset("ServiceXDatasetSource", "tree").Where("lambda event: event.A > 0 and event.B * event.C > 0 ").Select("lambda event: {'A': event.A, 'B': event.B} ")


Full qastle query:
(Select (Where (call EventDataset 'ServiceXDatasetSource' 'tree') (lambda (list event) (and (> (attr event 'A') 0) (> (* (attr event 'B') (attr event 'C')) 0)))) (lambda (list event) (dict (list 'A' 'B') (list (attr event 'A') (attr event 'B')))))
```

<!-- ### Test your qastle query using local ROOT Flat ntuple

Generated qastle query can be tested locally using ROOT flat ntuple. The following `func-adl-uproot` package is required:

`func-adl-uproot==1.2`

```
>>> import func_adl_uproot
>>> ftn = func_adl_uproot.generate_function(query)
>>> output = ftn(<INPUT ROOT FILE>)
``` -->
