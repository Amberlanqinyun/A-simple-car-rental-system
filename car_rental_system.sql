-- Create User Table
CREATE TABLE IF NOT EXISTS users
(
    UserID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Username VARCHAR(100) NOT NULL,
    PasswordHash VARCHAR(200) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Role ENUM('admin', 'customer', 'staff') NOT NULL
);

-- Create Customer Table
CREATE TABLE IF NOT EXISTS customers
(
    CustomerID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    UserID INT,
    CustomerName VARCHAR(100) NOT NULL,
    Address VARCHAR(200),
    Email VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20),
    FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Staff Table
CREATE TABLE IF NOT EXISTS staff
(
    StaffID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    UserID INT,
    StaffName VARCHAR(100) NOT NULL,
    Address VARCHAR(200),
    Email VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(20),
    FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Rental Cars Table
CREATE TABLE IF NOT EXISTS rental_cars
(
    CarID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    CarModel VARCHAR(100) NOT NULL,
    RegistrationNumber VARCHAR(10) NOT NULL,
    Year INT NOT NULL,
    SeatingCapacity INT NOT NULL,
    RentalPerDay DECIMAL(10, 2) NOT NULL,
    CarImage VARCHAR(200) -- Assuming the car image is stored as a URL or path
);


-- Insert Sample Data for Users (Including Password Hash and Role)
INSERT INTO users (Username, PasswordHash, Email, Role)
VALUES
    ('SarahAdams', '$2b$12$y1CUCO8Zghg3V9mTdI5RiOBZu39qDNbzYgsEaDKl0mH3J72Z4ENRO', 'sarah.adams@example.com', 'admin'),
    ('JohnDoe', '$2b$12$8ZsykTep9gr9SyxwUNfrg.NK9H6U9p2LRLv5o3ttAG4yfWUEs18iy', 'john.doe@example.com', 'customer'),
    ('JaneSmith', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'jane.smith@example.com', 'customer'),
    ('MikeJohnson', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'mike.johnson@example.com', 'customer'),
    ('EmilyBrown', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'emily.brown@example.com', 'customer'),
    ('DavidLee', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'david.lee@example.com', 'customer'),
    ('MichaelTurner', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'michael.turner@example.com', 'staff'),
    ('EmmaWhite', '$2b$12$5vQhJiaNocXWKOlMEOX//O60fA1MwMFph5U3.joqPhue6nnh8qE3S', 'emma.white@example.com', 'staff');

-- Insert Sample Data for Customers 
INSERT INTO customers (UserID, CustomerName, Address, Email, PhoneNumber)
VALUES
    (1, 'John Doe', '123 Main St, Auckland', 'john.doe@example.com', '+64 21 555 1234'),
    (2, 'Jane Smith',  '456 Oak Ave, North Shore, Auckland', 'jane.smith@example.com', '+64 27 555 5678'),
    (3, 'Mike Johnson', '789 Elm St, Henderson, Auckland', 'mike.johnson@example.com', '+64 22 555 9876'),
    (4, 'Emily Brown', '101 Pine Rd, Papatoetoe, Auckland', 'emily.brown@example.com', '+64 21 555 1111'),
    (5, 'David Lee', '555 Maple Ln, Mt. Wellington, Auckland', 'david.lee@example.com', '+64 27 555 2222');

-- Insert Sample Data for Staff 
INSERT INTO staff (UserID, StaffName, StaffNumber, Address, Email, PhoneNumber)
VALUES
    (6, 'Sarah Adams', 'STAFF001', '111 Elm St, Auckland Central, Auckland', 'sarah.adams@example.com', '+64 21 555 4444'),
    (7, 'Michael Turner', 'STAFF002', '222 Oak Ave, Albany, Auckland', 'michael.turner@example.com', '+64 22 555 5555'),
    (8, 'Emma White', 'STAFF003', '333 Pine Rd, Ellerslie, Auckland', 'emma.white@example.com', '+64 27 555 6666');


-- Insert Sample Data for Rental Cars (20 cars)
INSERT INTO rental_cars (CarModel, RegistrationNumber, Year, SeatingCapacity, RentalPerDay, CarImage)
VALUES
    ('Toyota Corolla', 'JSH346', 2022, 5, 50.00, 'https://freepngimg.com/thumb/car/1-2-car-png-picture.png'),
    ('Honda Civic', 'KTR567', 2021, 5, 55.00, 'https://freepngimg.com/thumb/car/2-2-car-transparent.png'),
    ('Ford Mustang', 'BNZ998', 2023, 4, 70.00, 'https://freepngimg.com/thumb/car/3-2-car-free-download-png.png'),
    ('Nissan Altima', 'DHY789', 2022, 5, 60.00, 'https://freepngimg.com/thumb/car/4-2-car-png-hd.png'),
    ('Kia Sportage', 'YTR123', 2023, 5, 65.00, 'https://freepngimg.com/thumb/car/5-2-car-png-pic.png'),
    ('Hyundai Sonata', 'HYD321', 2023, 5, 60.00, 'https://freepngimg.com/thumb/car/6-2-car-png-file.png'),
    ('Chevrolet Malibu', 'CHV987', 2023, 5, 65.00, 'https://freepngimg.com/thumb/car/7-2-car-free-png-image.pngg'),
    ('Volkswagen Passat', 'VWP654', 2023, 5, 70.00, 'https://freepngimg.com/thumb/car/13-2-car-png.png'),
    ('Subaru Legacy', 'SBL321', 2023, 5, 65.00, 'https://freepngimg.com/thumb/car/10-2-car-download-png.png'),
    ('Mazda 6', 'MZD654', 2023, 5, 60.00, 'https://freepngimg.com/thumb/car/11-2-car-download-png.png'),
    ('Audi A4', 'AUD987', 2023, 5, 75.00, 'https://freepngimg.com/thumb/car/13-2-car-download-png.png'),
    ('BMW 3 Series', 'BMW321', 2023, 5, 80.00, 'https://freepngimg.com/thumb/car/9-2-car-high-quality-png.png'),
    ('Mercedes-Benz C-Class', 'MBZ654', 2023, 5, 85.00, 'https://freepngimg.com/thumb/car/6-2-car-png-file.png'),
    ('Lexus IS', 'LEX987', 2023, 5, 80.00, 'https://freepngimg.com/thumb/car/9-2-car-high-quality-png.png'),
    ('Infiniti Q50', 'INF321', 2023, 5, 75.00, 'https://freepngimg.com/thumb/car/5-2-car-png-pic.png'),
    ('Acura TLX', 'ACU654', 2023, 5, 70.00, 'https://freepngimg.com/thumb/car/10-2-car-download-png.png'),
    ('Cadillac CT4', 'CAD987', 2023, 5, 75.00, 'https://freepngimg.com/thumb/car/12-2-car-png-image.png'),
    ('Alfa Romeo Giulia', 'ALF321', 2023, 5, 80.00, 'https://freepngimg.com/thumb/car/11-2-car-picture.png'),
    ('Volvo S60', 'VOL654', 2023, 5, 75.00, 'https://freepngimg.com/thumb/car/3-2-car-free-download-png.png'),
    ('Genesis G70', 'GEN987', 2023, 5, 80.00, 'https://freepngimg.com/thumb/car/1-2-car-png-picture.png');
