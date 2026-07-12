-- Add campground suggestions tracking to the database

CREATE TABLE IF NOT EXISTS campground_suggestions (
    suggestion_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    suggester_name VARCHAR(255) NOT NULL,
    suggester_email VARCHAR(255),
    suggester_call_sign VARCHAR(20),
    park_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    state_province VARCHAR(50),
    country VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    access_information TEXT,
    parking_available BOOLEAN,
    power_available BOOLEAN,
    water_available BOOLEAN,
    cell_coverage VARCHAR(100),
    radio_club_contact VARCHAR(255),
    website_url VARCHAR(500),
    suggested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'under_review', 'approved', 'rejected') DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_at TIMESTAMP NULL,
    reviewed_by VARCHAR(255),
    created_park_id INTEGER NULL,
    FOREIGN KEY (created_park_id) REFERENCES parks(park_id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_suggested_at (suggested_at),
    INDEX idx_park_name (park_name)
);

-- View for pending suggestions
CREATE OR REPLACE VIEW v_pending_suggestions AS
SELECT 
    suggestion_id,
    suggester_name,
    suggester_call_sign,
    park_name,
    location,
    suggested_at,
    description,
    status
FROM campground_suggestions
WHERE status IN ('pending', 'under_review')
ORDER BY suggested_at DESC;