CREATE TABLE team (
  TeamID INT PRIMARY KEY,
  TeamName VARCHAR(255) NOT NULL
);

CREATE TABLE token (
  TokenID INT PRIMARY KEY,
  TokenValue VARCHAR(255) NOT NULL,
  TokenType VARCHAR(255)
);

CREATE TABLE user (
  UserID INT PRIMARY KEY,
  UserName VARCHAR(255) NOT NULL,
  PW VARCHAR(255) NOT NULL
  TeamID INT,
  FOREIGN KEY (TeamID) REFERENCES team(TeamID)
);

CREATE TABLE userToToken (
  UserID INT,
  TokenID INT,
  FOREIGN KEY (UserID) REFERENCES user(UserID),
  FOREIGN KEY (TokenID) REFERENCES token(TokenID),
  PRIMARY KEY (UserID, TokenID)
);
INSERT INTO team VALUES(1,"Investment Team 1");
INSERT INTO user VALUES(1,"TaeheeKim","Taehee Kim","SuperSecretPassword",1);