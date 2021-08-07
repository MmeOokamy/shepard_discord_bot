## Environement
* Linux
    * python3 -m venv bot-env
    * source bot-env/bin/activate

* Win
    * python -m venv bot-env
    * source bot-env\script\activate.bat

* Install Discord
    * pip install -U discord.py -m


## Tokken
* dotenv
    * pip install -U python-dotenv
    * from dotenv import load_dotenv
        * load_dotenv() <- create an .env file => with => TOKEN=INSERThereYOurTOK3N
        * use -> bot.run(os.getenv("TOKEN")) 