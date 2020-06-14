import qastle
import ast
import re


def _multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 


class Translate:

    def __init__(self, tcut_selection, selected_columns):
        self.tcut_selection = tcut_selection
        self.selected_columns = selected_columns
        self.list_of_columns_in_selection = []
        self._translated_selection = self.tcut_selection
        self._translated_selected_columns = ""
        self._get_list_of_columns_in_selection()
        self._translate_selection()
        self._translate_selected_columns()


    def _get_list_of_columns_in_selection(self):
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
        remove_patterns = _multiple_replace(ignore_patterns, self.tcut_selection)

        remove_marks = re.sub('[<&>!=|-]',' ',remove_patterns)
        # remove_marks = re.sub(r'[\?:<&>!=|-]',' ',remove_patterns) # Add ?, : for ternary
        variables = []
        for x in remove_marks.split():
            try:
                float(x)
            except ValueError:
                variables.append(x)
        self.list_of_columns_in_selection = list(dict.fromkeys(variables)) # Remove duplicates
        return self.list_of_columns_in_selection


    def _decorate_columns_in_selection(self):
        for x in self.list_of_columns_in_selection:
            self._translated_selection = re.sub(r'\b(%s)\b'%x, r'event.%s'%x, self._translated_selection)


    def _replace_operators(self):
        replace_patterns = {
            "&&" : " and ",
            "||" : " or ",
            "!=" : " != ",
            ">=" : " >= ",
            "<=" : " <= ",
            ">" : " > ",
            "<" : " < "    
        }
        self._translated_selection = _multiple_replace(replace_patterns, self._translated_selection)
        self._translated_selection = " ".join(self._translated_selection.split()) # Remove duplicate whitespace


    def _replace_boolean(self):
        self._translated_selection = "and " + self._translated_selection + " and" # Prepare for search. Better idea?
        search_patterns = [('and','and'), ('and','\)'), ('\(','and'), ('or','or'), ('\(','or'), ('or','\)'), ('or','and'), ('and','or')]
        for x in self._get_list_of_columns_in_selection():
            for pattern in search_patterns:
                pre = pattern[0].replace('\\','')
                suf = pattern[1].replace('\\','')
                if re.search(fr'{pattern[0]}\s*event.{x}\s*{pattern[1]}', self._translated_selection):
                    self._translated_selection = re.sub(fr'{pattern[0]}\s*event.{x}\s*{pattern[1]}', fr'{pre} event.{x} > 0 {suf}', self._translated_selection)
                if re.search(fr'{pattern[0]}\s*!event.{x}\s*{pattern[1]}', self._translated_selection):
                    self._translated_selection = re.sub(fr'{pattern[0]}\s*!event.{x}\s*{pattern[1]}', fr'{pattern[0]} event.{x} == 0 {pattern[1]}', self._translated_selection)
                if re.search(r'!\([^()]*\)', self._translated_selection): # Search for !(something)
                    self._translated_selection = re.sub(r'!\([^()]*\)',re.search(r'!\([^()]*\)', self._translated_selection).group(0).lstrip('!') + " == 0",self._translated_selection)
        self._translated_selection = self._translated_selection.rsplit(' ', 1)[0].split(' ', 1)[1] # Delete `and` at the beginning and the last


    def _translate_selection(self):
        self._decorate_columns_in_selection()
        self._replace_operators()
        self._replace_boolean()


    def _translate_selected_columns(self): 
        passDict = True
        passList = False   
        if self.selected_columns.lower() == 'all':
            selected_columns_text = 'event'
        else:            
            if passDict:
                self.selected_columns = [num.strip() for num in self.selected_columns.split(',')]
                selected_columns_list_text = [f'\'{i}\': event.{i}' for i in self.selected_columns]
                selected_columns_text = ', '.join(selected_columns_list_text)
                selected_columns_text = '{' + selected_columns_text + '}'
            elif passList:
                self.selected_columns = [num.strip() for num in self.selected_columns.split(',')]
                selected_columns_list_text = [f'event.{i}' for i in self.selected_columns]
                selected_columns_text = ', '.join(selected_columns_list_text)
                selected_columns_text = '(' + selected_columns_text + ')'
        self._translated_selected_columns = selected_columns_text


    def to_qastle(self):
        if self.tcut_selection.lower() == "none":
            query = "EventDataset().Select(\"lambda event: " + self._translated_selected_columns + "\")"
        else:
            query = "EventDataset().Where('lambda event: " + self._translated_selection + "').Select(\"lambda event: " + self._translated_selected_columns + "\")"
        # self.func_adl_query = query
        return qastle.python_ast_to_text_ast(qastle.insert_linq_nodes(ast.parse(query)))