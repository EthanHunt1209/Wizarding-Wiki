from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Balu@2005',
    'database': 'harry_potter_db'
}

def create_database():
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute("DROP DATABASE IF EXISTS harry_potter_db")
        cursor.execute("CREATE DATABASE harry_potter_db")
        cursor.execute("USE harry_potter_db")
        
        # Create tables with additional fields for future use
        cursor.execute("""
             CREATE TABLE characters ( 
             id INT PRIMARY KEY,
             name VARCHAR(100),
             date_of_birth DATE,
             blood_status VARCHAR(20),
             house VARCHAR(30),
             marital_status VARCHAR(20),
             also_known_as VARCHAR(255),
             book_appearances VARCHAR(255)
             )
        """)
        
        cursor.execute("""
            CREATE TABLE creatures (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            species VARCHAR(100),
            notable_role TEXT,
            book_appearances VARCHAR(20)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE spells (
            id INT PRIMARY KEY,
            spell_name VARCHAR(100),
            what_it_does TEXT,
            users VARCHAR(255),
            book_appearances VARCHAR(20)
            )
        """)
        
        # Clear existing data to remove duplicates
        cursor.execute("DELETE FROM characters")
        cursor.execute("DELETE FROM creatures")
        cursor.execute("DELETE FROM spells")
        
        # Insert character data
        cursor.execute("""
            INSERT INTO characters (id, name, date_of_birth, blood_status, house, marital_status, also_known_as, book_appearances) VALUES
            (1, 'Harry Potter', '1980-07-31', 'Half-blood', 'Gryffindor', 'Single', 'The Boy Who Lived; The Chosen One', '1,2,3,4,5,6,7'),
            (2, 'Ron Weasley', '1980-03-01', 'Pure-blood', 'Gryffindor', 'Married', 'Wheezy', '1,2,3,4,5,6,7'),
            (3, 'Hermione Granger', '1979-09-19', 'Muggle-born', 'Gryffindor', 'Married', 'Brightest Witch of Her Age', '1,2,3,4,5,6,7'),
            (4, 'Voldemort', '1926-12-31', 'Half-blood', 'Slytherin', 'Single', 'Tom Riddle; He-Who-Must-Not-Be-Named', '1,2,4,5,6,7'),
            (5, 'Albus Dumbledore', '1881-08-12', 'Half-blood', 'Gryffindor', 'Single', 'Headmaster of Hogwarts; Leader of the Order', '1,2,3,4,5,6'),
            (6, 'Severus Snape', '1960-01-09', 'Half-blood', 'Slytherin', 'Single', 'The Half-Blood Prince', '1,2,3,4,5,6,7'),
            (7, 'Draco Malfoy', '1980-06-05', 'Pure-blood', 'Slytherin', 'Married', 'Draco', '1,2,3,4,5,6,7'),
            (8, 'Rubeus Hagrid', '1928-12-06', 'Half-blood', 'Gryffindor', 'Single', 'Keeper of Keys and Grounds', '1,2,3,4,5,6,7'),
            (9, 'Minerva McGonagall', '1935-10-04', 'Half-blood', 'Gryffindor', 'Widowed', 'Deputy Headmistress; Animagus', '1,2,3,4,5,6,7'),
            (10, 'Sirius Black', '1959-11-03', 'Pure-blood', 'Gryffindor', 'Single', 'Padfoot', '3,4,5'),
            (11, 'Neville Longbottom', '1980-07-30', 'Pure-blood', 'Gryffindor', 'Married', 'Neville', '1,2,3,4,5,6,7'),
            (12, 'Ginny Weasley', '1981-08-11', 'Pure-blood', 'Gryffindor', 'Married', 'Ginny', '2,3,4,5,6,7'),
            (13, 'Luna Lovegood', '1981-02-13', 'Pure-blood', 'Ravenclaw', 'Married', 'Loony', '5,6,7'),
            (14, 'Lucius Malfoy', '1954-10-29', 'Pure-blood', 'Slytherin', 'Married', 'Death Eater', '2,4,5,7'),
            (15, 'Bellatrix Lestrange', '1951-11-12', 'Pure-blood', 'Slytherin', 'Married', 'Bella', '5,6,7'),
            (16, 'Remus Lupin', '1960-03-10', 'Half-blood', 'Gryffindor', 'Married', 'Moony', '3,5,6,7'),
            (17, 'Peter Pettigrew', '1960-04-20', 'Pure-blood', 'Gryffindor', 'Single', 'Wormtail', '3,4,5,6,7'),
            (18, 'Nymphadora Tonks', '1973-10-16', 'Half-blood', 'Hufflepuff', 'Married', 'Tonks', '5,6,7'),
            (19, 'Dolores Umbridge', '1961-08-26', 'Half-blood', 'Slytherin', 'Single', 'Senior Undersecretary', '5,7'),
            (20, 'Gellert Grindelwald', '1883-01-01', 'Pure-blood', 'Durmstrang', 'Single', 'Dark Wizard', '7'),
            (21, 'Arthur Weasley', '1950-02-06', 'Pure-blood', 'Gryffindor', 'Married', 'Father of the Weasley Family', '2,4,5,6,7'),
            (22, 'Molly Weasley', '1949-10-30', 'Pure-blood', 'Gryffindor', 'Married', 'Mother of the Weasley Family', '2,4,5,6,7'),
            (23, 'Fred Weasley', '1978-04-01', 'Pure-blood', 'Gryffindor', 'Single', 'One of the Weasley Twins', '2,3,4,5,6,7'),
            (24, 'George Weasley', '1978-04-01', 'Pure-blood', 'Gryffindor', 'Married', 'One of the Weasley Twins', '2,3,4,5,6,7'),
            (25, 'Percy Weasley', '1976-08-22', 'Pure-blood', 'Gryffindor', 'Married', 'Head Boy; Ministry Official', '1,2,3,4,5,6,7'),
            (26, 'Bill Weasley', '1970-11-29', 'Pure-blood', 'Gryffindor', 'Married', 'Curse Breaker', '4,5,6,7'),
            (27, 'Charlie Weasley', '1972-12-12', 'Pure-blood', 'Gryffindor', 'Single', 'Dragon Expert', '1,4'),
            (28, 'Fleur Delacour', '1977-02-05', 'Half-blood', 'Beauxbatons', 'Married', 'Triwizard Champion', '4,6,7'),
            (29, 'Gilderoy Lockhart', '1964-01-26', 'Half-blood', 'Ravenclaw', 'Single', 'Fraud Author', '2'),
            (30, 'Horace Slughorn', '1882-04-28', 'Pure-blood', 'Slytherin', 'Single', 'Potion Master', '6,7'),
            (31, 'Sybill Trelawney', '1960-03-09', 'Half-blood', 'Ravenclaw', 'Single', 'Divination Professor', '3,5,6,7'),
            (32, 'Pomona Sprout', '1941-05-15', 'Half-blood', 'Hufflepuff', 'Single', 'Herbology Professor', '2,5,7'),
            (33, 'Filius Flitwick', '1940-10-17', 'Half-blood', 'Ravenclaw', 'Single', 'Charms Master', '1,2,3,4,5,6,7'),
            (34, 'Poppy Pomfrey', '1945-12-24', 'Half-blood', 'Gryffindor', 'Single', 'Madam Pomfrey', '1,2,3,4,5,6,7'),
            (35, 'Frank Longbottom', '1960-03-12', 'Pure-blood', 'Gryffindor', 'Married', 'Auror, Neville''s Father', '5,7'),
            (36, 'Dudley Dursley', '1980-06-23', 'Muggle', 'Not a Hogwarts student', 'Married', 'Big D', '1,2,3,4,5,6,7'),
            (37, 'Vernon Dursley', '1953-08-28', 'Muggle', 'Not a Hogwarts student', 'Married', 'Uncle Vernon', '1,2,3,4,5,6,7'),
            (38, 'Petunia Dursley', '1958-09-07', 'Muggle', 'Not a Hogwarts student', 'Married', 'Aunt Petunia', '1,2,3,4,5,6,7'),
            (39, 'Marge Dursley', '1950-11-20', 'Muggle', 'Not a Hogwarts student', 'Single', 'Aunt Marge', '3'),
            (40, 'Hepzibah Smith', '1872-04-16', 'Pure-blood', 'Hufflepuff', 'Single', 'Hufflepuff''s descendant', '6'),
            (41, 'Cornelius Fudge', '1955-07-15', 'Pure-blood', 'Not a Hogwarts student', 'Married', 'Minister of Magic', '2,3,4,5'),
            (42, 'Rufus Scrimgeour', '1961-10-05', 'Pure-blood', 'Not a Hogwarts student', 'Married', 'Minister for Magic', '6,7'),
            (43, 'Barty Crouch Sr.', '1930-11-18', 'Pure-blood', 'Not a Hogwarts student', 'Married', 'Ministry Official', '4'),
            (44, 'Barty Crouch Jr.', '1962-06-21', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '4'),
            (45, 'Fenrir Greyback', '1959-02-14', 'Werewolf', 'Not a Hogwarts student', 'Single', 'Dark Werewolf', '6,7'),
            (46, 'Narcissa Malfoy', '1955-05-19', 'Pure-blood', 'Slytherin', 'Married', 'Cissy', '5,6,7'),
            (47, 'Yaxley', '1960-01-15', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '7'),
            (48, 'Pius Thicknesse', '1965-07-12', 'Pure-blood', 'Not a Hogwarts student', 'Married', 'Imperiused Minister', '7'),
            (49, 'Thorfinn Rowle', '1960-02-09', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '6,7'),
            (50, 'Dean Thomas', '1980-09-03', 'Muggle-born', 'Gryffindor', 'Single', 'Dean', '1,2,3,4,5,7'),
            (51, 'Seamus Finnigan', '1980-09-15', 'Half-blood', 'Gryffindor', 'Single', 'Seamus', '1,2,3,4,5,6,7'),
            (52, 'Lee Jordan', '1979-04-09', 'Half-blood', 'Gryffindor', 'Single', 'Quidditch Commentator', '1,2,3,5'),
            (53, 'Angelina Johnson', '1977-12-07', 'Half-blood', 'Gryffindor', 'Married', 'Quidditch Captain', '2,3,4,5'),
            (54, 'Lavender Brown', '1980-05-30', 'Half-blood', 'Gryffindor', 'Single', 'Lavender', '1,2,5,6'),
            (55, 'Parvati Patil', '1980-04-19', 'Pure-blood', 'Gryffindor', 'Single', 'Parvati', '4,5,6,7'),
            (56, 'Padma Patil', '1980-04-19', 'Pure-blood', 'Ravenclaw', 'Single', 'Padma', '4,5,7'),
            (57, 'Zacharias Smith', '1980-07-12', 'Pure-blood', 'Hufflepuff', 'Single', 'Zacharias', '5,6,7'),
            (58, 'Ernie Macmillan', '1980-02-10', 'Pure-blood', 'Hufflepuff', 'Single', 'Ernie', '2,5,6,7'),
            (59, 'Justin Finch-Fletchley', '1980-05-28', 'Muggle-born', 'Hufflepuff', 'Single', 'Justin', '2,5'),
            (60, 'Kingsley Shacklebolt', '1959-08-10', 'Pure-blood', 'Not a Hogwarts student', 'Single', 'Auror', '5,6,7'),
            (61, 'Aberforth Dumbledore', '1884-03-15', 'Half-blood', 'Gryffindor', 'Single', 'Barman of the Hog''s Head', '5,6,7'),
            (62, 'Elphias Doge', '1881-12-21', 'Pure-blood', 'Gryffindor', 'Single', 'Order Member', '5,7'),
            (63, 'Mundungus Fletcher', '1960-11-06', 'Half-blood', 'Not a Hogwarts student', 'Single', 'Dung', '5,6,7'),
            (64, 'Andromeda Tonks', '1953-04-02', 'Pure-blood', 'Slytherin', 'Married', 'Dromeda', '7'),
            (65, 'Ted Tonks', '1950-06-19', 'Muggle-born', 'Hufflepuff', 'Married', 'Edward Tonks', '7'),
            (66, 'Dirk Cresswell', '1960-07-24', 'Muggle-born', 'Ravenclaw', 'Married', 'Dirk', '7'),
            (67, 'Cedric Diggory', '1977-09-01', 'Pure-blood', 'Hufflepuff', 'Single', 'Champion', '3,4'),
            (68, 'Viktor Krum', '1976-12-05', 'Pure-blood', 'Durmstrang', 'Single', 'International Quidditch Seeker', '4,7'),
            (69, 'Rita Skeeter', '1951-11-07', 'Half-blood', 'Slytherin', 'Single', 'Journalist', '4,5,7'),
            (70, 'Xenophilius Lovegood', '1960-09-18', 'Pure-blood', 'Ravenclaw', 'Married', 'Editor of The Quibbler', '7'),
            (71, 'Mad-Eye Moody', '1939-01-05', 'Pure-blood', 'Gryffindor', 'Single', 'Auror', '4,5,7'),
            (72, 'Charity Burbage', '1958-06-29', 'Muggle-born', 'Not a Hogwarts student', 'Single', 'Muggle Studies Professor', '7'),
            (73, 'Mafalda Hopkirk', '1955-02-13', 'Pure-blood', 'Not a Hogwarts student', 'Single', 'Ministry Official', '5,7'),
            (74, 'Travers', '1957-03-23', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '7'),
            (75, 'Scabior', '1975-05-15', 'Half-blood', 'Not a Hogwarts student', 'Single', 'Snatcher', '7'),
            (76, 'Antonin Dolohov', '1950-09-01', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '5,7'),
            (77, 'Reginald Cattermole', '1960-08-20', 'Half-blood', 'Gryffindor', 'Married', 'Ministry Employee', '7'),
            (78, 'Albert Runcorn', '1961-11-11', 'Pure-blood', 'Not a Hogwarts student', 'Married', 'Ministry Official', '7'),
            (79, 'Mary Cattermole', '1962-04-28', 'Half-blood', 'Not a Hogwarts student', 'Married', 'Ministry Employee''s Wife', '7'),
            (80, 'Wilkie Twycross', '1940-05-03', 'Pure-blood', 'Ravenclaw', 'Single', 'Apparition Instructor', '6'),
            (81, 'Garrick Ollivander', '1909-09-25', 'Pure-blood', 'Ravenclaw', 'Single', 'Wandmaker', '1,4,5,7'),
            (82, 'Irma Pince', '1940-05-14', 'Half-blood', 'Ravenclaw', 'Single', 'Librarian', '2,5'),
            (83, 'Caractacus Burke', '1892-08-17', 'Pure-blood', 'Slytherin', 'Single', 'Co-owner of Borgin and Burkes', '6'),
            (84, 'Borgin', '1920-10-02', 'Pure-blood', 'Slytherin', 'Single', 'Shopkeeper', '2,6'),
            (85, 'Roger Davies', '1978-07-02', 'Pure-blood', 'Ravenclaw', 'Single', 'Ravenclaw Quidditch Captain', '4'),
            (86, 'Michael Corner', '1980-01-20', 'Half-blood', 'Ravenclaw', 'Single', 'DA Member', '5,6,7'),
            (87, 'Terry Boot', '1980-02-12', 'Half-blood', 'Ravenclaw', 'Single', 'DA Member', '5,7'),
            (88, 'Susan Bones', '1980-06-11', 'Half-blood', 'Hufflepuff', 'Single', 'Susan', '2,5,6'),
            (89, 'Cormac McLaggen', '1978-04-04', 'Pure-blood', 'Gryffindor', 'Single', 'Cormac', '6'),
            (90, 'Blaise Zabini', '1980-09-25', 'Pure-blood', 'Slytherin', 'Single', 'Blaise', '6'),
            (91, 'Gregory Goyle', '1980-08-12', 'Pure-blood', 'Slytherin', 'Single', 'Goyle', '1,2,3,4,5,6,7'),
            (92, 'Vincent Crabbe', '1980-08-12', 'Pure-blood', 'Slytherin', 'Single', 'Crabbe', '1,2,3,4,5,6,7'),
            (93, 'Walden Macnair', '1950-06-06', 'Pure-blood', 'Slytherin', 'Single', 'Executioner', '3,5,7'),
            (94, 'Augustus Rookwood', '1955-09-30', 'Pure-blood', 'Slytherin', 'Single', 'Death Eater', '5,7'),
            (95, 'Gawain Robards', '1962-10-18', 'Pure-blood', 'Ravenclaw', 'Single', 'Head of Auror Office', '7'),
            (96, 'Daphne Greengrass', '1980-07-24', 'Pure-blood', 'Slytherin', 'Married', 'Daphne', '5,6,7'),
            (97, 'Astoria Greengrass', '1982-08-14', 'Pure-blood', 'Slytherin', 'Married', 'Astoria Malfoy', '7'),
            (98, 'Melinda Bobbin', '1980-03-17', 'Half-blood', 'Hufflepuff', 'Single', 'Melinda', '5'),
            (99, 'Theodore Nott', '1980-06-25', 'Pure-blood', 'Slytherin', 'Single', 'Theo', '5,6,7'),
            (100, 'Amos Diggory', '1960-07-19', 'Pure-blood', 'Hufflepuff', 'Married', 'Cedric''s Father', '4,7')
        """)
        
        # Creatures
        creatures = [
            (1, 'Dobby', 'House-elf', 'Freed by Harry, loyal, dies in Book 7', '2,4,5,7'),
            (2, 'Kreacher', 'House-elf', 'Black family elf, helps Harry in Book 7', '5,6,7'),
            (3, 'Winky', 'House-elf', 'Crouch family elf, dismissed', '4'),
            (4, 'Hokey', 'House-elf', 'Hepzibah Smith\'s elf, framed for murder', '6'),
            (5, 'Griphook', 'Goblin', 'Gringotts goblin, helps break-in, betrays trio', '1,7'),
            (6, 'Bogrod', 'Goblin', 'Bewitched during Gringotts break-in', '7'),
            (7, 'Ragnok', 'Goblin', 'Mentioned as goblin leader', '5,7'),
            (8, 'Gornuk', 'Goblin', 'Travels with Ted Tonks and Dean, killed', '7'),
            (9, 'Firenze', 'Centaur', 'Divination professor, exiled by herd', '1,5,6'),
            (10, 'Bane', 'Centaur', 'Hostile to humans', '1,5,7'),
            (11, 'Ronan', 'Centaur', 'Peaceful and wise centaur', '1,5'),
            (12, 'Buckbeak', 'Hippogriff', 'Saved by Harry, later lives with Hagrid', '3,5,6,7'),
            (13, 'Norberta', 'Norwegian Ridgeback', 'Raised by Hagrid, revealed female', '1,7'),
            (14, 'Aragog', 'Acromantula', 'Hagrid\'s giant spider, dies in Book 6', '2,4,6'),
            (15, 'Shelob', 'Acromantula', 'Aragog\'s mate (mentioned)', '6'),
            (16, 'Fluffy', 'Three-headed Dog', 'Guarded the Philosopher\'s Stone', '1'),
            (17, 'Fawkes', 'Phoenix', 'Dumbledore\'s loyal companion', '2,5,6'),
            (18, 'Hedwig', 'Owl', 'Harry\'s companion, killed in Book 7', '1,2,3,4,5,6,7'),
            (19, 'Pigwidgeon', 'Owl', 'Ron\'s owl from Sirius', '4,5,6,7'),
            (20, 'Errol', 'Owl', 'Elderly Weasley family owl', '2,3,4'),
            (21, 'Crookshanks', 'Cat', 'Hermione\'s intelligent pet', '3,4,5'),
            (22, 'Trevor', 'Toad', 'Neville\'s frequently lost pet', '1,2,3,4'),
            (23, 'Fang', 'Boarhound', 'Hagrid\'s large but cowardly dog', '1,2,3,4,5,6,7'),
            (24, 'Mrs Norris', 'Cat', 'Filch\'s alert and intelligent pet', '1,2,3,4,5,6,7'),
            (25, 'The Grey Lady', 'Ghost', 'Ravenclaw ghost, reveals diadem location', '1,7'),
            (26, 'Nearly Headless Nick', 'Ghost', 'Gryffindor house ghost, resident of Hogwarts', '1,2,3,4,5,7'),
            (27, 'The Bloody Baron', 'Ghost', 'Slytherin house ghost, silent and intimidating', '1,2,5,7'),
            (28, 'The Fat Friar', 'Ghost', 'Hufflepuff house ghost, kind and cheerful', '1'),
            (29, 'Peeves', 'Poltergeist', 'Mischievous spirit at Hogwarts', '1,2,3,4,5'),
            (30, 'Nagini', 'Snake', 'Voldemort\'s companion and Horcrux', '4,6,7'),
            (31, 'The Basilisk', 'Serpent', 'Monster of the Chamber of Secrets', '2'),
            (32, 'Thestrals', 'Thestral', 'Pulled Hogwarts carriages, visible to few', '5,6,7'),
            (33, 'Grawp', 'Giant', 'Hagrid\'s half-brother', '5,6,7'),
            (34, 'Karkus', 'Giant', 'Former Gurg of the giants', '5'),
            (35, 'Morholt', 'Giant', 'Briefly mentioned, killed by Death Eaters', '5'),
            (36, 'The Hungarian Horntail', 'Dragon', 'Fought by Harry in Triwizard Tournament', '4'),
            (37, 'The Swedish Short-Snout', 'Dragon', 'Another dragon in the Triwizard Tournament', '4'),
            (38, 'The Common Welsh Green', 'Dragon', 'Triwizard dragon', '4'),
            (39, 'The Chinese Fireball', 'Dragon', 'Faced by Krum in Triwizard Tournament', '4'),
            (40, 'The Ukrainian Ironbelly', 'Dragon', 'Guards Gringotts vaults', '7'),
            (41, 'The Murtlap', 'Creature', 'Bites Dudley, mentioned in DA notes', '5'),
            (42, 'The Boggart', 'Shapeshifter', 'Takes the form of people\'s fears', '3'),
            (43, 'The Niffler', 'Creature', 'Treasure-loving, mentioned by Hagrid', '4'),
            (44, 'The Blast-Ended Skrewt', 'Hybrid Creature', 'Created by Hagrid, dangerous', '4'),
            (45, 'The Cornish Pixies', 'Creature', 'Mischievous, unleashed by Lockhart', '2'),
            (46, 'The Dementors', 'Dark Creature', 'Azkaban guards, feed on happiness', '3,4,5,6'),
            (47, 'The Veela', 'Spirit', 'Enchanting spirits at the Quidditch World Cup', '4'),
            (48, 'The Acromantula Colony', 'Acromantula', 'Aragog\'s giant spider descendants', '2,6'),
            (49, 'The Merpeople', 'Merpeople', 'Aquatic beings, Triwizard Task 2', '4'),
            (50, 'The Grey Lady', 'Ghost', 'Ravenclaw ghost, daughter of Rowena', '7')
        ]
        cursor.executemany("INSERT INTO creatures (id, name, species, notable_role, book_appearances) VALUES (%s, %s, %s, %s, %s)", creatures)
        
        # Spells
        spells = [
            (1, 'Expelliarmus', 'Disarms opponent', 'Harry, Snape, Draco, Lupin', '2,3,4,5,6,7'),
            (2, 'Lumos', 'Produces light from wand tip', 'Harry, Hermione, Ron', '2,3,4,5,6,7'),
            (3, 'Nox', 'Cancels Lumos light', 'Harry, Hermione', '2,3,4,5,6,7'),
            (4, 'Alohomora', 'Unlocks doors and objects', 'Hermione', '1,2,3,4,5,6,7'),
            (5, 'Accio', 'Summons an object', 'Harry, Dumbledore, Hermione', '4,5,6,7'),
            (6, 'Expecto Patronum', 'Conjures a Patronus to repel Dementors', 'Harry, Snape, Dumbledore, Umbridge', '3,4,5,6,7'),
            (7, 'Wingardium Leviosa', 'Levitates objects', 'Hermione, Ron', '1,5'),
            (8, 'Stupefy', 'Stuns target', 'Harry, Neville, Kingsley, Tonks', '4,5,6,7'),
            (9, 'Protego', 'Shields against spells', 'Harry, Hermione, Snape', '5,6,7'),
            (10, 'Rictusempra', 'Tickling hex', 'Harry', '2'),
            (11, 'Impedimenta', 'Slows down or halts target', 'Harry, Hermione', '4,5,6'),
            (12, 'Reducto', 'Destroys solid objects', 'Harry, Ginny', '5,6,7'),
            (13, 'Incendio', 'Starts a fire', 'Hermione, Dumbledore', '1,2,3,4,5,6,7'),
            (14, 'Aguamenti', 'Produces water', 'Harry, Seamus', '6,7'),
            (15, 'Silencio', 'Silences a target', 'Hermione', '5'),
            (16, 'Levicorpus', 'Dangles person by ankle', 'Harry, Snape', '6'),
            (17, 'Liberacorpus', 'Counter to Levicorpus', 'Harry', '6'),
            (18, 'Sectumsempra', 'Causes deep slashes', 'Harry, Snape', '6'),
            (19, 'Muffliato', 'Fills ears with buzzing to block conversation', 'Harry, Snape', '6'),
            (20, 'Obliviate', 'Erases memories', 'Hermione, Lockhart', '2,7'),
            (21, 'Petrificus Totalus', 'Full body bind', 'Hermione', '1,5,7'),
            (22, 'Rennervate', 'Revives unconscious people', 'Harry, Dumbledore', '5,6,7'),
            (23, 'Confringo', 'Explodes target', 'Harry', '7'),
            (24, 'Diffindo', 'Cuts objects', 'Hermione', '4,5,6'),
            (25, 'Reparo', 'Repairs broken objects', 'Hermione, Harry', '1,2,3,4,5,6,7'),
            (26, 'Episkey', 'Heals minor injuries', 'Tonks, Luna', '6'),
            (27, 'Ennervate', 'Old version of Rennervate', 'Lupin', '4'),
            (28, 'Crucio', 'Causes intense pain (Unforgivable)', 'Harry, Bellatrix, Voldemort', '4,5,6,7'),
            (29, 'Imperio', 'Controls actions (Unforgivable)', 'Voldemort, Barty Crouch Jr.', '4,5,6,7'),
            (30, 'Avada Kedavra', 'Instantly kills (Unforgivable)', 'Voldemort, Snape, Bellatrix', '4,5,6,7'),
            (31, 'Homenum Revelio', 'Detects nearby humans', 'Dumbledore, Hermione', '6,7'),
            (32, 'Finite Incantatem', 'Ends ongoing spell effects', 'Snape, Hermione', '2,3,4,5,6,7'),
            (33, 'Prior Incantato', 'Reveals last spell cast from wand', 'Amos Diggory', '4'),
            (34, 'Portus', 'Turns objects into Portkeys', 'Dumbledore', '5'),
            (35, 'Apparition', 'Magical teleportation', 'Dumbledore, Snape, Harry, Voldemort, Death Eaters', '6,7'),
            (36, 'Obscuro', 'Conjures blindfold over target', 'Hermione', '7'),
            (37, 'Colloportus', 'Locks doors', 'Hermione', '5'),
            (38, 'Locomotor', 'Moves object', 'McGonagall, Tonks', '5,6,7'),
            (39, 'Impervius', 'Repels water, fog', 'Harry, Hermione', '3'),
            (40, 'Descendo', 'Moves objects downward', 'Crabbe', '7'),
            (41, 'Glisseo', 'Turns stairs into slide', 'Hermione', '7'),
            (42, 'Lumos Maxima', 'Produces bright light', 'Harry', '3'),
            (43, 'Protego Maxima', 'Stronger shield charm', 'Flitwick', '7'),
            (44, 'Fiendfyre', 'Cursed fire that destroys Horcruxes', 'Crabbe', '7'),
            (45, 'Cave Inimicum', 'Defensive ward spell', 'Hermione', '7'),
            (46, 'Expulso', 'Causes explosions', 'Death Eaters', '7'),
            (47, 'Incarcerous', 'Conjures ropes to bind', 'Snape, Umbridge', '5,6,7'),
            (48, 'Tarantallegra', 'Forces uncontrollable dancing', 'Draco', '2,5'),
            (49, 'Oppugno', 'Causes conjured objects to attack', 'Hermione', '6'),
            (50, 'Confundo', 'Confuses target', 'Hermione', '6,7')
        ]
        cursor.executemany("INSERT INTO spells (id, spell_name, what_it_does, users, book_appearances) VALUES (%s, %s, %s, %s, %s)", spells)
        
        conn.commit()
        print("Database and tables created successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def check_duplicate_names():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Query to find duplicate names
        query = """
        SELECT name, COUNT(*) as count
        FROM characters
        GROUP BY name
        HAVING COUNT(*) > 1
        ORDER BY count DESC, name
        """
        
        cursor.execute(query)
        duplicates = cursor.fetchall()
        
        if duplicates:
            print("\nDuplicate names found:")
            for name, count in duplicates:
                print(f"{name}: appears {count} times")
        else:
            print("\nNo duplicate names found in the dataset.")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/characters')
def get_characters():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get filter parameters
        search = request.args.get('search', '').lower()
        blood_status = request.args.get('blood_status', '')
        house = request.args.get('house', '')
        marital_status = request.args.get('marital_status', '')
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc')
        limit = int(request.args.get('limit', 50))
        
        # Build query
        query = "SELECT * FROM characters WHERE 1=1"
        params = []
        
        if search:
            query += " AND (LOWER(name) LIKE %s OR LOWER(also_known_as) LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if blood_status:
            query += " AND blood_status = %s"
            params.append(blood_status)
        
        if house:
            query += " AND house = %s"
            params.append(house)
            
        if marital_status:
            query += " AND marital_status = %s"
            params.append(marital_status)
        
        # Add sorting
        valid_sort_columns = ['name', 'date_of_birth', 'blood_status', 'house', 'marital_status']
        if sort_by in valid_sort_columns:
            query += f" ORDER BY {sort_by} {sort_order}"
        else:
            query += " ORDER BY name ASC"
        
        # Add limit
        query += " LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        characters = cursor.fetchall()
        
        # Get unique values for filters
        cursor.execute("SELECT DISTINCT blood_status FROM characters WHERE blood_status IS NOT NULL ORDER BY blood_status")
        blood_statuses = [row['blood_status'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT house FROM characters WHERE house IS NOT NULL ORDER BY house")
        houses = [row['house'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT marital_status FROM characters WHERE marital_status IS NOT NULL ORDER BY marital_status")
        marital_statuses = [row['marital_status'] for row in cursor.fetchall()]
        
        return jsonify({
            'characters': characters,
            'filters': {
                'blood_status': blood_statuses,
                'house': houses,
                'marital_status': marital_statuses
            }
        })
        
    except Error as e:
        print(f"Database error: {e}")  # Add logging
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")  # Add logging
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/creatures')
def get_creatures():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get query parameters
        search = request.args.get('search', '').lower()
        sort_by = request.args.get('sort_by', 'name')  # Default sort by name
        sort_order = request.args.get('sort_order', 'asc')  # Default ascending
        species = request.args.get('species', '')
        book_appearances = request.args.get('book_appearances', '')
        
        # Base query
        query = "SELECT * FROM creatures WHERE 1=1"
        params = []
        
        # Add search conditions
        if search:
            query += """ AND (
                LOWER(name) LIKE %s 
                OR LOWER(species) LIKE %s
                OR LOWER(notable_role) LIKE %s
                OR LOWER(book_appearances) LIKE %s
            )"""
            search_param = f"%{search}%"
            params.extend([search_param] * 4)
        
        # Add filter conditions
        if species:
            query += " AND species = %s"
            params.append(species)
        
        if book_appearances:
            query += " AND book_appearances LIKE %s"
            params.append(f"%{book_appearances}%")
        
        # Add sorting
        valid_sort_columns = ['name', 'species', 'notable_role', 'book_appearances']
        if sort_by in valid_sort_columns:
            query += f" ORDER BY {sort_by} {'DESC' if sort_order.lower() == 'desc' else 'ASC'}"
        
        cursor.execute(query, params)
        creatures = cursor.fetchall()
        
        return jsonify({'creatures': creatures})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/spells')
def get_spells():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Get query parameters
        search = request.args.get('search', '').lower()
        sort_by = request.args.get('sort_by', 'spell_name')  # Default sort by spell name
        sort_order = request.args.get('sort_order', 'asc')  # Default ascending
        book_appearances = request.args.get('book_appearances', '')
        
        # Base query
        query = "SELECT * FROM spells WHERE 1=1"
        params = []
        
        # Add search conditions
        if search:
            query += """ AND (
                LOWER(spell_name) LIKE %s 
                OR LOWER(what_it_does) LIKE %s
                OR LOWER(users) LIKE %s
                OR LOWER(book_appearances) LIKE %s
            )"""
            search_param = f"%{search}%"
            params.extend([search_param] * 4)
        
        # Add filter conditions
        if book_appearances:
            query += " AND book_appearances LIKE %s"
            params.append(f"%{book_appearances}%")
        
        # Add sorting
        valid_sort_columns = ['spell_name', 'what_it_does', 'users', 'book_appearances']
        if sort_by in valid_sort_columns:
            query += f" ORDER BY {sort_by} {'DESC' if sort_order.lower() == 'desc' else 'ASC'}"
        
        cursor.execute(query, params)
        spells = cursor.fetchall()
        
        return jsonify({'spells': spells})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    create_database()
    check_duplicate_names()
    app.run(debug=True) 