import re
with open('crawler.log', "r", encoding='utf-8') as log:
    log = log.readline()
    match = re.match(r"([\d-]+ [\d:,]+) (.+)", log)

    if match:
        time = match.group(1)
        message = match.group(2)
        time_log = {'time': time, 'message': message}
    print(time_log)