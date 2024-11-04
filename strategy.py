import pandas as pd
def renaming_id(df, id, value):
    """Function that renames rows ID for granting unique name accordingly to the specified format."""
    #Coger el máximo número en ID y añadirlo a _.
    print(value)
    max = df[id].max()
    print(max)

    def update_id():
        nonlocal max
        max += 1
        return max

    filtered_df = df[df[id] == value]

    df.loc[filtered_df.index[1:], id] = filtered_df[id].iloc[1:].apply(lambda x: update_id())
    

def delete_duplicates(df, id, value):
    """Function that deletes duplicates that are all the same."""
    
    to_remove = df[df[id] == value].index

    df.drop(to_remove[1:], inplace=True)


def null_assign(column: str, id_column:str, data: dict, parser: dict, support:dict, df: dict) -> dict:
    """Function that implements the assignation of null values"""
    null_elems = data[column].isnull().values.tolist()
    for i in range(len(null_elems)):
        if null_elems[i]:
            #print("null item in position ", i+1)
            assigned = False
            for domain in parser:
                if not assigned:
                    for elem in parser[domain]:
                        candidates = pd.DataFrame()

                        if elem in data:
                            # CASO 1: el dataset origen y destino comparten columna de búsqueda.
                            search_key = data[[elem]].iat[i,0]
                            # searching candidates for data assignation
                            #print("query data is ", elem, "for search key", search_key, "type", type(search_key), "and column", column, "in", elem, domain)
                            if type(search_key) == str:
                                candidates = df[domain].query(f" {elem} == '{search_key}' and {column}.notnull()")
                            elif not pd.isna(search_key):
                                candidates = df[domain].query(f" {elem} == {search_key} and {column}.notnull()")
                            if not candidates.empty and not assigned:
                                # print("Candidates: ", candidates[column])
                                data.loc[i, column] = candidates[column].iloc[0]
                                assigned = True

                        else:
                            # CASO 2: el dataset origen y destino NO comparten la columna de búsqueda
                            search_key = data[support[domain]].iat[i,0]
                            # searching candidates for data assignation
                            print("query data is ", elem, "for search key", search_key, "type", type(search_key), "and column", column, "in", elem, domain)
                            if type(search_key) == str:
                                candidates = df[domain].query(f" {elem} == '{search_key}'")
                            elif not pd.isna(search_key):
                                candidates = df[domain].query(f" {elem} == {search_key}")
                            if not candidates.empty and not assigned:
                                # print("Candidates: ", candidates[column])
                                data.loc[i, column] = candidates[elem].iloc[0]
                                assigned = True

            if not assigned:
                data.loc[i,column] = str(data[id_column][i]) + "-" + column + "-desconocido"

            print("NEW " + column + " IS", data[column][i], "in position", i+1, "assigned is", assigned)
    return data[column]

