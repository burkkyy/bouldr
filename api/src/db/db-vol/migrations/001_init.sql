-- Create Users Table
CREATE TABLE Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL,
    displayName TEXT, 
    joinDate DATE NOT NULL 
);

-- Create Regions Table 
CREATE TABLE Regions (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    parentID INTEGER NOT NULL,
    FOREIGN KEY (parentID) REFERENCES Regions(ID)
);

-- Create Boulders Table 
CREATE TABLE Boulders (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    authorID INTEGER NOT NULL, 
    name TEXT NOT NULL, 
    description TEXT, 
    image TEXT, 
    grade INTEGER NOT NULL,
    coordinates TEXT,
    dateAdded DATE NOT NULL,
    FOREIGN KEY (authorID) REFERENCES Users(ID)
);

-- Create Sends Table
CREATE TABLE Sends (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    boulderID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    rating REAL,
    sendType INTEGER NOT NULL,
    FOREIGN KEY (boulderID) REFERENCES Boulders(ID),
    FOREIGN KEY (userID) REFERENCES Users(ID)
);