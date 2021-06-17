drop table if exists user_dynamic;
create table user_dynamic
(
    dynamic_id int comment '动态唯一id',
    type_id    int comment '动态类型, 用于获取评论',
    oid        int comment '动态对象id，用于获取评论',
    primary key (dynamic_id)
) COMMENT '';

drop table if exists kv;
create table kv_store
(
    field_name  varchar NOT NULL,
    field_value varchar NOT NULL,
    primary key (field_name)
) COMMENT ''