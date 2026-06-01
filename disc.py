from disc_data import run_disc, CF_DATA, MK_DATA
from datetime import datetime
from forces_stat import forces_stat
from monkey_stat import monkey_stat

current_day = datetime.now().strftime("%A")
monkeys_days = "Tuesday, Thursday, Saturday"
if current_day in monkeys_days:
    run_disc(data=MK_DATA, func=monkey_stat)
else:
    run_disc(data=CF_DATA, func=forces_stat)
