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

"""def null_codDistrito_asign(data, parser):
    Function that implementents the asignation of null values for COD_DISTRITO
    j=0
    for item in data:
        if item is null:
            for domain in parser:
                if not df[domain][j].isnull():
        j += 1"""