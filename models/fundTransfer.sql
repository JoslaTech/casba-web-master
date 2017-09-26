CREATE TABLE FUNDTRANSFER (
  ID int NOT NULL,
  bvn bigint,
  accNo bigint,
  accNoDestination bigint,
  amount bigint,
  DoC DATE,
  Primary Key(ID)
);

INSERT INTO FUNDTRANSFER (ID) VALUES (1);
