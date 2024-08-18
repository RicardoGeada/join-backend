
def generate_initials(username):
    """
    Generate initials for the username. 
    e.g. 'John Doe' -> 'JD', 'Johndoe' -> 'JO', 'John Frederick Doe' -> 'JD'
    """
    if not username:
        return '--'
    
    if username:     
        names = username.split()
        if len(names) == 1:
            first_character = names[0][0].upper() 
            second_character = names[0][1].upper() if len(names[0]) > 1  else '-'
            return first_character + second_character 
        if len(names) > 1:
            return names[0][0].upper() + names[len(names)-1][0].upper()
    
    return '--'