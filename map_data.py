import pandas as pd


def getData(year):
    # loads vote data
    df = pd.read_csv('https://raw.githubusercontent.com/MEDSL/county-returns/master/countypres_2000-2016.csv',
                     dtype={"FIPS": str})

    # fixes the FIPS data
    df['FIPS'] = df['FIPS'].astype(str).str.zfill(5)
    df = df[df['year'] == year]
    df_republican = df[df['party'] == 'republican']
    df_democrat = df[df['party'] == 'democrat']

    # Now lets reconcat it together with name qualifiers
    df = pd.concat([df_republican.set_index('FIPS'),
                    df_democrat.set_index('FIPS')],
                   axis=1,
                   keys=('rep', 'dem')
                   )

    # pops the name on the front instead of a multiindex
    df.columns = df.columns.map('_'.join)
    df['fips'] = df.index
    df = df.drop(columns=['rep_year', 'rep_state', 'rep_state_po', 'rep_county', 'rep_office',
                          'rep_candidate', 'rep_party',
                          'rep_version', 'dem_year', 'dem_state', 'dem_state_po', 'dem_county',
                          'dem_office', 'dem_candidate', 'dem_party',
                          'dem_totalvotes', 'dem_version'
                          ])
    json = df.to_json(orient='records')
    
    return json