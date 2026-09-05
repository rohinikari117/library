import sqlite3

def add_massive_book_collection():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # 1st Year (Common for all branches generally, but we can assign to specific branches)
    first_year_books = [
        ('Engineering Mathematics - I', 'B.S. Grewal', 'R20', 'CSE', 1, 1, 'Textbook', '', 'Higher Engineering Mathematics', ''),
        ('Engineering Physics', 'Resnick Halliday', 'R20', 'ECE', 1, 1, 'Textbook', '', 'Fundamentals of Physics', ''),
        ('Engineering Chemistry', 'Jain & Jain', 'R23', 'MECH', 1, 1, 'Textbook', '', 'Engineering Chemistry', ''),
        ('Programming for Problem Solving', 'E. Balagurusamy', 'R20', 'CSE', 1, 1, 'Textbook', '', 'Programming in ANSI C', ''),
        ('Engineering Graphics', 'N.D. Bhatt', 'R20', 'CIVIL', 1, 2, 'Textbook', '', 'Engineering Drawing', ''),
        ('Basic Electrical Engineering', 'V.K. Mehta', 'R23', 'EEE', 1, 2, 'Textbook', '', 'Basic Electrical Engineering', ''),
    ]

    # CSE Core Books
    cse_books = [
        ('Data Structures and Algorithms', 'Narasimha Karumanchi', 'R20', 'CSE', 2, 3, 'Textbook', '', 'Data Structures and Algorithms Made Easy', ''),
        ('Object Oriented Programming using C++', 'E. Balagurusamy', 'R20', 'CSE', 2, 3, 'Workbook', '', 'OOP with C++', ''),
        ('Computer Organization and Architecture', 'William Stallings', 'R23', 'CSE', 2, 4, 'Textbook', '', 'Computer Organization and Architecture', ''),
        ('Design and Analysis of Algorithms', 'Thomas H. Cormen', 'R20', 'CSE', 2, 4, 'Soft copy', '', 'Introduction to Algorithms', ''),
        ('Formal Languages and Automata Theory', 'J.D. Ullman', 'R20', 'CSE', 3, 5, 'Textbook', '', 'Introduction to Automata Theory', ''),
        ('Software Engineering', 'Ian Sommerville', 'R23', 'CSE', 3, 5, 'Textbook', '', 'Software Engineering 10th Edition', ''),
        ('Computer Networks', 'Andrew S. Tanenbaum', 'R20', 'CSE', 3, 6, 'Textbook', '', 'Computer Networks 5th Edition', ''),
        ('Web Technologies', 'Uttam K. Roy', 'R20', 'CSE', 3, 6, 'Workbook', '', 'Web Technologies Oxford', ''),
        ('Artificial Intelligence', 'Stuart Russell', 'R23', 'CSE', 4, 7, 'Textbook', '', 'Artificial Intelligence: A Modern Approach', ''),
        ('Cryptography and Network Security', 'William Stallings', 'R20', 'CSE', 4, 7, 'Textbook', '', 'Principles and Practice', ''),
        ('Cloud Computing', 'Rajkumar Buyya', 'R20', 'CSE', 4, 8, 'Soft copy', '', 'Cloud Computing Principles and Paradigms', ''),
    ]

    # ECE Core Books
    ece_books = [
        ('Electronic Devices and Circuits', 'Jacob Millman', 'R20', 'ECE', 2, 3, 'Textbook', '', 'Electronic Devices and Circuits', ''),
        ('Digital Logic Design', 'M. Morris Mano', 'R23', 'ECE', 2, 3, 'Textbook', '', 'Digital Design', ''),
        ('Analog Communications', 'Simon Haykin', 'R20', 'ECE', 2, 4, 'Textbook', '', 'Communication Systems', ''),
        ('Electromagnetic Waves and Transmission Lines', 'Matthew N.O. Sadiku', 'R20', 'ECE', 2, 4, 'Workbook', '', 'Elements of Electromagnetics', ''),
        ('Digital Signal Processing', 'John G. Proakis', 'R23', 'ECE', 3, 5, 'Textbook', '', 'Digital Signal Processing', ''),
        ('Microprocessors and Microcontrollers', 'A.K. Ray', 'R20', 'ECE', 3, 5, 'Textbook', '', 'Advanced Microprocessors and Peripherals', ''),
        ('Antennas and Wave Propagation', 'John D. Kraus', 'R20', 'ECE', 3, 6, 'Soft copy', '', 'Antennas for All Applications', ''),
        ('VLSI Design', 'Douglas A. Pucknell', 'R23', 'ECE', 3, 6, 'Textbook', '', 'Basic VLSI Design', ''),
        ('Microwave Engineering', 'David M. Pozar', 'R20', 'ECE', 4, 7, 'Textbook', '', 'Microwave Engineering', ''),
        ('Optical Communications', 'Gerd Keiser', 'R20', 'ECE', 4, 7, 'Workbook', '', 'Optical Fiber Communications', ''),
        ('Satellite Communications', 'Timothy Pratt', 'R23', 'ECE', 4, 8, 'Textbook', '', 'Satellite Communications', ''),
    ]

    # MECH Core Books
    mech_books = [
        ('Engineering Mechanics', 'S.S. Bhavikatti', 'R20', 'MECH', 2, 3, 'Textbook', '', 'Engineering Mechanics', ''),
        ('Material Science and Metallurgy', 'O.P. Khanna', 'R23', 'MECH', 2, 3, 'Textbook', '', 'Material Science and Metallurgy', ''),
        ('Kinematics of Machinery', 'R.S. Khurmi', 'R20', 'MECH', 2, 4, 'Textbook', '', 'Theory of Machines', ''),
        ('Manufacturing Technology', 'P.N. Rao', 'R20', 'MECH', 2, 4, 'Workbook', '', 'Manufacturing Technology Vol 1 & 2', ''),
        ('Dynamics of Machinery', 'S.S. Rattan', 'R23', 'MECH', 3, 5, 'Textbook', '', 'Theory of Machines', ''),
        ('Heat and Mass Transfer', 'R.K. Rajput', 'R20', 'MECH', 3, 5, 'Soft copy', '', 'Heat and Mass Transfer', ''),
        ('Design of Machine Elements', 'V.B. Bhandari', 'R20', 'MECH', 3, 6, 'Textbook', '', 'Design of Machine Elements', ''),
        ('CAD/CAM', 'P.N. Rao', 'R23', 'MECH', 3, 6, 'Textbook', '', 'CAD/CAM Principles and Applications', ''),
        ('Operations Research', 'Hira & Gupta', 'R20', 'MECH', 4, 7, 'Workbook', '', 'Operations Research', ''),
        ('Finite Element Analysis', 'S.S. Rao', 'R20', 'MECH', 4, 7, 'Textbook', '', 'The Finite Element Method in Engineering', ''),
        ('Automobile Engineering', 'Kirpal Singh', 'R23', 'MECH', 4, 8, 'Textbook', '', 'Automobile Engineering Vol 1 & 2', ''),
    ]

    # CIVIL Core Books
    civil_books = [
        ('Building Materials', 'S.K. Duggal', 'R20', 'CIVIL', 2, 3, 'Textbook', '', 'Building Materials', ''),
        ('Surveying', 'B.C. Punmia', 'R23', 'CIVIL', 2, 3, 'Workbook', '', 'Surveying Vol 1', ''),
        ('Fluid Mechanics', 'A.K. Jain', 'R20', 'CIVIL', 2, 4, 'Textbook', '', 'Fluid Mechanics', ''),
        ('Structural Analysis', 'C.S. Reddy', 'R20', 'CIVIL', 2, 4, 'Textbook', '', 'Basic Structural Analysis', ''),
        ('Geotechnical Engineering', 'K.R. Arora', 'R23', 'CIVIL', 3, 5, 'Soft copy', '', 'Soil Mechanics and Foundation Engineering', ''),
        ('Design of Concrete Structures', 'N. Krishna Raju', 'R20', 'CIVIL', 3, 5, 'Textbook', '', 'Design of Reinforced Concrete Structures', ''),
        ('Transportation Engineering', 'S.K. Khanna', 'R20', 'CIVIL', 3, 6, 'Textbook', '', 'Highway Engineering', ''),
        ('Environmental Engineering', 'S.K. Garg', 'R23', 'CIVIL', 3, 6, 'Workbook', '', 'Water Supply Engineering', ''),
        ('Design of Steel Structures', 'S.K. Duggal', 'R20', 'CIVIL', 4, 7, 'Textbook', '', 'Design of Steel Structures', ''),
        ('Estimation and Costing', 'B.N. Dutta', 'R20', 'CIVIL', 4, 7, 'Textbook', '', 'Estimating and Costing in Civil Engineering', ''),
        ('Construction Management', 'P.S. Gahlot', 'R23', 'CIVIL', 4, 8, 'Textbook', '', 'Construction Planning and Management', ''),
    ]

    # EEE Core Books
    eee_books = [
        ('Network Analysis', 'M.E. Van Valkenburg', 'R20', 'EEE', 2, 3, 'Textbook', '', 'Network Analysis', ''),
        ('Electrical Machines - I', 'P.S. Bimbhra', 'R23', 'EEE', 2, 3, 'Workbook', '', 'Electrical Machinery', ''),
        ('Power Systems - I', 'J.B. Gupta', 'R20', 'EEE', 2, 4, 'Textbook', '', 'A Course in Power Systems', ''),
        ('Electrical Measurements', 'A.K. Sawhney', 'R20', 'EEE', 2, 4, 'Textbook', '', 'Electrical and Electronic Measurements', ''),
        ('Control Systems', 'Benjamin C. Kuo', 'R23', 'EEE', 3, 5, 'Soft copy', '', 'Automatic Control Systems', ''),
        ('Power Electronics', 'P.S. Bimbhra', 'R20', 'EEE', 3, 5, 'Textbook', '', 'Power Electronics', ''),
        ('Switchgear and Protection', 'Sunil S. Rao', 'R20', 'EEE', 3, 6, 'Textbook', '', 'Switchgear Protection and Power Systems', ''),
        ('Electric Drives', 'G.K. Dubey', 'R23', 'EEE', 3, 6, 'Workbook', '', 'Fundamentals of Electrical Drives', ''),
        ('Power System Operation and Control', 'P.S.R. Murty', 'R20', 'EEE', 4, 7, 'Textbook', '', 'Power System Operation and Control', ''),
        ('High Voltage Engineering', 'M.S. Naidu', 'R20', 'EEE', 4, 7, 'Textbook', '', 'High Voltage Engineering', ''),
        ('Renewable Energy Sources', 'G.D. Rai', 'R23', 'EEE', 4, 8, 'Textbook', '', 'Non-Conventional Energy Sources', ''),
    ]

    all_books = first_year_books + cse_books + ece_books + mech_books + civil_books + eee_books

    c.executemany('''
        INSERT INTO books (title, author, regulation, branch, year, semester, type, file_path, description, cover_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', all_books)
    
    conn.commit()
    conn.close()
    print(f"Massive collection of {len(all_books)} books added successfully.")

if __name__ == '__main__':
    add_massive_book_collection()
