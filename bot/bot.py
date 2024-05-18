import logging
import re
import paramiko
import psycopg2
from psycopg2 import Error
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

host = '10.5.0.5'
port = '22'
username = 'root'
password = 'root123'
connection = psycopg2.connect(user = "postgres",
                                  password = "postgres",
                                  host = "10.5.0.5",
                                  port = "5432",
                                  database = "db_mydatabase")

TOKEN = "7082183229:AAGQCWjMClqNimMhm4ELvm200csiXNo54DM"

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска адреса электронной почты: ')
    return 'find_email'

def find_email(update: Update, context):
    global emailList
    user_input = update.message.text

    emailRegex = re.compile(r'\S+@\S+\.\S+')

    emailList = emailRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('Адреса электронной почты не найдены')
        return

    emailAddresses = ''
    for i in range(len(emailList)):
        emailAddresses += f'{i+1}. {emailList[i]}\n'
    update.message.reply_text(emailAddresses)
    update.message.reply_text('Записать данные в базу данных? (Да или нет)')
    return 'insert_email_into_db'

def insert_email_into_db(update: Update, context):
        user_choice = update.message.text
        logging.info(user_choice)
        if user_choice == 'Да':
            logging.info('Начало записи в БД')
            cursor = connection.cursor()
            for i in range(len(emailList)):
                cursor.execute("SELECT emailid FROM emails ORDER BY emailid DESC LIMIT 1;")
                data = cursor.fetchall()
                data = str(data).replace('[','').replace(']', '').replace('(', '').replace(')', '').replace(',', '')
                int_data = int(data)
                cursor.execute("INSERT INTO emails (emailid, emailaddress) VALUES ('"+f'{int_data+1}'+"','"+f'{emailList[i]}'+"')")
                connection.commit()
            update.message.reply_text('Запись добавлена в базу данных. Для проверки введите команду "/get_emails"')
            return ConversationHandler.END
        else:
            return ConversationHandler.END

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки его сложности: ')

    return 'verify_password'

def verify_password(update: Update, context):
    user_input = update.message.text

    passRegex = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

    passList = passRegex.findall(user_input)

    if not passList:
        update.message.reply_text('Пароль простой')
        return
    else:
        update.message.reply_text('Пароль сложный')

    return ConversationHandler.END


def get_release (update: Update, context):
    logging.info('Переход к функции get_release')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_uname(update: Update, context):
    logging.info('Переход к функции get_uname')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_uptime(update: Update, context):
    logging.info('Переход к функции get_uptime')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_df(update: Update, context):
    logging.info('Переход к функции get_df')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_free(update: Update, context):
    logging.info('Переход к функции get_free')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_mpstat(update: Update, context):
    logging.info('Переход к функции get_mpstat')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_w(update: Update, context):
    logging.info('Переход к функции get_w')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_auths(update: Update, context):
    logging.info('Переход к функции get_auths')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_critical(update: Update, context):
    logging.info('Переход к функции get_critical')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -n 5 -p 2')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_ps(update: Update, context):
    logging.info('Переход к функции get_ps')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_ss(update: Update, context):
    logging.info('Переход к функции get_ss')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss|tail')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getAptListCommand(update: Update, context):
    update.message.reply_text('Если вам необходимо вывести данные об определенном пакете, то напишите его название, если необходимо вывести данные о всех пакетах, то напишите all: ')
    return 'get_apt_list'

def get_apt_list(update: Update, context):
    logging.info('Переход к функции get_apt_list')
    user_input = update.message.text
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    if user_input == 'all':
        stdin, stdout, stderr = client.exec_command('apt list | tail -n 10')
    else:
        stdin, stdout, stderr = client.exec_command('apt list' + ' ' + f'{user_input}')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_services(update: Update, context):
    logging.info('Переход к функции get_services')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service | tail -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_repl_logs(update: Update, context):
    logging.info('Переход к функции get_repl_logs')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /var/log/postgresql/postgresql-15-main.log | tail -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def get_emails(update: Update, context):
    logging.info('Переход к функции get_emails')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM emails;")
    data = cursor.fetchall()
    data = str(data).replace('),', '\n').replace('[', ''). replace(',', ':').replace(']', '').replace('(', '').replace(')', '')
    update.message.reply_text(data)
    return ConversationHandler.END

def get_phone_numbers(update: Update, context):
    logging.info('Переход к функции get_phone_numbers')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM phones;")
    data = cursor.fetchall()
    data = str(data).replace('),', '\n').replace('[', ''). replace(',', ':').replace(']', '').replace('(', '').replace(')', '')
    update.message.reply_text(data)
    return ConversationHandler.END

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'


def find_phone_number (update: Update, context):
    global phoneNumberList
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'[8|\+7]\d{10,11}|[\+7|8]\(\d{3}\)\d{7,8}|[\+7|8] \d{3} \d{3} \d{2} \d{2}|[+7|8] \(\d{3}\) \d{3} \d{2} \d{2}|[\+7|8]-\d{3}-\d{3}-\d{2}-\d{2}|[\+7|8] \(\d{3}\) \d{3}-\d{2}-\d{2}') # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
        
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    update.message.reply_text('Записать данные в базу данных? (Да или нет)')
    return 'insert_phone_into_db'

