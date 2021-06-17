drop table if exists video;
create table video
(
    aid          int,
    type_id      int,
    pic          varchar(200),
    play         int,
    description  varchar(400),
    title        varchar(200),
    sub_title    varchar(200),
    review       int,
    author       varchar(100),
    mid          int comment '用户id',
    created      int,
    length       varchar(40),
    video_review int,
    bvid         varchar(100),
) COMMENT '视频对象表';

drop table if exists user_dynamic ;
create table user_dynamic
(

) COMMENT '';