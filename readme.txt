Witaj w README superpoczty 2000

1. czym jest superpoczta 2000?
Superpoczta 2000 to lokalnie działający klient-server poczty który jest niesamowicie przydatny! :D

2. Instalacja
Program Superpoczta 2000 jak każdy dobry szanujący się software zawiera swój bezawaryjny super wydajny skrypt instalacyjny.
Wystarczy uruchomić plik setup.py i trolololo ( https://www.youtube.com/watch?v=TJL4Y3aGPuA ), a jeżeli o zgrozo z jakiegoś powodu skrypt nie zadziała (co nie ma prawa się wydarzyć!)
to zalecamy odpalić skrypt w konsoli w tym celu
odpalamy terminal > cd /ścierzka/do/programu/ > python3 setup.py

3. Instalacja manualna.

Jeżeli lubisz niepotrzebnie komplikować sobie życie lub przez chwilę chcesz poczuć się jak prawdziwy geek
możesz samodzielnie przeprowadzić proces instalacji w 6 potwornie trudnych krokach!

1. przejdź do katalogu z programem:
cd /ścierzka/do/programu/
2. stwórz wirtualne środowisko
virtualenv -p python3 env
3. zainstaluj zależności
python3 install -r requirements.py
4. stwórz bazę danych
>> sudo su - postgres
>> psql
>> CREATE DATABASE name_of_db;
5. stwórz tabelki w bazie
>> sudo su - postgres
>> psql
>> \c name_of_db
>> CREATE TABLE users (
id serial NOT NULL,
username VARCHAR(255) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
hashed_password VARCHAR(255) NOT NULL,
PRIMARY KEY (id)
);
>> CREATE TABLE messages (
id serial NOT NULL,
title VARCHAR(255) NOT NULL,
message TEXT NOT NULL,
sender VARCHAR(255) NOT NULL,
receiver VARCHAR(255) NOT NULL,
creation_date timestamp,
PRIMARY KEY (id),
FOREIGN KEY(sender) REFERENCES users(email),
FOREIGN KEY(receiver) REFERENCES users(email)
);
6. dodaj ustawienia bazy danych do pliku config
W katalogu głównym projektu przejdź do folderu database
Stwórz, jeżeli jeszcze nie istnieje lub modyfikuj plik config.ini
'''
[db]
username = postgres
password = coderslab
name = asdfg123
'''
gdzie jako username podaj swój login dostępu do postgres
password - hasło dostępu
name - nazwa bazy danych, na której będzie działała twoja Superpoczta 2000

Jeżeli samodzielnie przebrnąłeś przez powyższe kroki, to poczułeś z pewnością namiastkę tego, jak czuł się wielki twórca Superpoczty 2000 (ale i tak nie dorównujesz mu do pięt!)
zasłużyłeś na zaszczytne miano script kiddie 2000 :D