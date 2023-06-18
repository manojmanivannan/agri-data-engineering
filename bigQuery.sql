create
or replace table `agriculture-data-pipe-project.analytic.production_tbl` as (
    SELECT
        c.crop_name,
        c.crop_measure,
        s.season_type,
        d.district_name,
        st.state_name,
        y.year,
        a.area_value,
        a.area_id,
        p.Production
    FROM
        `agriculture-data-pipe-project.analytic.production_fact` p
        join `agriculture-data-pipe-project.analytic.dim_crop` c on p.crop_id = c.crop_id
        join `agriculture-data-pipe-project.analytic.dim_season` s on p.season_id = s.season_id
        join `agriculture-data-pipe-project.analytic.dim_district` d on p.district_id = d.district_id
        join `agriculture-data-pipe-project.analytic.dim_state` st on p.state_id = st.state_id
        join `agriculture-data-pipe-project.analytic.dim_year` y on p.year_id = y.year_id
        join `agriculture-data-pipe-project.analytic.dim_area` a on p.area_id = a.area_id
);