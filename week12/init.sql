CREATE TABLE IF NOT EXISTS phones (
    id              int auto_increment,
    review_rating   text,
    review_content  text,
    PRIMARY KEY (id)
) CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS phone_comments (
    id              int auto_increment,
    phone_id        int,
    commnt          text,
    PRIMARY KEY (id),
    FOREIGN KEY (phone_id)
) CHARACTER SET = utf8;
