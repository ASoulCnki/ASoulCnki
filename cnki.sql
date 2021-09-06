drop table if exists user_dynamic;
create table user_dynamic
(
    dynamic_id bigint comment '动态唯一id',
    type_id    int comment '动态类型, 用于获取评论, 区分视频/',
    oid        bigint comment '动态对象id，用于获取评论',
    ctime      int comment '动态创建时间',
    uid        int comment '视频/专栏/动态 拥有者(UP主)uid',
    status     int comment '评论爬取状态，0: 未爬取， 1: 至少爬取完成过一次',
    primary key (dynamic_id)
) DEFAULT CHARACTER SET = utf8mb4;

drop table if exists kv;
create table kv_store
(
    field_name  varchar(255) NOT NULL,
    field_value text         NOT NULL,
    primary key (field_name)
) DEFAULT CHARACTER SET = utf8mb4;

drop table if exists reply;
create table reply
(
    rpid       bigint comment '回复id',
    type_id    int comment '动态类型,用于区分视频/专栏/动态',
    dynamic_id bigint comment '适用于动态的评论区',
    uid        int comment '视频/专栏/动态 拥有者(UP主)uid',
    mid        int comment '评论发布者id',
    oid        bigint comment '源稿件id',
    ctime      int comment '创建时间',
    m_name     varchar(255) comment '评论发布者昵称',
    content    text comment '评论内容',
    like_num   int,
    primary key (rpid)
) DEFAULT CHARACTER SET = utf8mb4;
