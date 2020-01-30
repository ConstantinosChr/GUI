import pandas as pd
import numpy as np
import string
from itertools import permutations
import random
import json

## Static values
# Transposition
alphabet = list(string.ascii_lowercase)

phonetic_transpositions = [("ed","de"),("de","ed"),
                           ("ei","ie"),("ie","ei"),
                           ("ae","ea"),("ea","ae"),
                           ("th","ht"),("au","ua"),
                           ("re","er"),("er","re"),
                           ("rt","tr"),("is","si"),
                           ("sm","ms"),("se","es"),
                           ("oe","eo"),("or","ro"),
                           ("ro","or"),("sh","hs"),
                           ("hs","sh"),("ch","hc"),
                           ("hc","ch"),("eh","he"),
                           ("he","eh"),("tu","ut"),
                           ("ts","st"),("oa","ao"),]

potential_permutations = set(list(permutations(["a","e","i","o","u"],2))) # n* (n-1)
potential_transpositions = set([(x[0]+x[1],x[1]+x[0]) for x in potential_permutations])
uncommon_transpositions = potential_transpositions.difference(phonetic_transpositions)

# Titles
titles = ["Mr. ","Mr ","Mrs. ","Mrs ","Mx. ", "Mx ", "Ms. ","Ms ","Miss ","Madam "]

# Character Replacement
phonetic_replacements = [("s","z") , ("z","s") , ("s","c"), ("c","s") , ("c","z"),
                        ("z","c") , ("u","o") , ("o","u"), ("ua","o"), ("o","ua"),
                        ("ph","f"), ("f","ph"), ("y","i"), ("i","y") , ("d","th"), 
                        ("t","d") , ("v","w") , ("w","v"), ("k","q") , ("q","k"), 
                        ("v","b") , ("b","v") , ("a","e"), ("e","a") , ("x","j"), 
                        ("j","x") , ("v","f") , ("f","v"), ("c","k") , ("k","c")]      

typographic_errors = [("t","y"), ("y","t"), ("o","p"), ("p","o"), 
                          ("d","e"), ("e","d"), ("f","d"), ("d","f"),
                          ("r","f"), ("f","r"), ("e","r"), ("r","e"),
                          ("r","t"), ("t","r")]

alphabet_alternatives = [("n","ñ"), ("ñ","n")]

already_used_permutations = phonetic_replacements + typographic_errors + alphabet_alternatives
potential_comb = set(list(permutations(string.ascii_lowercase,2)))
uncommon_replacements = potential_comb.difference(already_used_permutations)

#Auxiliar Functions


def get_vowel_index(name):
    vowels = ["a","e","i","o","u","A","E","I","O","U"]
    return [i for i,j in enumerate(name) if j in vowels]


def get_vowel_lowercase_index(name):
    vowels = ["a","e","i","o","u"]
    return [i for i,j in enumerate(name) if j in vowels]


def get_vowel_uppercase_index(name):
    vowels = ["A","E","I","O","U"]
    return [i for i,j in enumerate(name) if j in vowels]


def get_consonant_lowercase_index(name):
    consonants = [x for x in string.ascii_lowercase if x not in "aeiou"]
    return [i for i,j in enumerate(name) if j in consonants]


def swap_letter(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)


