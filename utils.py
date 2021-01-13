import finance_api
from tabulate import tabulate
from datetime import datetime, timedelta, date
from selenium import webdriver
from PIL import Image
from io import BytesIO
from os.path import expanduser
from time import sleep

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(format_company_overview(finance_api.get_company_overview(ticker_symbol)))

def handle_message(message):
    message_args = message.content.split()
    command = message_args[0]
    if (len(message_args) > 1) :
        ticker_symbol = message_args[1]
    else:
        ticker_symbol = ""
    
    # testing
    # command = '$overview'
    # ticker_symbol = 'tnxp'
    if command == '$daily':
        return format_daily(finance_api.get_daily(ticker_symbol))
    elif command == '$quote':
        return format_quote(finance_api.get_quote_endpoint(ticker_symbol))
    elif command == '$graph':
        graph(ticker_symbol)
        return 'post_graph'
    elif command == '$overview':
        return format_company_overview(finance_api.get_company_overview(ticker_symbol))
    elif command == '$help':
        return format_help()
    else: 
        return None

def format_daily(obj):
    today = date.today().strftime('%Y-%m-%d')
    try:
        data_dict = obj[today]
        date_used = today
    except:
        yesterday = today - timedelta(days=1)
        yesterday_formatted = yesterday.strftime('%Y-%m-%d')
        date_used = yesterday_formatted
        data_dict = obj[yesterday_formatted]
    
    rtn_str = "Date: " + date_used + "\n"
    rtn_str += "------------------------ \n"
    for key, value in data_dict.items():
        rtn_str += "{:<8} {:<15}".format(key[3:], value) + "\n"
    
    rtn_str += "------------------------"

    return rtn_str


def format_quote(obj):
    today = date.today().strftime('%Y-%m-%d')
    
    rtn_str = "Date: " + today + "\n"
    rtn_str += "------------------------ \n"
    for key, value in obj.items():
        rtn_str += "{:<20} {:<15}".format(key[4:], value) + "\n"
    
    rtn_str += "------------------------"

    return rtn_str


def format_company_overview(obj):
    rtn_str = "{:<20} {:<15}".format('Symbol', obj['Symbol']) + "\n"
    rtn_str += "{:<20} {:<15}".format('Name', obj['Name']) + "\n"
    rtn_str += "{:<20} {:<15}".format('Sector', obj['Sector']) + "\n"
    rtn_str += "{:<20} {:<15}".format('Description', obj['Description']) + "\n\n"
    
    rtn_str += "{:<20} {:<15}".format('52 Week High', obj['52WeekHigh']) + "\n"
    rtn_str += "{:<20} {:<15}".format('52 Week Low', obj['52WeekLow']) + "\n"
    rtn_str += "{:<20} {:<15}".format('50 Day Moving Average', obj['50DayMovingAverage']) + "\n"
    rtn_str += "{:<20} {:<15}".format('200 Day Moving Average', obj['200DayMovingAverage']) + "\n\n"

    rtn_str += "{:<20} {:<15}".format('Analyst Target Price', obj['AnalystTargetPrice']) + "\n"
    
    return rtn_str


def graph(ticker_symbol):
    # Define url and driver
    url = 'https://www.stockscores.com/charts/charts/?ticker=' + ticker_symbol
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.set_window_size(1366, 1000)

    # Go to url, scroll down to right point on page and find correct element
    driver.get(url)
    sleep(1) #  Wait for page to load
    list_el = driver.find_element_by_class_name('timechoice').find_element_by_tag_name('li')
    list_el.click()
    sleep(0.5) # Wait for graph to update
    element = driver.find_element_by_class_name('col_full')
    driver.save_screenshot("shot.png")

    location = element.location
    size = element.size

    x = location['x']
    y = location['y']
    w = size['width']
    h = 900
    width = x + w - 100
    height = y + h

    driver.close()

    im = Image.open('shot.png')
    im = im.crop((100, 250, int(width), int(height)))
    im.save('shot.png')


def format_help():
    rtn_str = "Commands: (arguments must be separated by spaces)\n\n"
    rtn_str += "$daily (1 arg)\n"
    rtn_str += "$quote (1 arg)\n"
    rtn_str += "$graph (1 arg)\n"

    return rtn_str


def code_embed(message):
    # ```
    # >
    return '```' + message + '```'
