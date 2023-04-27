

CREATE TABLE if not exists user_data (
    username TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT,
    status TEXT CHECK (status IN ('active', 'inactive', 'disabled')),
    role TEXT CHECK(role IN ('admin','user')),
    plan TEXT CHECK(plan IN ('free','gold','platinum')),
    register_time TEXT
);

DELETE FROM user_data;

INSERT INTO user_data VALUES('user_free','test@gmail.com','$2b$12$E2h35wKPuFb3Vr8uC6Du8uzukmu0f2wM44uzm.UthGjKzKHEiMZNK','active','user','free','2023-04-26 11:16:20');
INSERT INTO user_data VALUES('damg7245','damg@gmail.com','$2b$12$yJ/iddK8UQjzx0oC3M/WteYutgmtGgub8uukDPZHj4gkk69hN97Jy','active','admin','platinum','2023-04-26 11:16:20');
INSERT INTO user_data VALUES('user_gold','test1@gmail.com','$2b$12$l7JWANZU3dr3/sQXx18FBu.oH6LMBeJy9EKuF/YcK0nFQ3N6UbZx6','active','user','gold','2023-04-26 11:16:20');
INSERT INTO user_data VALUES('user_platinum','test2@gmail.com','$2b$12$reKZJlqbGQNOfEm8cWJpK.AkU8OxGoQcv6sJsos1A9fGiYzimXV9m','active','user','platinum','2023-04-26 11:16:20');


CREATE TABLE if not exists plan_details (
    plan TEXT PRIMARY KEY,
    word_book TEXT,
    sign_it TEXT,
    hand_speak TEXT);

DELETE FROM plan_details;

INSERT INTO plan_details VALUES('free','5','5','5');
INSERT INTO plan_details VALUES('gold','10','10','10');
INSERT INTO plan_details VALUES('platinum','15','15','15');




CREATE TABLE if not exists user_current_usage (
    username TEXT PRIMARY KEY,
    word_book_currentcount TEXT,
    sign_it_currentcount TEXT,
    hand_speak_currentcount TEXT,
    word_book_lastused TEXT,
    sign_it_lastused TEXT,
    hand_speak_lastused TEXT
    );

DELETE FROM user_current_usage;

INSERT INTO user_current_usage VALUES('user_free','0','0','0','2023-04-26 11:16:20','2023-04-26 11:16:20','2023-04-26 11:16:20');
INSERT INTO user_current_usage VALUES('user_gold','0','0','0','2023-04-26 11:16:20','2023-04-26 11:16:20','2023-04-26 11:16:20');
INSERT INTO user_current_usage VALUES('user_platinum','0','0','0','2023-04-26 11:16:20','2023-04-26 11:16:20','2023-04-26 11:16:20');