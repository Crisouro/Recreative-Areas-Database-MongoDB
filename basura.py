def clean_format(c: str, df, pattern: str, add = ""):
    """Algorithm for cleansing the format of a column."""

    regex = re.compile(pattern)
    
    def format_id(x):
        if pd.notnull(x):
            if regex.match(x):
                return x 
            else:
                numbers = ''.join(re.findall(r"\d+", x))

                if numbers:
                    return f"AR_{numbers}"
                
        return x

    if (c in ["NIF", "ID"]):
        df[c] = df[c].apply(lambda x: format_id(x))

def exp_format(df, cd_format):
    """Function that checks whether the column format coincides with the expected one"""

    expected = {}
    
    print("\n[GENERAL ANALYSIS][EXPECTED_FORMAT]")
    for c in cd_format.keys():
        regex = cd_format[c]["pattern"]
        print(type(df[c][0]))
        expected[c] = df[c].str.match(regex).all()
        if (not expected[c]):
            print(c, " values doesn't match expected format ", cd_format[c]["pattern"])
            cf.clean_format(c, df, regex, cd_format[c]["add"])
            print(c, " values format has been cleaned ", cd_format[c]["pattern"])
        else:
            print(c, " values match expected format ", cd_format[c]["pattern"])
    
    return expected