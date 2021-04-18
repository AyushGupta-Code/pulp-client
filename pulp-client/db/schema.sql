CREATE TABLE IF NOT EXISTS user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  -- orderid INT UNIQUE NOT NULL,
  address TEXT NULL
  -- FOREIGN KEY (orderid) REFRENCES order (orderid)
);


CREATE TABLE IF NOT EXISTS shop (
  shopid INT UNIQUE NOT NULL,
  shop_name TEXT NOT NULL,
  shop_email TEXT NOT NULL,
  shop_address TEXT NOT NULL,
  PRIMARY KEY (shopid)
);


CREATE TABLE orders (
	orderid INT AUTO_INCREMENT,
	file BLOB NOT NULL,
	shopid INT NOT NULL,
	status TEXT, 
	userid TEXT NOT NULL,
	PRIMARY KEY (orderid),
	FOREIGN KEY (shopid) REFERENCES shop (shopid),
	FOREIGN KEY (userid) REFERENCES user (id)
);

