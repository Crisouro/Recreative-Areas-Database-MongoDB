"""File for cleaning supporting functions. """
def renaming_id():
    """Function that renames rows ID for granting unique name accordingly to the specified format."""
    #Coger el máximo número en ID y añadirlo a _.
    print(True)
    pass

def null_codDistrito_asign(data, parser):
    """Function that implementents the asignation of null values for COD_DISTRITO"""
    j=0
    for item in data:
        if item is null:
            for domain in parser:
                if not df[domain][j].isnull():

        j += 1

