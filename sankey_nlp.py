"""
File: sankey.py
Description: Provide a wrapper that maps a dataframe to a sankey diagram
"""

import plotly.graph_objects as go

def _code_mapping(df, vars):
    """ Map labels in vars to integers """
    sum_value = list()
    # get distinct labels
    for var_idx in range(len(vars)):
        sum_value += list(df[vars[var_idx]])
    labels = sorted(set(sum_value))

    # get integer codes
    codes = list(range(len(labels)))

    # create label to code mapping
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    for var_idx in range(len(vars)):
        df = df.replace({vars[var_idx]: lc_map})

    return df, labels


def make_sankey(df, vars, vals=None):
    """""
    :param df: Input dataframe
    :param vars: List of labels
    :param vals: Thickness of the link for each row
    :return:
    """
    # convert dataframe to str
    df = df.astype(str)

    # applies values as necessary (if vals is given a value)
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df) # all 1's
    df, labels = _code_mapping(df, vars)

    # creates link to hold the sources and targets for the whole list of columns as one dict
    link = dict(source=[], target=[], value=[])
    for var_idx in range(len(vars)-1):
        link_key = f"{vars[var_idx]}_{vars[var_idx + 1]}"
        link['source'].extend(df[vars[var_idx]])
        link['target'].extend(df[vars[var_idx + 1]])
        link['value'].extend(values)

    # sets the node to the labels from _code_mapping
    node = {'label': labels}

    # generates the figure and plots it
    sk = go.Figure(data=[go.Sankey(link=link, node=node)])
    sk.show()


def main():
    # call some test routines on this library
    print("")



if __name__ == '__main__':
    main()