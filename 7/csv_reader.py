# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

def load_profiles_lookup_table(ctx):
    import csv
    with open('/ring/ring/profile_lookup.txt') as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        reader.next()
        for row in reader:
            PR_CODE = row[0]
            r=ctx[PR_CODE] = {}
            r['TR_CODE'] = row[1]
            r['PROFIL_CODE'] = row[2]
            r['H'] = row[3]
            r['W'] = row[4]
            r['R60'] = row[5]
            r['R61'] = row[6]
            r['R20'] = row[7]
            r['R40'] = row[8]
            r['R41'] = row[9]
            r['P1'] = row[10]
            r['P2'] = row[11]
            r['P3'] = row[12]
            r['P4'] = row[13]
            r['BESCHREIBUNG'] = row[14]
    return ctx
        
#ctx=load_profiles_lookup_table({})
#ctx['PR_001']['TR_CODE']

