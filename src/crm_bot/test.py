#!/usr/bin/env python3
from crm_bot.models import Status
from crm_bot.storage import RequestStorage

storage = RequestStorage()

storage.add(12345678, "@test1", "abc")
storage.add(12345679, "@test2", "bcd")
storage.add(12345680, "@test3", "cde")

storage.update_status(2, Status.IN_PROGRESS)

print(storage.get_all())