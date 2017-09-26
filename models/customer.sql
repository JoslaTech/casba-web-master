CREATE TABLE CUSTOMER (
  ID int NOT NULL,
  bvn bigint,
  firstName varchar(255),
  lastName varchar(255),
  email varchar(255),
  phoneNumber varchar(255),
  dateOfBirth varchar(255),
  password varchar(255),
  city varchar(255),
  DoC DATE,
  Primary Key(ID)
);

INSERT INTO CUSTOMER (ID) VALUES (1);
