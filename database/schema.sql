-- COTA Project: Amateur Radio Contacts Database Schema
-- Tracks radio contacts made during camping activities at various parks/campgrounds

-- Parks reference table (to be imported from external parks file)
CREATE TABLE IF NOT EXISTS parks (
    park_id INTEGER PRIMARY KEY,
    park_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    state_province VARCHAR(50),
    country VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    park_code VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Campground/Site details within parks
CREATE TABLE IF NOT EXISTS campgrounds (
    campground_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    park_id INTEGER NOT NULL,
    campground_name VARCHAR(255) NOT NULL,
    site_number VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    elevation INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (park_id) REFERENCES parks(park_id) ON DELETE CASCADE,
    INDEX idx_park_id (park_id)
);

-- Radio operators participating in COTA
CREATE TABLE IF NOT EXISTS operators (
    operator_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    call_sign VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    license_class VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Contact log: individual amateur radio contacts
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    operator_id INTEGER NOT NULL,
    park_id INTEGER NOT NULL,
    campground_id INTEGER,
    contact_datetime TIMESTAMP NOT NULL,
    contact_date DATE GENERATED ALWAYS AS (DATE(contact_datetime)) STORED,
    contact_time TIME GENERATED ALWAYS AS (TIME(contact_datetime)) STORED,
    remote_call_sign VARCHAR(20) NOT NULL,
    remote_operator_name VARCHAR(255),
    remote_location VARCHAR(255),
    frequency_mhz DECIMAL(10, 2),
    mode VARCHAR(50), -- SSB, CW, FM, DIGITAL, etc.
    signal_report_sent VARCHAR(5), -- RST report format
    signal_report_received VARCHAR(5),
    duration_seconds INTEGER,
    notes TEXT,
    qth_locator VARCHAR(10), -- Maidenhead grid square
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id) ON DELETE CASCADE,
    FOREIGN KEY (park_id) REFERENCES parks(park_id) ON DELETE CASCADE,
    FOREIGN KEY (campground_id) REFERENCES campgrounds(campground_id) ON DELETE SET NULL,
    INDEX idx_operator_id (operator_id),
    INDEX idx_park_id (park_id),
    INDEX idx_contact_datetime (contact_datetime),
    INDEX idx_contact_date (contact_date),
    INDEX idx_remote_call_sign (remote_call_sign)
);

-- Activation events: track COTA activation sessions
CREATE TABLE IF NOT EXISTS activations (
    activation_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    park_id INTEGER NOT NULL,
    operator_id INTEGER NOT NULL,
    activation_start TIMESTAMP NOT NULL,
    activation_end TIMESTAMP,
    duration_hours DECIMAL(5, 2) GENERATED ALWAYS AS (TIMESTAMPDIFF(HOUR, activation_start, activation_end)) STORED,
    contact_count INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (park_id) REFERENCES parks(park_id) ON DELETE CASCADE,
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id) ON DELETE CASCADE,
    INDEX idx_park_id (park_id),
    INDEX idx_activation_start (activation_start),
    INDEX idx_operator_id (operator_id)
);

-- Equipment used during contacts
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    operator_id INTEGER NOT NULL,
    equipment_type VARCHAR(100), -- Radio, Antenna, Power Supply, etc.
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id) ON DELETE CASCADE
);

-- Contact-Equipment relationship (many-to-many)
CREATE TABLE IF NOT EXISTS contact_equipment (
    contact_equipment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    contact_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    UNIQUE KEY unique_contact_equipment (contact_id, equipment_id)
);

-- Statistics and summary tables (for performance optimization)
CREATE TABLE IF NOT EXISTS daily_statistics (
    stat_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    park_id INTEGER NOT NULL,
    contact_date DATE NOT NULL,
    contact_count INTEGER,
    unique_operators INTEGER,
    unique_remote_calls INTEGER,
    average_signal_report DECIMAL(5, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (park_id) REFERENCES parks(park_id) ON DELETE CASCADE,
    UNIQUE KEY unique_park_date (park_id, contact_date),
    INDEX idx_contact_date (contact_date)
);

-- Create views for common queries
CREATE OR REPLACE VIEW v_recent_contacts AS
SELECT 
    c.contact_id,
    o.call_sign,
    o.first_name,
    o.last_name,
    p.park_name,
    p.location,
    c.contact_datetime,
    c.remote_call_sign,
    c.frequency_mhz,
    c.mode,
    c.signal_report_sent,
    c.signal_report_received
FROM contacts c
JOIN operators o ON c.operator_id = o.operator_id
JOIN parks p ON c.park_id = p.park_id
ORDER BY c.contact_datetime DESC;

CREATE OR REPLACE VIEW v_park_summary AS
SELECT 
    p.park_id,
    p.park_name,
    p.location,
    COUNT(DISTINCT c.contact_id) as total_contacts,
    COUNT(DISTINCT c.operator_id) as unique_operators,
    COUNT(DISTINCT c.remote_call_sign) as unique_remote_calls,
    MAX(c.contact_datetime) as last_contact
FROM parks p
LEFT JOIN contacts c ON p.park_id = c.park_id
GROUP BY p.park_id, p.park_name, p.location;
