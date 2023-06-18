if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df_state=pd.DataFrame(data=df.State.unique()).reset_index().rename({'index':'state_id',0:'state_name'},axis=1)
    df_district = df[['District','State']]\
        .drop_duplicates()\
        .reset_index()\
        .drop('index',axis=1)\
        .reset_index()\
        .rename({'index':'district_id','District':'district_name','State':'state_name'},axis=1)
    df_crop = df[['Crop','Production Units']]\
        .drop_duplicates()\
        .reset_index()\
        .drop('index',axis=1)\
        .reset_index()\
        .rename({'index':'crop_id','Crop':'crop_name','Production Units':'crop_measure'},axis=1)
    df_year = pd.DataFrame(data=df.Year.unique()).reset_index().rename({'index':'year_id',0:'year_name'},axis=1)
    df_year['year'] = df_year['year_name'].map(lambda x: int(x[0:4]))
    df_season = pd.DataFrame(data=df.Season.unique()).reset_index().rename({'index':'season_id',0:'season_type'},axis=1)
    df_area = pd.DataFrame(data=df.Area.unique()).reset_index().rename({'index':'area_id',0:'area_value'},axis=1)
    fact_table = df.merge(df_state,left_on='State',right_on='state_name')\
        .merge(df_district,left_on='District',right_on='district_name')\
        .merge(df_year,left_on='Year',right_on='year_name')\
        .merge(df_season,left_on='Season',right_on='season_type')\
        .merge(df_area,left_on='Area',right_on='area_value')\
        .merge(df_crop,left_on='Crop',right_on='crop_name')\
        [['district_id','state_id','year_id','season_id','area_id','crop_id','Production','Yield']]\
        .dropna(axis=0).reset_index().rename({'index':'id'},axis=1)



    return {
        'dim_state':df_state.to_dict(orient="dict"),
        'dim_district': df_district.to_dict(orient="dict"),
        'dim_crop': df_crop.to_dict(orient="dict"),
        'dim_year': df_year.to_dict(orient="dict"),
        'dim_season': df_season.to_dict(orient="dict"),
        'dim_area': df_area.to_dict(orient="dict"),
        'production_fact':fact_table.to_dict(orient="dict")
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'