-- Insert sample subjects
INSERT INTO subjects (name, level, description) VALUES
('Mathematics', 'High School', 'Includes algebra, calculus, and geometry'),
('Physics', 'High School', 'Classical mechanics, thermodynamics, and modern physics'),
('Chemistry', 'High School', 'Organic and inorganic chemistry'),
('Biology', 'High School', 'Cell biology, genetics, and human anatomy'),
('English', 'All Levels', 'Grammar, literature, and composition'),
('History', 'All Levels', 'World history and local history'),
('Geography', 'All Levels', 'Physical and human geography'),
('Computer Science', 'High School', 'Programming and computer concepts');

-- Insert sample tutors (password is 'password123' for all)
INSERT INTO tutors (email, password_hash, name, qualification, experience, bio, is_verified, phone) VALUES
('john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'John Doe', 'M.Sc. Mathematics', '5+ years teaching experience', 'Passionate about making mathematics easy to understand', TRUE, '+1234567890'),
('jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Jane Smith', 'Ph.D. Physics', '8+ years teaching experience', 'Expert in physics with research background', TRUE, '+1234567891'),
('mike.wilson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Mike Wilson', 'M.A. English Literature', '6+ years teaching experience', 'Specializing in literature and creative writing', TRUE, '+1234567892');

-- Insert sample users (students/parents) (password is 'password123' for all)
INSERT INTO users (email, password_hash, name, is_admin, phone) VALUES
('student1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Alex Johnson', FALSE, '+1234567893'),
('student2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Sarah Williams', FALSE, '+1234567894'),
('student3@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6f.CbP9BYe', 'Tom Brown', FALSE, '+1234567895');

-- Insert sample testimonials
INSERT INTO testimonials (user_id, tutor_id, rating, comment, created_at) VALUES
(1, 1, 5, 'Excellent tutor! Made mathematics so much easier to understand. Highly recommended!', NOW()),
(2, 1, 5, 'Great teaching methods and very patient. My grades improved significantly.', NOW()),
(3, 2, 5, 'Dr. Smith is an amazing physics tutor. Complex concepts are explained clearly.', NOW()),
(1, 3, 4, 'Very helpful and knowledgeable in English literature. Great communication skills.', NOW());

-- Insert sample bookings
INSERT INTO bookings (user_id, tutor_id, subject_id, booking_date, status) VALUES
(1, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'confirmed'),
(2, 2, 2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'confirmed'),
(3, 3, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'pending'); 