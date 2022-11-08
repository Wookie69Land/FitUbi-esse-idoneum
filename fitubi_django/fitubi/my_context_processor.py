from datetime import datetime

def my_cp(request):
  ctx = {
    "now": datetime.now(),
    "version": "1.0",
  }
  return ctx