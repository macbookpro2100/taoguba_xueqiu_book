CREATE TABLE generic_info (
  creator_id   VARCHAR(255)  NOT NULL    DEFAULT '',
  creator_name VARCHAR(255)  NOT NULL    DEFAULT '',
  title        VARCHAR(255)  NOT NULL    DEFAULT '',
  description  VARCHAR(255)  NOT NULL    DEFAULT '',
  PRIMARY KEY (creator_id)
);

CREATE TABLE generic_article (
  article_id   VARCHAR(255)  NOT NULL    DEFAULT '',
  author_name  VARCHAR(255)  NOT NULL    DEFAULT '',
  author_id    VARCHAR(255)  NOT NULL    DEFAULT '',
  title        VARCHAR(2000) NOT NULL    DEFAULT '',
  content      longtext      NOT NULL    DEFAULT '',
  comment      INT(20)       NOT NULL    DEFAULT 0,
  agree        VARCHAR(255)  DEFAULT '无',
  publish_date DATE          NOT NULL    DEFAULT '2000-01-01',
  PRIMARY KEY (article_id)
);

CREATE TABLE LoginRecord (
  account    VARCHAR(255)   DEFAULT '',
  password   VARCHAR(255)   DEFAULT '',
  recordDate DATE           DEFAULT '2000-01-01',
  cookieStr  VARCHAR(50000) DEFAULT '',
  PRIMARY KEY (account)
);

