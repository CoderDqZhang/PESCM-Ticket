import uuid
import time
import datetime
from ticket.until import pinyin

def create_serial_number():
	return uuid.uuid1()


def get_date_time():
    return (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

def get_time():
    return (time.strftime('%Y%m%d%H%M%S',time.localtime()))


def get_ticket_id(ticket_model):
    first_order = pinyin.get_pinyin_first_alpha(ticket_model.ticket_model_name)
    ticket_id = str(first_order + get_date_time())
    return ticket_id

if __name__ == "__main__":
	id = create_serial_number()