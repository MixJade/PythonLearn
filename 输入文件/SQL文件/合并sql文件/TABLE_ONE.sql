create table TABLE_ONE
(
    ONE_ID    NVARCHAR2(32) not null
        primary key,
    ONE_NM    NVARCHAR2(400)
);

comment on table TABLE_ONE is '第一张表';

comment on column TABLE_ONE.ONE_ID is '第一个主键';

comment on column TABLE_ONE.ONE_NM is '第一个名称';
