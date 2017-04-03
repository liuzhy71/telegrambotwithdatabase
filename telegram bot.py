from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram import ChatAction
import sqlite3

default_list=["Take a break","Go back to home","Go to a lecture"]

def showTasks(bot,update):


    to_do_list = []

    """filename = 'task_list.txt'
    try:
        txt = open(filename)
        to_do_list = txt.read().splitlines()
        txt.close()
    except IOError:
        t = 1
        # update.message.reply_text("File not found! Use empty list instead.")"""


    conn = sqlite3.connect('todo_database.db')
    cur = conn.cursor()
    to_do_list = cur.fetchall()
    conn.close()

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("Show all existing tasks.")
    if len(to_do_list) < 1:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Nothing to do, here!")
    else:
        temp_to_do_list = to_do_list[:]
        temp_to_do_list.sort()
        i = 1
        for things in temp_to_do_list:
            update.message.reply_text('(' + str(i) + ')' + things)
            i += 1

def newTask(bot,update,args):
    to_do_list=[]

    """filename = 'task_list.txt'
    try:
        txt = open(filename)
        to_do_list = txt.read().splitlines()
        txt.close()
    except IOError:
        t = 1
        # update.message.reply_text("File not found! Use empty list instead.")"""

    conn = sqlite3.connect('todo_database.db')
    cur = conn.cursor()
    sql = "select count(*) from todo_list"
    cur = conn.execute(sql)
    count = cur[0]
    conn.execute("INSERT INTO todo_list (id, todo) VALUES (?,?)")
    cur.close()

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    #update.message.reply_text("Insert a new task.\nPlease type the task:")
    newtask = ' '.join(args)
    if (newtask==''):
        update.message.reply_text("No task is entered.")
    else:
        to_do_list.append(newtask)
        update.message.reply_text("The new task was successfully added to the list!")
        i = 1
        for things in to_do_list:
            update.message.reply_text('(' + str(i) + ')' + things)
            i += 1

    try:
        txt = open(filename, 'w')
        for single_task in to_do_list:
            txt.write(single_task + '\n')
        txt.close()
    except IOError:
        t = 2
        # print('Problems in saving to do list.')

def removeTask(bot, update, args):
    to_do_list = []
    filename = 'task_list.txt'
    try:
        txt = open(filename)
        to_do_list = txt.read().splitlines()
        txt.close()
    except IOError:
        t = 1
        # update.message.reply_text("File not found! Use empty list instead.")
    deltask = ' '.join(args)
    if (deltask==''):
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("No task is delated!")
    else:
        to_do_list.remove(deltask)
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("The task was successfully delated!")
    i = 1
    for things in to_do_list:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text('(' + str(i) + ')' + things)
        i += 1
    try:
        txt = open(filename, 'w')
        for single_task in to_do_list:
            txt.write(single_task + '\n')
        txt.close()
    except IOError:
        t = 2
        # print('Problems in saving to do list.')

def removeAllTasks(bot,update,args):
    to_do_list=[]
    filename = 'task_list.txt'
    try:
        txt = open(filename)
        to_do_list = txt.read().splitlines()
        txt.close()
    except IOError:
        t = 1
        # update.message.reply_text("File not found! Use empty list instead.")
    remove_list = []
    substring = ''.join(args)
    if (substring == ''):
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("No task is delated!")
    else:
        for single_task in to_do_list:
            if (substring in single_task):
                remove_list.append(single_task)
        if (len(remove_list) > 0):
            for task_to_remove in remove_list:
                if (task_to_remove in to_do_list):
                    to_do_list.remove(task_to_remove)
                    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
                    update.message.reply_text("The element " + task_to_remove + " was successfully removed")
        else:
            bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
            update.message.reply_text("I did not find any tasks to delete!")

    try:
        txt = open(filename, 'w')
        for single_task in to_do_list:
            txt.write(single_task + '\n')
        txt.close()
    except IOError:
        t = 2
        # print('Problems in saving to do list.')

def echo(bot,update):
    #bot.sendChatAction(update.message.chat_id, ChatAction.UPLOAD_AUDIO)
    repeat_text = update.message.text

    #update.message.reply_text(repeat_text);
    #tts = gTTS(text=repeat_text,lang='en')
    #tts.save("echo.mp3")
    #bot.sendVoice(chat_id=update.message.chat_id,voice=open("echo.mp3",'rb'))

def main():
    updater = Updater('340779334:AAHz3xwTWZy-1Nw9jDlb5labgj9bMy3UUow')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('show',showTasks))
    dp.add_handler(CommandHandler('new',newTask,pass_args=True))
    dp.add_handler(CommandHandler('remove',removeTask,pass_args=True))
    dp.add_handler(CommandHandler('removeAllof',removeAllTasks,pass_args=True))
    dp.add_handler(MessageHandler(Filters.text,echo))
    updater.start_polling()    #continusely ask do you have somthing
    updater.idle()              #run forever or exterminate

if __name__ == '__main__':
    main()
