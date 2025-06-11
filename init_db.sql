-- Drop database if exists
DROP DATABASE IF EXISTS home_tuition;

-- Create database
CREATE DATABASE home_tuition;
USE home_tuition;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create tutors table
CREATE TABLE tutors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    qualification VARCHAR(200),
    experience TEXT,
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Create subjects table
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL
);

-- Create bookings table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tutor_id INT,
    subject_id INT,
    booking_date DATE NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tutor_id) REFERENCES tutors(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- Create testimonials table
CREATE TABLE testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tutor_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tutor_id) REFERENCES tutors(id)
);

-- Create contact_messages table
CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'unread'
);

-- Insert admin user

INSERT INTO users (email, password_hash, name, is_admin) 
VALUES ('admin@hometuition.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Admin', TRUE);

-- Insert sample subjects
INSERT INTO subjects (name, level) VALUES
('Mathematics', 'High School'),
('Physics', 'High School'),
('Chemistry', 'High School'),
('English', 'All Levels'); 