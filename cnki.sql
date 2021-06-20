drop table if exists user_dynamic;
create table user_dynamic
(
    dynamic_id bigint comment '动态唯一id',
    type_id    int comment '动态类型, 用于获取评论',
    oid        bigint comment '动态对象id，用于获取评论',
    status     int comment '评论爬取状态，0: 未爬取， 1: 至少爬取完成过一次',
    primary key (dynamic_id)
) COMMENT '';

drop table if exists kv;
create table kv_store
(
    field_name  varchar(255) NOT NULL,
    field_value text         NOT NULL,
    primary key (field_name)
) COMMENT ''

drop table if exists reply;
create table reply
(
    rpid      bigint comment '回复id',
    type_id   int,
    mid       int comment '成员id',
    oid       bigint comment '源稿件id',
    ctime     int '创建时间',
    m_name    varchar(255) '昵称',
    content   text '评论内容',
    like_num  int,
    json_text text comment '爬虫原始数据',
    primary key (rpid)
)