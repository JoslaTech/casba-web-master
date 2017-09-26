CREATE TABLE CARD (
  ID int NOT NULL,
  bvn bigint,
  accNo bigint,
  cardNo bigint,
  cardVendor varchar(255),
  cardType varchar(255),
  cvc bigint,
  expiry DATE,
  Primary Key(ID)
);

INSERT INTO CARD (ID) VALUES (1);
