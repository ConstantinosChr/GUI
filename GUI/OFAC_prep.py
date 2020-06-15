import pandas as pd
import numpy as np

ofac = pd.read_csv('https://www.treasury.gov/ofac/downloads/sdn.csv',
                                  names=['ent_num', 'SDN_Name', 'SDN_Type', 'Program', 'Title', 'Call_Sign',
                                         'Vess_type', 'Tonnage', 'GRT', 'Vess_flag', 'Vess_owner', 'Remarks'])

ofac = ofac[ofac['SDN_Type'] == 'individual'][['SDN_Name']]

ofac = ofac['SDN_Name'].str.title()

ofac.to_csv("/Users/constantinos/PycharmProjects/GUI/GUI/OFAC_names.csv", index=False, header=False)
