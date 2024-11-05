import cleaningFunctions as cf

def null_values(df)-> list:
    """Function that detects columns with null values in the dataset."""
    n_columns = []
    
    print("\n[GENERAL ANALYSIS][NULL VALUES]")
    for c in df.columns:
        if (df[c].isnull().any()):
            n_columns.append(c)
    print("The following columns have missing values: ", n_columns)

    return n_columns


def unique_id(df, c_id: list)-> dict:
    """Function that checks whether all the id elements in the datasets are unique."""

    unique = {}
    print("\n[GENERAL ANALYSIS][UNIQUE ID]")
    for c in c_id:
        duplicates = df[c][df[c].duplicated()].unique().tolist()

        if(len(duplicates) != 0):
            print("Duplicated data ", c, ": ", duplicates)
        else:
            print("No duplicated data")
        
        unique[c] = duplicates

    same={}
    same["same"] = True # Has each repeated ID the same column values? 
    same["col_diff"] = {} # For a repeated ID, the number of columns where duplicates are different in between. 
    for c in unique.keys():
        same["col_diff"][c] = {}
        for d in unique[c]:
            same["col_diff"][c][d] = {}
            
            dup_df = df[df[c] == d]
            #print(f"'{c}' = '{d}' :")
            
            copy = 0
            same["col_diff"][c][d]["all"] = []
            same["col_diff"][c][d]["some"] = [] 
            for col in dup_df.columns:
                if (len(dup_df[col].unique()) != 1):
                    
                    if (same["same"]):
                        same["same"] = False
                    
                    if (len(dup_df[col].unique()) == dup_df.shape[0]):
                        same["col_diff"][c][d]["all"].append(col)
                    else:
                        same["col_diff"][c][d]["some"].append(col)
            
            print(f"All values are different in the following columns: '{same['col_diff'][c][d]['all']}'")
            print(f"Some values are the same in the following columns: columns: '{same['col_diff'][c][d]['some']}'")

    unique["same"] = same

    return unique


def general_analysis(df, c_id: list)-> dict:
    """Function that executes a general analysis with common anomalies to all dataframes."""
    to_process = {}

    to_process["n_columns"] = null_values(df)               #1) Columns with null values?
    to_process["unique_id"] = unique_id(df, c_id)           #2) A Unique data column has duplicates?

    return to_process