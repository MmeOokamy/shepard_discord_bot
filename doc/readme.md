## Environment :
* Linux
    * python3 -m venv bot-l-env
    * source bot-l-env/bin/activate

* Win
    * python -m venv bot-w-env
    * source bot-w-env\script\activate.bat

* Install Discord
    * pip install -U discord.py
## Token :
* dotenv
    * pip install -U python-dotenv
    * from dotenv import load_dotenv
        * load_dotenv() <- create an .env file => with => TOKEN=INSERThereYOurTOK3N
        * use -> bot.run(os.getenv("TOKEN")) 

## Requirement :
* freeze
  * → pip freeze > requirements.txt


* install
  *  → pip install -r requirements.txt