import csv

def calculate_type_char(password): # lowercase, uppercase, number, symbol
    num_type = 0
    lowercase_present = any(char.islower() for char in password)
    uppercase_present = any(char.isupper() for char in password)
    digits_present = any(char.isdigit() for char in password)
    symbols_present = any(not char.isalnum() for char in password)

    if lowercase_present: num_type += 1
    if uppercase_present: num_type += 1
    if digits_present: num_type += 1
    if symbols_present: num_type += 1
    return num_type

def calculate_dup_char(password): # calculate char appear twice or more
    ascii_char = [0 for i in range (256)]
    num_rep = 0
    for char in password:
        if ascii_char[ord(char)] == 0: ascii_char[ord(char)] += 1
        elif ascii_char[ord(char)] == 1:
            num_rep += 1
            ascii_char[ord(char)] += 1
    return num_rep

def calculate_unique_char(password): # calculate different chars used  
    return len(set(password))

def calculate_consecutive_LC(password): 
    temp = ""
    count = 0
    for a in password:
        if a.islower():
            if temp == a:
                count += 1
            temp = a
    return count

def calculate_consecutive_UC(password): 
    temp = ""
    count = 0
    for a in password:
        if a.isupper():
            if temp == a:
                count += 1
            temp = a
    return count

def calculate_consecutive_number(password): 
    temp = ""
    count = 0
    for a in password:
        if a.isdecimal():
            if temp == a:
                count += 1
            temp = a
    return count

def calculate_sequence_character(password): 
    Alphabet = "abcdefghijklmnopqrstuvwxyz"
    Number = "0123456789"
    count = 0
    for s in range (len(Alphabet) - 2):
        AlphaFwd = Alphabet[s : s + 3]
        AlphaRev = AlphaFwd[::-1]
        if AlphaFwd in password.lower() or AlphaRev in password.lower():
            count += 1

    for s in range (len(Number) - 2):
        NumFwd = Number[s : s + 3]
        NumRev = NumFwd[::-1]
        if NumFwd in password.lower() or NumRev in password.lower():
            count += 1

    return count

if __name__ == "__main__":
    with open('dataset.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)

        headers = csv_reader.fieldnames + ['types_of_character', 'duplicate_character', 'unique_character', 'consecutive_LC', 'consecutive_UC', 'consecutive_number', 'sequence_character']

        headers.remove('entropy')
        headers.remove('crack_time_sec')
        headers.remove('crack_time')

        with open('data/update_dataset.csv', 'w', newline='') as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=headers)
            csv_writer.writeheader()

            for row in rows:
                row = {key: row[key] for key in row if key in headers}
                row['types_of_character'] = str(calculate_type_char(row['password']))
                row['duplicate_character'] = str(calculate_dup_char(row['password']))
                row['unique_character'] = str(calculate_unique_char(row['password']))
                row['consecutive_LC'] = str(calculate_consecutive_LC(row['password']))
                row['consecutive_UC'] = str(calculate_consecutive_UC(row['password']))
                row['consecutive_number'] = str(calculate_consecutive_number(row['password']))
                row['sequence_character'] = str(calculate_sequence_character(row['password']))
                csv_writer.writerow(row)
