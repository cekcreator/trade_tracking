from track_trades import find_recent_trade_write_to_csv
from send_email import send_email

if __name__ == '__main__':
    find_recent_trade_write_to_csv()
    send_email()
    print('Done')
