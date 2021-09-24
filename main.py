from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='USD')
        bot.select_place_to_go(input('Where do you want to go?'))
        bot.select_dates(check_in_date=input('What is check in date?'), check_out_date=input('What is check out date?'))
        bot.select_adults(int(input('How many people?')))
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh() #workaround to let bot grab data properly in order
        bot.report_results()


except Exception as e:
    if 'in PATH' in str(e):
        print("There is a problem running program from CLI")
    else:
        raise
