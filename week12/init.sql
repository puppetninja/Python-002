CREATE TABLE IF NOT EXISTS phones (
    id               int auto_increment,
    phone_name       varchar(1024) unique,
    phone_url        text,
    PRIMARY KEY (id)
) CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS phone_comments (
    id               int auto_increment,
    phone_name       text,
    comment_content  text,
    comment_date     date,
    PRIMARY KEY (id)
) CHARACTER SET = utf8;
