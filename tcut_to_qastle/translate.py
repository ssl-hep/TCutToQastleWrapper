import qastle
import ast
import re


def _check_parentheses(expression): 
      
    open_tup = tuple('(') 
    close_tup = tuple(')') 
    map = dict(zip(open_tup, close_tup)) 
    queue = [] 
  
    for i in expression: 
        if i in open_tup: 
            queue.append(map[i]) 
        elif i in close_tup: 
            if not queue or i != queue.pop(): 
                # return "Unbalanced"
                raise Exception("TCut selection query has unbalanced parentheses")
    if not queue: 
        # return "Balanced"
        pass
    else: 
        # return "Unbalanced"
        raise Exception("TCut selection query has ubalanced parentheses")


def _multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 


def get_list_of_columns_in_selection(tcut_selection:str):
    
    # 1st step: recognize all variable names
    ignore_patterns = { # These are supported by Qastle
        "abs" : " ",
        "(" : " ",
        ")" : " ",
        "*" : " ",
        "/" : " ",
        "+" : " ",
        "-" : " "
    }
    remove_patterns = _multiple_replace(ignore_patterns, tcut_selection)

    remove_marks = re.sub('[<&>!=|-]',' ',remove_patterns)
    # remove_marks = re.sub(r'[\?:<&>!=|-]',' ',remove_patterns) # Add ?, : for ternary
    variables = []
    for x in remove_marks.split():
        try:
            float(x)
        except ValueError:
            variables.append(x)
    return list(dict.fromkeys(variables)) # Remove duplicates


def _decorate_columns_in_selection(tcut_selection:str):
    for x in get_list_of_columns_in_selection(tcut_selection):
        tcut_selection = re.sub(r'\b(%s)\b'%x, r'event.%s'%x, tcut_selection)
    return tcut_selection


def _replace_operators(translated_selection:str):
    replace_patterns = {
        "&&" : " and ",
        "||" : " or ",
        "!=" : " != ",
        ">=" : " >= ",
        "<=" : " <= ",
        ">" : " > ",
        "<" : " < "    
    }
    translated_selection = _multiple_replace(replace_patterns, translated_selection)
    translated_selection = " ".join(translated_selection.split()) # Remove duplicate whitespace
    return translated_selection


def _replace_boolean(tcut_selection:str, translated_selection:str):
    translated_selection = "and " + translated_selection + " and" # Prepare for search. Better idea?
    search_patterns = [('and','and'), ('and','\)'), ('\(','and'), ('or','or'), ('\(','or'), ('or','\)'), ('or','and'), ('and','or')]
    for x in get_list_of_columns_in_selection(tcut_selection):
        for pattern in search_patterns:
            pre = pattern[0].replace('\\','')
            suf = pattern[1].replace('\\','')
            if re.search(fr'{pattern[0]}\s*event.{x}\s*{pattern[1]}', translated_selection):
                translated_selection = re.sub(fr'{pattern[0]}\s*event.{x}\s*{pattern[1]}', fr'{pre} event.{x} > 0 {suf}', translated_selection)
            if re.search(fr'{pattern[0]}\s*!event.{x}\s*{pattern[1]}', translated_selection):
                translated_selection = re.sub(fr'{pattern[0]}\s*!event.{x}\s*{pattern[1]}', fr'{pattern[0]} event.{x} == 0 {pattern[1]}', translated_selection)
            if re.search(r'!\([^()]*\)', translated_selection): # Search for !(something)
                translated_selection = re.sub(r'!\([^()]*\)',re.search(r'!\([^()]*\)', translated_selection).group(0).lstrip('!') + " == 0",translated_selection)
    translated_selection = translated_selection.rsplit(' ', 1)[0].split(' ', 1)[1] # Delete `and` at the beginning and the last
    return translated_selection


def _translate_selection(tcut_selection:str):
    tcut_selection_with_event = _decorate_columns_in_selection(tcut_selection)
    tcut_selection_after_operator_replacement = _replace_operators(tcut_selection_with_event)
    selection_in_func_adl = _replace_boolean(tcut_selection, tcut_selection_after_operator_replacement)
    return selection_in_func_adl


def _translate_selected_columns(selected_columns:str): 
    passDict = True
    passList = False   
    if selected_columns.lower() == "":    
        selected_columns_text = 'event'
    else:            
        if passDict:
            selected_columns = [num.strip() for num in selected_columns.split(',')]
            selected_columns_list_text = [f'\'{i}\': event.{i}' for i in selected_columns]
            selected_columns_text = ', '.join(selected_columns_list_text)
            selected_columns_text = '{' + selected_columns_text + '}'
        elif passList:
            selected_columns = [num.strip() for num in selected_columns.split(',')]
            selected_columns_list_text = [f'event.{i}' for i in selected_columns]
            selected_columns_text = ', '.join(selected_columns_list_text)
            selected_columns_text = '(' + selected_columns_text + ')'
    return selected_columns_text


def translate(tree_name:str, selected_columns:str = "", tcut_selection:str = ""):
    _check_parentheses(tcut_selection)
    if tree_name is "":
        raise Exception("Tree name is missing")
    if tcut_selection is "":
        query = f"EventDataset(\"ServiceXDatasetSource\", \"{tree_name}\").Select(\"lambda event:  {_translate_selected_columns(selected_columns)} \")"
    else:
        query = f"EventDataset(\"ServiceXDatasetSource\", \"{tree_name}\").Where(\"lambda event: {_translate_selection(tcut_selection)} \").Select(\"lambda event: {_translate_selected_columns(selected_columns)} \")"            
    return qastle.python_ast_to_text_ast(qastle.insert_linq_nodes(ast.parse(query)))