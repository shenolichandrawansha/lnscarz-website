USE lnscarz_db;

CREATE TABLE IF NOT EXISTS sell_requests (
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