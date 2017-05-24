CREATE TABLE jianshu_info (
  creator_id   VARCHAR(255)  NOT NULL    DEFAULT '',
  creator_hash VARCHAR(255)  NOT NULL    DEFAULT '',
  creator_name VARCHAR(255)  NOT NULL    DEFAULT '',
  creator_sign VARCHAR(2000) NOT NULL    DEFAULT '',
  creator_logo VARCHAR(255)  NOT NULL    DEFAULT '',

  description  VARCHAR(3000) NOT NULL    DEFAULT '',
  article_num  INT(20)       NOT NULL    DEFAULT 0,
  follower     INT(20)       NOT NULL    DEFAULT 0,
  PRIMARY KEY (creator_id)
);

CREATE TABLE jianshu_article (
  article_id   VARCHAR(255)  NOT NULL    DEFAULT '',
  author_hash  VARCHAR(255)  NOT NULL    DEFAULT '',
  author_name  VARCHAR(255)  NOT NULL    DEFAULT '',
  author_sign  VARCHAR(2000) NOT NULL    DEFAULT '',

  author_id    VARCHAR(255)  NOT NULL    DEFAULT '',
  href         VARCHAR(255)  NOT NULL    DEFAULT '',
  title        VARCHAR(2000) NOT NULL    DEFAULT '',
  content      longtext      NOT NULL    DEFAULT '',
  comment      INT(20)       NOT NULL    DEFAULT 0,
  agree        VARCHAR(20)       NOT NULL    DEFAULT '无',
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

CREATE TABLE jianshu_collection_info (
  collection_fake_id    VARCHAR(50) NOT NULL,
  collection_real_id    VARCHAR(50) NOT NULL,
  title                 VARCHAR(255),
  description           VARCHAR(1000),
  follower              INT(20)     NOT NULL DEFAULT 0,
  PRIMARY KEY (collection_fake_id)
);

CREATE TABLE jianshu_collection_index (
  collection_fake_id    VARCHAR(50) NOT NULL,
  href                  VARCHAR(50) NOT NULL,
  PRIMARY KEY (collection_fake_id, href)
);

CREATE TABLE jianshu_notebooks_info (
  notebooks_id          VARCHAR(50) NOT NULL,
  author_name           VARCHAR(255)  NOT NULL,
  title                 VARCHAR(255),
  description           VARCHAR(1000),
  follower              INT(20)     NOT NULL DEFAULT 0,
  PRIMARY KEY (notebooks_id)
);

CREATE TABLE jianshu_notebooks_index (
  notebooks_id          VARCHAR(50) NOT NULL,
  href                  VARCHAR(50) NOT NULL,
  PRIMARY KEY (notebooks_id, href)
);