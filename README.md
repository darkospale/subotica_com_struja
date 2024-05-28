# subotica_com_struja
This is a personal plugin that fetches data from subotica.com website that informs about electricity outage in town for certain parts of the city.

## How to use

Download the repo and place it somewhere on your local machine <br>
(If you have a server where to place it, even better).

If you want, create a virtual environment with command
```python -m venv <name>```

Install all the required packages using
```pip install -r requirements.txt```

Of course, in order to be able to send the messages to your telegram bot
you will need to create a bot. <br>

You can just follow this link: https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/

After that, create a `.env` file and the following variables and fill in the info:
* TELEGRAM_CHAT_ID
* TELEGRAM_API_KEY
* GOOGLE_SPACE_ID (WIP)

<span style="color: red;">Make sure to have `pip` installed!</span>

Now, you are ready to run your script. Do it by using this:

To make it executable:
```chmod a+x /path/to/reminder.py```

Use `nohup` to make the process run in the background: <br>
```nohup /path/to/reminder.py &```

#### Now you are done. So basically you can exit your terminal and the process will be running.

If you want to, however, kill the process, you can find it like so:

`ps ax | grep reminder.py`

And kill the process by using:

`kill -9 <process_id>`


### To-Do list

- [ ] Add multiple locations using multi-input fields;
- [ ] Implement a graphical interface (GUI) using tkinter;
- [ ] Select option if to include weekends or not;
- [ ] Make an executable file;
- [ ] Make the script accept arguments from the telegram bot chat;