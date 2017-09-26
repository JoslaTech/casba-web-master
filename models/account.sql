CREATE TABLE ACCOUNT (
  ID int NOT NULL,
  bvn bigint,
  accNo bigint,
  accBank varchar(255),
  accName varchar(255),
  accType varchar(255),
  accBalance bigint,
  DoC DATE,
  Primary Key(ID)
);

INSERT INTO ACCOUNT (ID) VALUES (1);
