DROP DATABASE epytodo;
CREATE DATABASE IF NOT EXISTS epytodo;
USE epytodo;
CREATE TABLE IF NOT EXISTS user (
    user_id int(11) NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    CONSTRAINT
    PRIMARY KEY(user_id, username)
)AUTO_INCREMENT=0;

CREATE TABLE IF NOT EXISTS task (
    task_id int(11) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    begin DATETIME DEFAULT CURDATE(),
    end DATETIME,
    status ENUM('not started', 'in progress', 'done') NOT NULL DEFAULT 'not started',
    CONSTRAINT
    PRIMARY KEY (task_id)
);

CREATE TABLE IF NOT EXISTS user_has_task (
    fk_user_id int,
    fk_task_id int
);