USE ctf;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS secrets;

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id VARCHAR(32) NOT NULL,
  email VARCHAR(128) NOT NULL,
  item VARCHAR(64) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE secrets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  flag VARCHAR(128) NOT NULL
);

INSERT INTO orders (order_id, email, item) VALUES
('A10293', 'sigma@school.local', 'Hoodie'),
('A10294', 'tungtung@school.local', 'T-Shirt'),
('A10295', 'imut@school.local', 'Cap');

INSERT INTO secrets (flag) VALUES
('LKSWNSB{SqLI_TT4Api1_BbutT44444}');
