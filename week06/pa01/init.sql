CREATE TABLE IF NOT EXISTS movie_reviews (
    id              int auto_increment,
    review_rating   text,
    review_content  text,
    PRIMARY KEY (id)
) CHARACTER SET = utf8;
