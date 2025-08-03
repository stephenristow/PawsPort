DROP TABLE IF EXISTS PawsUser, Dog, Breed, DogBreed, Friendship;

CREATE TABLE PawsUser (
	email varchar(255) NOT NULL UNIQUE,
    pawsword varchar(255) NOT NULL,
    username varchar(32) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE Dog (
	dog_name varchar(50) NOT NULL,
    bio varchar(255),
    sex char(1) NOT NULL,
    age int NOT NULL,
    username varchar(32) NOT NULL,
    PRIMARY KEY (username, dog_name),
    FOREIGN KEY (username) REFERENCES PawsUser(username)
);

CREATE TABLE Breed (
	breed_name varchar(50) NOT NULL,
    PRIMARY KEY (breed_name)
);

CREATE TABLE DogBreed (
    username varchar(32) NOT NULL,
    dog_name varchar(50) NOT NULL,
    breed_name varchar(50) NOT NULL,
    PRIMARY KEY (username, dog_name, breed_name),
    FOREIGN KEY (username, dog_name) REFERENCES Dog(username, dog_name),
    FOREIGN KEY (breed_name) REFERENCES Breed(breed_name)
);

CREATE TABLE Friendship (
    username varchar(32) NOT NULL,
    friend_username varchar(32) NOT NULL,
    date_connected DATE,
    PRIMARY KEY (username, friend_username),
    FOREIGN KEY (username) REFERENCES PawsUser(username),
    FOREIGN KEY (friend_username) REFERENCES PawsUser(username)
);
