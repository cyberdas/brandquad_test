from apachelogs import LogParser

# combined parser
parser = LogParser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"')
log_1 = ''
log_2 = ''
log_3 = ''