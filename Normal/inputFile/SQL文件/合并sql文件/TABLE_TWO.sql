create table TABLE_TWO
(
    TWO_ID    NVARCHAR2(32) not null
        primary key,
    TWO_NM    NVARCHAR2(400)
);

comment on table TABLE_TWO is '第一张表';

comment on column TABLE_TWO.TWO_ID is '第一个主键';

comment on column TABLE_TWO.TWO_NM is '第一个名称';