def insert_phone_into_db(update: Update, context):
        user_choice = update.message.text
        logging.info(user_choice)
        if user_choice == 'Да':
            logging.info('Начало записи в БД')
            cursor = connection.cursor()
            for i in range(len(phoneNumberList)):
                cursor.execute("SELECT phoneid FROM phones ORDER BY phoneid DESC LIMIT 1;")
                data = cursor.fetchall()
                data = str(data).replace('[','').replace(']', '').replace('(', '').replace(')', '').replace(',', '')
                int_data = int(data)
                cursor.execute("INSERT INTO phones (phoneid, phonenumber) VALUES ('"+f'{int_data+1}'+"','"+f'{phoneNumberList[i]}'+"')")
                connection.commit()
            update.message.reply_text('Запись добавлена в базу данных. Для проверки введите команду "/get_phone_numbers"')
            return ConversationHandler.END
        else:
            return ConversationHandler.END


def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'insert_phone_into_db': [MessageHandler(Filters.text & ~Filters.command, insert_phone_into_db)]
        },
        fallbacks=[]
    )

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'insert_email_into_db': [MessageHandler(Filters.text & ~Filters.command, insert_email_into_db)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )

    convHandlerGetRelease = ConversationHandler(
        entry_points=[CommandHandler('get_release', get_release)],
        states={
            'get_release': [MessageHandler(Filters.text & Filters.command, get_release)],
        },
        fallbacks=[]
    )

    convHandlerGetUname = ConversationHandler(
        entry_points=[CommandHandler('get_uname', get_uname)],
        states={
            'get_uname': [MessageHandler(Filters.text & Filters.command, get_uname)],
        },
        fallbacks=[]
    )

    convHandlerGetUptime = ConversationHandler(
        entry_points=[CommandHandler('get_uptime', get_uptime)],
        states={
            'get_uptime': [MessageHandler(Filters.text & Filters.command, get_uptime)],
        },
        fallbacks=[]
    )

    convHandlerGetDf = ConversationHandler(
        entry_points=[CommandHandler('get_df', get_df)],
        states={
            'get_df': [MessageHandler(Filters.text & Filters.command, get_df)],
        },
        fallbacks=[]
    )

    convHandlerGetFree = ConversationHandler(
        entry_points=[CommandHandler('get_free', get_free)],
        states={
            'get_free': [MessageHandler(Filters.text & Filters.command, get_free)],
        },
        fallbacks=[]
    )

    convHandlerGetMpstat = ConversationHandler(
        entry_points=[CommandHandler('get_mpstat', get_mpstat)],
        states={
            'get_mpstat': [MessageHandler(Filters.text & Filters.command, get_mpstat)],
        },
        fallbacks=[]
    )

    convHandlerGetW = ConversationHandler(
        entry_points=[CommandHandler('get_w', get_w)],
        states={
            'get_w': [MessageHandler(Filters.text & Filters.command, get_w)],
        },
        fallbacks=[]
    )

    convHandlerGetAuths = ConversationHandler(
        entry_points=[CommandHandler('get_auths', get_auths)],
        states={
            'get_auths': [MessageHandler(Filters.text & Filters.command, get_auths)],
        },
        fallbacks=[]
    )

    convHandlerGetCritical = ConversationHandler(
        entry_points=[CommandHandler('get_critical', get_critical)],
        states={
            'get_critical': [MessageHandler(Filters.text & Filters.command, get_critical)],
        },
        fallbacks=[]
    )

    convHandlerGetPs = ConversationHandler(
        entry_points=[CommandHandler('get_ps', get_ps)],
        states={
            'get_ps': [MessageHandler(Filters.text & Filters.command, get_ps)],
        },
        fallbacks=[]
    )

    convHandlerGetSs = ConversationHandler(
        entry_points=[CommandHandler('get_ss', get_ss)],
        states={
            'get_ss': [MessageHandler(Filters.text & Filters.command, get_ss)],
        },
        fallbacks=[]
    )

    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

    convHandlerGetServices = ConversationHandler(
        entry_points=[CommandHandler('get_services', get_services)],
        states={
            'get_services': [MessageHandler(Filters.text & Filters.command, get_services)],
        },
        fallbacks=[]
    )

    convHandlerGetReplLogs = ConversationHandler(
        entry_points=[CommandHandler('get_repl_logs', get_repl_logs)],
        states={
            'get_repl_logs': [MessageHandler(Filters.text & Filters.command, get_repl_logs)],
        },
        fallbacks=[]
    )	

    convHandlerGetEmails = ConversationHandler(
        entry_points=[CommandHandler('get_emails', get_emails)],
        states={
            'get_emails': [MessageHandler(Filters.text & Filters.command, get_emails)],
        },
        fallbacks=[]
    )	

    convHandlerGetPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('get_phone_numbers', get_phone_numbers)],
        states={
            'get_phone_numbers': [MessageHandler(Filters.text & Filters.command, get_phone_numbers)],
        },
        fallbacks=[]
    )	

	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerVerifyPass)
    dp.add_handler(convHandlerGetRelease)
    dp.add_handler(convHandlerGetUname)
    dp.add_handler(convHandlerGetUptime)
    dp.add_handler(convHandlerGetDf)
    dp.add_handler(convHandlerGetFree)
    dp.add_handler(convHandlerGetMpstat)
    dp.add_handler(convHandlerGetW)
    dp.add_handler(convHandlerGetAuths)
    dp.add_handler(convHandlerGetCritical)
    dp.add_handler(convHandlerGetPs)
    dp.add_handler(convHandlerGetSs)
    dp.add_handler(convHandlerGetAptList)
    dp.add_handler(convHandlerGetServices)
    dp.add_handler(convHandlerGetReplLogs)
    dp.add_handler(convHandlerGetEmails)
    dp.add_handler(convHandlerGetPhoneNumbers)
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()
	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
