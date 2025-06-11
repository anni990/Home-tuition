-- Create database
CREATE DATABASE IF NOT EXISTS home_tuition;
USE home_tuition;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tutors table
CREATE TABLE tutors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    qualification VARCHAR(200),
    experience TEXT,
    bio TEXT,
    profile_image VARCHAR(255),
    hourly_rate DECIMAL(10,2),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subjects table
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    level VARCHAR(50) NOT NULL
);

-- Tutor_subjects (Many-to-Many relationship)
CREATE TABLE tutor_subjects (
    tutor_id INT,
    subject_id INT,
    PRIMARY KEY (tutor_id, subject_id),
    FOREIGN KEY (tutor_id) REFERENCES tutors(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

-- Bookings table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tutor_id INT,
    subject_id INT,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (tutor_id) REFERENCES tutors(id) ON DELETE SET NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL
);

-- Testimonials table
CREATE TABLE testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tutor_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (tutor_id) REFERENCES tutors(id) ON DELETE CASCADE
);

-- Contact messages table
CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

-- Insert admin user
INSERT INTO users (email, password_hash, name, is_admin) 
VALUES ('admin@hometuition.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Admin', TRUE);

-- Insert some sample subjects
INSERT INTO subjects (name, description, level) VALUES
('Mathematics', 'Includes algebra, calculus, and geometry', 'High School'),
('Physics', 'Classical mechanics, thermodynamics, and more', 'High School'),
('Chemistry', 'Organic and inorganic chemistry', 'High School'),
('English', 'Grammar, literature, and composition', 'All Levels'),
('Biology', 'Cell biology, genetics, and human anatomy', 'High School'); 