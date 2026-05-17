DROP TABLE IF EXISTS inquiries;
DROP TABLE IF EXISTS sell_requests;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS admins;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    mileage INT NOT NULL,
    transmission VARCHAR(50) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    colour VARCHAR(50),
    price DECIMAL(12,2) NOT NULL,
    description TEXT,
    image VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NULL,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(50),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
);

CREATE TABLE sell_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(150) NOT NULL,
    nic_passport VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(50) NOT NULL,
    whatsapp_number VARCHAR(50),
    email VARCHAR(150),
    district VARCHAR(100) NOT NULL,

    vehicle_brand VARCHAR(100) NOT NULL,
    vehicle_model VARCHAR(150) NOT NULL,
    manufacture_year VARCHAR(20) NOT NULL,
    mileage VARCHAR(100) NOT NULL,
    fuel_type VARCHAR(100) NOT NULL,
    transmission VARCHAR(100) NOT NULL,
    body_type VARCHAR(100),
    vehicle_colour VARCHAR(100),
    vehicle_condition VARCHAR(150) NOT NULL,
    previous_owners VARCHAR(100),
    registration_number VARCHAR(100),
    vehicle_image VARCHAR(255),

    expected_price_min DECIMAL(12,2),
    expected_price_max DECIMAL(12,2),
    insurance_status VARCHAR(150),
    revenue_license_valid_until VARCHAR(50),
    fault_status VARCHAR(150),
    preferred_contact_method VARCHAR(100),
    notes TEXT,

    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO vehicles
(make, model, year, mileage, transmission, fuel_type, colour, price, description, image, status)
VALUES
('Toyota', 'Corolla Altis', 2020, 45000, 'Auto', 'Petrol', 'White', 8500000.00, 'Quality used Toyota Corolla Altis available for sale.', 'img/cars/car-1.jpg', 'Available'),
('Honda', 'Vezel Hybrid', 2019, 38000, 'Auto', 'Hybrid', 'Red', 9200000.00, 'Honda Vezel Hybrid with excellent condition.', 'img/cars/car-2.jpg', 'Available'),
('Nissan', 'X-Trail 4WD', 2021, 22000, 'Auto', 'Petrol', 'Black', 14500000.00, 'Nissan X-Trail 4WD available for sale.', 'img/cars/car-3.jpg', 'Available'),
('Toyota', 'Aqua Hybrid', 2018, 55000, 'Auto', 'Hybrid', 'Blue', 6800000.00, 'Toyota Aqua Hybrid with good fuel efficiency.', 'img/cars/car-4.jpg', 'Available'),
('Suzuki', 'Swift Sport', 2022, 18000, 'Manual', 'Petrol', 'Yellow', 7400000.00, 'Suzuki Swift Sport in excellent condition.', 'img/cars/car-5.jpg', 'Available'),
('BMW', '3 Series 320i', 2020, 30000, 'Auto', 'Petrol', 'Blue', 22000000.00, 'BMW 3 Series 320i luxury vehicle.', 'img/cars/car-6.jpg', 'Available'),
('Honda', 'Fit Hybrid', 2019, 42000, 'Auto', 'Hybrid', 'Silver', 5900000.00, 'Honda Fit Hybrid available for sale.', 'img/cars/car-7.jpg', 'Available'),
('Mitsubishi', 'Outlander', 2021, 25000, 'Auto', 'Diesel', 'White', 16500000.00, 'Mitsubishi Outlander diesel SUV.', 'img/cars/car-8.jpg', 'Available');