def swap_element(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ' '.join(c)


def check_success(original_name, resulting_name):
    if resulting_name != original_name:
        success = "True"
    else:
        success = "False"

    return success


#Initials
def firstname_initials_single(name):
    '''Returns first element as initial if more than one element in name'''
    name_elements = name.split(" ")
    if len(name_elements)>=2:
        output = name_elements[0][0] + ". "
        return output + " ".join(name_elements[1:])
    else:
        return name


def firstname_initials(name):
    '''Returns first and second element as initials if more than two elements in name,
        otherwise first element as initial '''
    name_elements = name.split(" ")
    if len(name_elements)>=3:
        output = name_elements[0][0] + "." + name_elements[1][0] + ". "
        return output + " ".join(name_elements[2:])
    else:
        return firstname_initials_single(name)


def initials_lastname(name):
    '''Returns last element as initial if more than one element in name'''
    name_elements = name.split(" ")
    if len(name_elements)>=2:
        output = name_elements[-1][0] + "."
        return " ".join(name_elements[:-1]) + " " + output
    else:
        return firstname_initials_single(name)


def lastname_initials_clear_first_name(name):
    '''xxx'''
    name_elements = name.split(" ")
    if len(name_elements)>=2:
        output = name_elements[-1][0] + "."
        return " ".join(name_elements[1:-1]) + " " + output
    else:
        return firstname_initials_single(name)


def initials_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    initials_dict = {"Initials": {"firstname_initials_single": firstname_initials_single,
                                  "firstname_initials": firstname_initials,
                                  "initials_lastname": initials_lastname,
                                  "lastname_initials_clear_first_name": lastname_initials_clear_first_name}}

    for key in initials_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in initials_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


#Character Extension
def add_spc_in_letters(name):
    '''Randomly adds a space in the middle of name element'''
    name_elements = name.split(" ")
    cne = np.random.choice(name_elements) # chosen name element
    cli = np.random.choice([x+1 for x in range(len(cne)-1)]) # chosen letter index
    return name.replace(cne,cne[:cli] + " " + cne[cli:])


def add_al_and_hyphen(name):
    '''Adds 'al-'' to the last element of a name'''
    name_elements = name.split(" ")
    return " ".join(name_elements[:-1]) + " al-" + name_elements[-1]


def add_Al_and_space(name):
    '''Adds 'Al-'' to the last element of a name'''
    name_elements = name.split(" ")
    return " ".join(name_elements[:-1]) + " Al-" + name_elements[-1]


def add_El_and_space(name):
    '''Adds 'El-'' to the last element of a name'''
    name_elements = name.split(" ")
    return " ".join(name_elements[:-1]) + " El-" + name_elements[-1]


def add_vowel(name):
    '''Adds a lowecase vowel to a randomly chosen element of the name'''
    vowels = ["a","e","i","o","u"]
    name_elements = name.split(" ")
    cv = np.random.choice(vowels) # chosen vowel
    cne = np.random.choice(name_elements) # chosen name element
    cli = np.random.choice([x+1 for x in range(len(cne)-1)]) # chosen letter index
    return name.replace(cne,cne[:cli] + cv + cne[cli:])


def add_h_before_vowel(name):
    '''Adds an h before a vowel to a randomly chosen element of the name'''
    vlcindx = get_vowel_lowercase_index(name) # vowels lower case index
    rcvi    = np.random.choice(vlcindx)# randomly chosen vowel index
    return name[:rcvi] + "h" +  name[rcvi:]


def add_consonant_final_s(name):
    '''Adds an s after a randomly chosen element of the name'''
    name_elements = name.split(" ")
    cne = np.random.choice(name_elements) # chosen name element
    return name.replace(cne,cne + "s")


def add_consonant_final_r(name):
    '''Adds an s after a randomly chosen element of the name'''
    name_elements = name.split(" ")
    cne = np.random.choice(name_elements) # chosen name element
    return name.replace(cne,cne + "r")


def add_consonant_final_z(name):
    '''Adds an s after a randomly chosen element of the name'''
    name_elements = name.split(" ")
    cne = np.random.choice(name_elements) # chosen name element
    return name.replace(cne,cne + "z")


def add_consonant_uncommon(name):
    '''Adds a non r,s,z consonant in a randomly chosen element of the name'''
    consonants = [x for x in string.ascii_lowercase if x not in "aeioursz"]
    name_elements = name.split(" ")
    cc = np.random.choice(consonants)
    cne = np.random.choice(name_elements) # chosen name element
    cli = np.random.choice([x+1 for x in range(len(cne)-1)]) # chosen letter index
    return name.replace(cne,cne[:cli] + cc + cne[cli:])


def add_consonant_double(name):
    '''Adds a double consonant in a randomly chosen element of the name'''
    consonants = [x for x in string.ascii_lowercase if x not in "aeiou"]
    cindx      = get_consonant_lowercase_index(name) # consonants index
    ccindx     = np.random.choice(cindx) # chosen consonant index
    cdc         = name[ccindx] #chosen doubled consonant
    return name[:ccindx] + cdc +name[ccindx:]


def add_special_character_apostrophe(name):
    '''Adds an apostrophe in a randomly chosen element of the name'''
    name_elements = name.split(" ")
    cne = np.random.choice(name_elements) # chosen name element
    ci = np.random.choice([x+1 for x in range(len(cne))]) #chosen index
    return name.replace(cne,cne[:ci] + "'" + cne[ci:])


def add_special_character_accent(name):
    '''Adds an accent to a vowel from a randomly chosen element of the name'''
    accents_dict = {"a":"á","e":"é","i":"í","o":"ó","u":"ú"}
    name_elements = name.split(" ")
    vlcindx = get_vowel_lowercase_index(name) # vowels lower case index
    rcvi    = np.random.choice(vlcindx)# randomly chosen vowel index
    return name[:rcvi] +accents_dict[name[rcvi]] + name[rcvi+1:]


def add_special_character_uncommon(name):
    '''Adds a punctuation simbol to a randomly chosen element of the name'''
    simbol = np.random.choice([x for x in string.punctuation if x not in ["'"]])
    ci = np.random.choice(range(len(name))) # chosen index
    return name[:ci] + simbol + name[ci:]


def character_extension_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    char_ext_dict = {
        "Character Extension": {
            "add_spc_in_letters": add_spc_in_letters,
            "add_prefix": {
                "add_al_and_hyphen": add_al_and_hyphen,
                "add_Al_and_space": add_Al_and_space,
                "add_El_and_space": add_El_and_space},
            "add_vowel": add_vowel,
            "add_h_before_vowel": add_h_before_vowel,
            "add_consonant": {
                "add_consonant_final_s": add_consonant_final_s,
                "add_consonant_final_r": add_consonant_final_r,
                "add_consonant_final_z": add_consonant_final_z,
                "add_consonant_uncommon": add_consonant_uncommon,
                "add_consonant_double": add_consonant_double},
            "add_special_character": {
                "add_special_character_apostrophe": add_special_character_apostrophe,
                "add_special_character_accent": add_special_character_accent,
                "add_special_character_uncommon": add_special_character_uncommon}}}

    for key in char_ext_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in char_ext_dict[key].items():
            if isinstance(char_ext_dict[key][key2], dict):
                for key3, value2 in char_ext_dict[key][key2].items():
                    variation_category.append(key)
                    original_name_list.append(original_name)
                    variation_subcategory.append(key2)
                    name_variation.append(key3)
                    resulting_name.append(value2(original_name))
                    success.append(check_success(original_name, value2(original_name)))
            else:
                variation_category.append(key)
                original_name_list.append(original_name)
                variation_subcategory.append(key2)
                name_variation.append(key2)
                resulting_name.append(value(original_name))
                success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Character Replacement
def phonetic_replacement(name):
    '''Selects a letter at random and replace it with a similar phonetic letter'''
        
    # Check if potential replacements, otherwise return original name
    pr = set([x[0] for x in phonetic_replacements]) #potential replacements
    if len([x for x in name if x in pr])==0:
        return name
    
    # Choose a character that it is a candidate phonetic replacement
    rci = np.random.choice([i for i,j in enumerate(name)
                            if j.lower() in pr]) #randomnly chosen index   
    
    # Find potential character replacements
    ptr = [x[1] for x in phonetic_replacements
                       if x[0]==name[rci].lower()] #potential to replace

    # Replace the character to a random phonetic replacement
    if name[rci].islower():
        
        return name[:rci] + np.random.choice(ptr) + name[rci+1:]
    else:
        return name[:rci] + np.random.choice(ptr).upper() + name[rci+1:]


def typographic_error(name):
    '''Selects a letter at random and replace it with a potential typographic error'''
    
    # Check if potential replacements, otherwise return original name
    pr = set([x[0] for x in typographic_errors]) #potential replacements
    if len([x for x in name if x in pr])==0:
        return name
    
    # Choose a character that it is a candidate typographic_error
    rci = np.random.choice([i for i,j in enumerate(name)
                            if j.lower() in pr]) #randomnly chosen index   

    # Find potential character replacements
    ptr = [x[1] for x in typographic_errors
                       if x[0]==name[rci].lower()] #potential to replace

    # Replace the character to a random typographic error
    if name[rci].islower():
        return name[:rci] + np.random.choice(ptr) + name[rci+1:]
    else:
        return name[:rci] + np.random.choice(ptr).upper() + name[rci+1:]


def alphabet_alternative(name):
    '''Selects a letter at random and replace it with a potential typographic error'''

    # Check if potential replacements, otherwise return original name
    pr = set([x[0] for x in alphabet_alternatives]) #potential replacements
    if len([x for x in name if x in pr])==0:
        return name
        
    # Choose a character that it is a candidate alphabet_alternative
    rci = np.random.choice([i for i,j in enumerate(name)
                            if j.lower() in pr]) #randomnly chosen index
    
    # Find potential character replacements
    ptr = [x[1] for x in alphabet_alternatives
                       if x[0]==name[rci].lower()] #potential to replace
    
    # Replace the character to a random alphabet alternative
    if name[rci].islower():
        return name[:rci] + np.random.choice(ptr) + name[rci+1:]
    else:
        return name[:rci] + np.random.choice(ptr).upper() + name[rci+1:]


def character_replacement_uncommon(name):
    '''Character replacement uncommon'''
    # Check if potential replacements, otherwise return original name
    pr = set([x[0] for x in uncommon_replacements]) #potential replacements
    if len([x for x in name if x in pr])==0:
        return name
        
    # Choose a character that it is a candidate alphabet_alternative
    rci = np.random.choice([i for i,j in enumerate(name)
                            if j.lower() in pr]) #randomnly chosen index
    
    # Find potential character replacements
    ptr = [x[1] for x in uncommon_replacements
                       if x[0]==name[rci].lower()] #potential to replace
    
    # Replace the character to a random uncommon replacements
    if name[rci].islower():
        return name[:rci] + np.random.choice(ptr) + name[rci+1:]
    else:
        return name[:rci] + np.random.choice(ptr).upper() + name[rci+1:]


def charachter_replacement_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    char_rep_dict = {
    "Character Replacement": {
        "phonetic_replacement": phonetic_replacement,
        "typographic_error": typographic_error,
        "alphabet_alternative": alphabet_alternative,
        "character_replacement_uncommon": character_replacement_uncommon
        }}

    for key in char_rep_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in char_rep_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


#Character Reduction
def remove_h(name):
    ''' If name has h remove one at random, otherwise return same name '''
    if "h" in name: 
        rci = np.random.choice([i for i,j in enumerate(name)
                                if j.lower() == "h"]) #randomnly chosen index
        return name[0:rci:] + name[rci+1::]
    else:
        return name


def remove_c_before_k(name):
    ''' If c before k, it removes c, otherwise return same name '''
    if "ck" in name:
        return name.replace("ck","k")
    if "Ck" in name:
        return name.replace("Ck","K")
    else:
        return name


def remove_e_before_s(name):
    ''' If c before k, it removes c, otherwise return same name '''
    if "es" in name:
        return name.replace("es","s")
    if "Es" in name:
        return name.replace("Es","S")
    else:
        return name


def remove_final_s(name):
    '''Remove "s" if at the end of a name element'''
    name_elements = name.split(" ")
    ees = [x for x in name_elements if x[-1]=="s"] #elements ending in "s"
    if ees:
        etrs = np.random.choice(ees) #element to remove "s"
        return name.replace(etrs,etrs[:-1])
    else:
        return name


def remove_final_z(name):
    '''Remove "z" if at the end of a name element'''
    name_elements = name.split(" ")
    ees = [x for x in name_elements if x[-1]=="z"] #elements ending in "z"
    if ees:
        etrs = np.random.choice(ees) #element to remove "z"
        return name.replace(etrs,etrs[:-1])
    else:
        return name


def remove_final_d(name):
    '''Remove "d" if at the end of a name element'''
    name_elements = name.split(" ")
    ees = [x for x in name_elements if x[-1]=="d"] #elements ending in "d"
    if ees:
        etrs = np.random.choice(ees) #element to remove "d"
        return name.replace(etrs,etrs[:-1])
    else:
        return name


def character_reduction_uncommon(name):
    '''Remove a character at random'''
    ccitr = [i for i,j in enumerate(name) if j!=" "] #candidate character index to remove
    citr  = np.random.choice(ccitr) #character index to remove
    return name[0:citr:] + name[citr+1::]


# Transposition
def phonetic_transposition(name):
    '''Perform common phonetic transpositions'''
    pt = [(i,j) for i,j in [x for x in phonetic_transpositions if x[0] in name]] #potential traspositions
    if pt:
        i = np.random.choice([i for i,j in enumerate(pt)])
        return name.replace(pt[i][0],pt[i][1])
    else:
        return name


def transposition_uncommon(name):
    '''Perform uncommon phonetic transpositions'''
    pt = [(i,j) for i,j in uncommon_transpositions if i in name] #potential traspositions
    if len(pt) == 0:
        return name
    else:
        np.random.shuffle(pt)  # shuffle potential transpositions
        random_pt = pt.pop()  # select the first one from the shuffled list

        pt_letters = list(random_pt[0])

        # Get letter positions
        first_letter = [pos for pos, char in enumerate(name) if char == pt_letters[0]]
        second_letter = [pos for pos, char in enumerate(name) if char == pt_letters[1]]

        let_pos = []
        for i in range(len(first_letter)):
            if first_letter[i] + 1 in second_letter:
                let_pos.append(first_letter[i])

        np.random.shuffle(let_pos)
        let_pos = let_pos.pop()
        final_name = swap_letter(name, let_pos, let_pos + 1)
    return final_name


def transposition_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    trans_dict = {
        "Transposition": {
            "phonetic_transposition": phonetic_transposition,
            "transposition_uncommon": transposition_uncommon}}

    for key in trans_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in trans_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


def charachter_reduction_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    char_rep_dict = {
    "Character Reduction": {
        "phonetic_miss": {
            "remove_h": remove_h,
            "remove_c_before_k": remove_c_before_k,
            "remove_e_before_s": remove_e_before_s,
            "remove_final_s": remove_final_s,
            "remove_final_z": remove_final_z,
            "remove_final_d": remove_final_d},
        "character_reduction_uncommon": character_reduction_uncommon
        }}

    for key in char_rep_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in char_rep_dict[key].items():
            if isinstance(char_rep_dict[key][key2], dict):
                for key3, value2 in char_rep_dict[key][key2].items():
                    variation_category.append(key)
                    original_name_list.append(original_name)
                    variation_subcategory.append(key2)
                    name_variation.append(key3)
                    resulting_name.append(value2(original_name))
                    success.append(check_success(original_name, value2(original_name)))
            else:
                variation_category.append(key)
                original_name_list.append(original_name)
                variation_subcategory.append(key2)
                name_variation.append(key2)
                resulting_name.append(value(original_name))
                success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Double Characters
def double_character_reduction(name):
    '''Finds double characters and removes one of the two characters'''
    double_characters_reps = [x+x for x in string.ascii_lowercase]
    pdcr = [dcr for dcr in double_characters_reps if dcr in name]
    if pdcr:
        ci = np.random.choice([i for i,j in enumerate(pdcr)])
        return name.replace(pdcr[ci], pdcr[ci][1])
    else:
        return name


def double_character_insertion(name):
    '''Takes any character at random and doubles it'''
    ci = np.random.choice([i for i,j in enumerate(name) if j!= " "])
    return name[:ci] + name[ci] + name[ci:]


def double_characters_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    double_char_dict = {
        "Double Characters": {
            "double_character_reduction": double_character_reduction,
            "double_character_insertion": double_character_insertion}}

    for key in double_char_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in double_char_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Spaces
def spaces_reduction(name):
    '''Deletes a space randomly in the string'''
    if len(name)>1:
        ci = np.random.choice([i for i,j in enumerate(name) if j== " "])
        return name[:ci] + name[ci+1:]
    else:
        return name


def spaces_insertion(name):
    '''Inserts a space randomly in the string'''
    ci = np.random.choice([i for i,j in enumerate(name) if j!= " "])
    return name[:ci] + " " + name[ci:]


def spaces_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    spaces_dict = {
        "Spaces": {
            "spaces_reduction": spaces_reduction,
            "spaces_insertion": spaces_insertion}}

    for key in spaces_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in spaces_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Name Order
def transposition_name(name):
    '''Transposes two elements of the name at random'''
    name_elements = name.split(" ")
    if len(name_elements)==1:
        return name
    elif len(name_elements)==2:
        return name_elements[1] + " " + name_elements[0]
    else:
        random_element_to_swap = random.randint(0, len(name_elements) - 1)
        random_element_to_be_swapped = random.randint(0, len(name_elements) - 1)
        index = list(range(0, len(name_elements)))
        if random_element_to_swap != random_element_to_be_swapped:
            return swap_element(name_elements, random_element_to_swap, random_element_to_be_swapped)
        else:
            index.pop(random_element_to_be_swapped)
            random_element_to_be_swapped = random.choice(index)
            return swap_element(name_elements, random_element_to_swap, random_element_to_be_swapped)


def random_name_transposition(name):
    '''Suffles name order at random'''
    name_elements_original = name.split(" ")
    name_elements_shuffle = name.split(" ")
    if len(name_elements_original)>=2:
        while name_elements_shuffle == name_elements_original:
            np.random.shuffle(name_elements_shuffle)
        return " ".join(name_elements_shuffle)
    else:
        return name


def name_order_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    name_order_dict = {
        "Name Order": {
            "random_name_transposition": random_name_transposition,
            "transposition_name": transposition_name}}

    for key in name_order_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in name_order_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Titles
def title_insertion(name):
    '''Adds title at the beginning of the name'''
    title = np.random.choice(titles)
    return title + name


def title_removal(name):
    '''Removes title if present'''
    if [x for x in titles if x in name]:
        for t in titles:
            name = name.replace(t,"")
    return name


def titles_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    titles_dict = {
        "Titles": {
            "title_insertion": title_insertion,
            "title_removal": title_removal}}

    for key in titles_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in titles_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


# Missing Name Component
def name_component_deletion(name):
    '''Deletes one element at random if name has more than one element'''
    name_elements = name.split(" ")
    if len(name_elements)>1:
        element_to_delete = np.random.choice(name_elements)
        return " ".join([x for x in name.split(" ") if x != element_to_delete])
    else:
        return name

def missing_name_comp_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    miss_name_com_dict = {
        "Missing Name Component": {
            "name_component_deletion": name_component_deletion}}

    for key in miss_name_com_dict:

        variation_category = []
        variation_subcategory = []
        name_variation = []
        original_name_list = []
        resulting_name = []
        success = []

        for key2, value in miss_name_com_dict[key].items():
            variation_category.append(key)
            variation_subcategory.append(key2)
            name_variation.append(key2)
            original_name_list.append(original_name)
            resulting_name.append(value(original_name))
            success.append(check_success(original_name, value(original_name)))

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df

def find_aliases_function(original_name):
    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    aliases = json.load(open("dictionary_aliases.json"))

    variation_category = []
    variation_subcategory = []
    name_variation = []
    original_name_list = []
    resulting_name = []
    success = []

    for key, value in aliases.items():
        if key == original_name:
            for alias in value:
                variation_category.append("Alias")
                variation_subcategory.append("Alias")
                name_variation.append("Alias")
                original_name_list.append(original_name)
                success.append("Alias")
                resulting_name.append(alias)

    output_df = pd.DataFrame(list(zip(variation_category,
                                      variation_subcategory,
                                      name_variation,
                                      original_name_list,
                                      resulting_name,
                                      success)), columns=columns)

    return output_df


def get_name_var(original_name, function_list):
    all_fun_dict = {
        "Initials": initials_function,
        "Character Extension": character_extension_function,
        "Character Replacement": charachter_replacement_function,
        "Character Reduction": charachter_reduction_function,
        "Transposition": transposition_function,
        "Double Characters": double_characters_function,
        "Spaces": spaces_function,
        "Name Order": name_order_function,
        "Titles": titles_function,
        "Missing Name Component": missing_name_comp_function,
        "Also Known As": find_aliases_function}

    columns = ["Variation Category", "Variation Sub Category", "Name Variation", "Original Name", "Resulting Name",
               "Success"]

    result = pd.DataFrame(columns=columns)


    for key, value in all_fun_dict.items():
        for fun in function_list:
            if key == fun:
                result = result.append(value(original_name), ignore_index=True)

    return result


