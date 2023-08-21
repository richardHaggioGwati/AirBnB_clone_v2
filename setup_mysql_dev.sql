-- Prepare MySQL server for the project

-- Create project development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create or update user 'hbnb_dev' with privileges
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;