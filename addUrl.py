
import random
import MySQLdb
import sys
import time
import os






        #self.conn = MySQLdb.connect(host = config['host'],
#                                    user=config['user'],passwd= config['passwd'] ,port = config['port'])
        #self.conn.select_db(config['database'])
            #sql = "update domain set scan_type=1, update_time = now() where id=%d" % item_id
            #c = self.conn.cursor()
            #res = c.execute(sql)
            #self.conn.commit()


db_config = {}
db_config['host'] = '192.168.100.97'
db_config['port'] = 3306
db_config['user'] = 'root'
db_config['passwd'] = 'root'
db_config['database'] = 'domain'
config = db_config

if __name__ == "__main__":
        conn = MySQLdb.connect(host = config['host'],
                                    user=config['user'],passwd= config['passwd'] ,port = config['port'])
        conn.select_db(config['database'])
	f = open('uniq-wp-domain.txt' , 'r')
	for line in f.readlines():
		line.strip()
            	sql = "insert into url set url='%s'" % line.strip()
		print sql
            	c = conn.cursor()
            	res = c.execute(sql)
	conn.commit()
