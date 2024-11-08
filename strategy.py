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

def assign_aux_dir(data): #ARREGLAR
    """Function that assigns auxiliar address to main adress in case no data is assigned in any field"""
    null_via = data["TIPO_VIA"].isnull().values.tolist()
    null_nom = data["NOM_VIA"].isnull().values.tolist()
    null_num = data["NUM_VIA"].isnull().values.tolist()
    null_aux = data["DIRECCION_AUX"].isnull().values.tolist()

    tipo_via = data["TIPO_VIA"].unique().tolist()
    tipo_via = [x for x in tipo_via if not (isinstance(x, float))]
    tipo_via += ["PZ", "AVDA", "CTRA", "AUTOV", "Pza", "C .", "Pq ."]
    tipos_via_pattern = "|".join(tipo_via)

    pattern = rf'(?:(?P<TIPO_VIA>{tipos_via_pattern})\s*(?P<NOM_VIA>.*?)),?\s*(?P<NUM_VIA>\d{{1,5}})?'
    pattern_per_row = data['DIRECCION_AUX'].str.extract(pattern)
    #print(pattern_per_row)

    for i in range(len(data)):
        if (not null_aux[i]) and null_via[i] and null_num[i] and null_nom[i]:
            #print("No address detected in item at position", i+1)
            print(pattern_per_row.loc[i])

            #data[['TIPO_VIA', 'NOM_VIA', 'NUM_VIA']] = data['DIRECCION_AUX'].str.extract(pattern)

            #df['TIPO_VIA'] = df['TIPO_VIA'].fillna(str(data["ID"]) + "TIPO_VIA-desconocido")

            #(df[['TIPO_VIA', 'NOM_VIA', 'NUM_VIA']])

                #aux_add = df_data.at[i, "DIRECCION_AUX"]
    #df_data['aux_dir'] = df_data['aux_dir'].apply()

def null_assign(column: str, id_column: str, data, parser: dict, support: dict, df) -> dict:
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
                            #print("query data is ", elem, "for search key", search_key, "type", type(search_key), "and column", column, "in", elem, domain)
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

            #print("NEW " + column + " IS", data[column][i], "in position", i+1, "assigned is", assigned)
    return data[column]

