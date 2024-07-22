# Pregikt-Upload

Dies ist ein Tool zum Hochladen von Predigten. 

### Usage

#### Executable
Es kann die Executable in diesem ordner ausgeführt werden, Sie muss jedoch im ./ verzeichniss sein.

#### python 
```
python main.py
```


### Installation

Um die Skripte auszuführen muss diese pip packages Installiert sein.
Die Executable kann auch ohne diese Ausgeführt werden.

```
pip install -r requirements.txt
```


### configurieren

Es muss eine config.json file vorhanden sein, mit diesem Inhalt.
```
{
    "config_json_not_empty": "True",
    
    "YOUTUBE_API_KEY": "YOUR API KEY",
    "channel_id": "Youtube Id von dem Kanal auf dem die Livestreams Hochgeladen werden",

    "server": "ftplib server name",
    "name": "ftplib usr name ",
    "password": "ftp passwort",

    "website_exists": "True",
    "website_url": "URL der Übersichtsseite"

    "threshold_db": -12,
    "ratio":2,
    "attack":200,
    "release":1000
}
```
Diese kann per Drag and drop auf dem LoginScreen hinzugefügt werden.



