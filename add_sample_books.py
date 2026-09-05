import sqlite3

def add_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    books = [
        # CSE
        ('Operating Systems', 'Silberschatz', 'R20', 'CSE', 3, 5, 'Textbook', '', 'Comprehensive guide to OS concepts', ''),
        ('Database Management Systems', 'Raghu Ramakrishnan', 'R23', 'CSE', 2, 4, 'Textbook', '', 'Deep dive into databases', ''),
        ('Machine Learning Basics', 'Andrew Ng', 'R20', 'CSE', 4, 7, 'Soft copy', '', 'Introductory concepts to ML', ''),
        
        # ECE
        ('Signals and Systems', 'Alan V. Oppenheim', 'R20', 'ECE', 2, 3, 'Textbook', '', 'Foundations of Signals and Systems', ''),
        ('VLSI Design', 'Neil Weste', 'R23', 'ECE', 3, 6, 'Textbook', '', 'CMOS VLSI Design', ''),
        ('Microprocessors', 'Ramesh Gaonkar', 'R20', 'ECE', 3, 5, 'Workbook', '', '8085 Microprocessor Architecture', ''),

        # MECH
        ('Thermodynamics', 'P.K. Nag', 'R20', 'MECH', 2, 3, 'Textbook', '', 'Engineering Thermodynamics', ''),
        ('Fluid Mechanics', 'R.K. Bansal', 'R23', 'MECH', 2, 4, 'Textbook', '', 'Fluid Mechanics and Hydraulic Machines', ''),
        ('Machine Design', 'V.B. Bhandari', 'R20', 'MECH', 3, 6, 'Soft copy', '', 'Design of Machine Elements', ''),

        # CIVIL
        ('Strength of Materials', 'R.K. Rajput', 'R20', 'CIVIL', 2, 3, 'Textbook', '', 'Basic concepts of solid mechanics', ''),
        ('Surveying', 'B.C. Punmia', 'R23', 'CIVIL', 2, 4, 'Textbook', '', 'Surveying principles and practices', ''),
        ('Structural Analysis', 'R.C. Hibbeler', 'R20', 'CIVIL', 3, 5, 'Workbook', '', 'Analysis of statically determinate structures', ''),

        # EEE
        ('Electrical Machines', 'P.S. Bimbhra', 'R20', 'EEE', 2, 3, 'Textbook', '', 'Generalized theory of electrical machines', ''),
        ('Power Systems', 'C.L. Wadhwa', 'R23', 'EEE', 3, 5, 'Textbook', '', 'Generation, transmission and distribution', ''),
        ('Control Systems', 'I.J. Nagrath', 'R20', 'EEE', 3, 6, 'Soft copy', '', 'Linear control systems', '')
    ]
    
    c.executemany('''
        INSERT INTO books (title, author, regulation, branch, year, semester, type, file_path, description, cover_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', books)
    
    conn.commit()
    conn.close()
    print("Sample books added successfully.")

if __name__ == '__main__':
    add_books()
