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
            print(f"'{c}' = '{d}' :")
            
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
            
            print(f"All values are different in the following columns: '{same["col_diff"][c][d]["all"]}'")
            print(f"Some values are the same in the following columns: columns: '{same["col_diff"][c][d]["some"]}'")

    unique["same"] = same

    return unique
        

def enum_display(df, c_enum: list)-> dict:
    """Function that displays the values used in an enumerated type field."""
    enum_values = {}

    print("\n[GENERAL ANALYSIS][ENUMERATION DISPLAY]")
    for c in c_enum:
        enum_values[c] = df[c].unique()
        print(c, ": ", enum_values[c])

    return enum_values

def general_analysis(df, c_id: list, cd_format: dict, c_enum: list)-> dict:
    """Function that executes a general analysis with common anomalies to all dataframes."""
    to_process = {}

    to_process["n_columns"] = null_values(df)               #1) Columns with null values?
    #to_process["exp_format"] = exp_format(df, cd_format)   #2) The column data follows the expected format.
    to_process["unique_id"] = unique_id(df, c_id)           #3) A Unique data column has duplicates?
    to_process["enum_values"] = enum_display(df, c_enum)    #4) Values in enumerated type columns.

    #type_analysis(df, c_type)                              #2) All columns' data are the expected type?

    return to_process