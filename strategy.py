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

def null_codDistrito_assign(data, support_col, parser, df):
    """Function that implements the assignation of null values for COD_DISTRITO"""
    null_elems = data['COD_DISTRITO'].isnull().values.tolist()
    for i in range(len(null_elems)):
        if null_elems[i]:
            #print("null item in position ", i)
            #print("SUPPORT DATA IS", data[support_col].iat[i,0])
            search_key = data[support_col].iat[i,0]
            assigned = False
            for domain in parser:
                if not assigned:
                    for elem in parser[domain]:
                        candidates = df[domain].query(f" DISTRITO == '{search_key}' and COD_DISTRITO.notnull()")
                        if not candidates.empty:
                            #print("Candidates: ", candidates['COD_DISTRITO'])
                            data['COD_DISTRITO'][i] = candidates['COD_DISTRITO'].iloc[0]
                            assigned = True
            if not assigned:
                data['COD_DISTRITO'][i] = str(data['ID'][i]) + "-COD_DISTRITO-desconocido"

            print("NEW COD_DISTRITO IS", data['COD_DISTRITO'][i], "in position", i+1, "assigned is", assigned)
    return data['COD_DISTRITO']

