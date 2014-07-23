
import random
import pexpect
import threading
from Queue import Queue
import MySQLdb
import sys
import time
import os

WPSCAN_DIR = '/home/toor/workspace/wpscan'
OUTPUT_LOG_PATH =  os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'output_log_tmp'

#shell_cmd = "echo 'Process started'; ping www.baidu.com; echo 'Process finished'"
shell_cmd = "ruby /root/wpscan/wpscan.rb --follow-redirection --url 'www.92app.com'"
shell_cmd = "ruby /root/wpscan/wpscan.rb -t 10 --follow-redirection --url 'www.anotherself.com' -e vp,vt"
#shell_cmd = "ruby /root/wpscan/wpscan.rb  --follow-redirection --url 'www.dofisodifidodofo.com'"
#shell_cmd = "ruby /root/wpscan/wpscan.rb --url 'www.92app.com'"
#shell_cmd = "ruby /root/wpscan/wpscan.rb --help"

def random_str(length):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    tmp = ''
    for i in range(0,length):
        tmp += random.choice(alpha)
    return tmp



def wpscan(url):
    output = ''
    #shell_cmd = "ruby %s/wpscan.rb -t 10 --follow-redirection --url '%s' -e vp,vt" % ( WPSCAN_DIR, url)
    #shell_cmd = "cd %s && ./wpscan.rb -t 20 --batch  --follow-redirection -c /home/toor/workspace/wpscan/conf.json  --url '%s'" % ( WPSCAN_DIR, url)
    logfile = OUTPUT_LOG_PATH + os.path.sep + random_str(20)
    if os.path.isfile(logfile):
        logfile = OUTPUT_LOG_PATH + os.path.sep + random_str(20)

    try:
        fout = file(logfile , 'w')
	child = pexpect.spawn("/bin/sh" , ['-c' , '/home/toor/workspace/batch_wpscan/start_wpscan.sh "%s"' % url ] ,timeout = 1200)
        child.logfile = fout
        child.expect(pexpect.EOF)
    except pexpect.TIMEOUT:
        output = "timeout"

    finally:
        f = file( logfile)
        content = f.read()
        f.close()
        os.remove(logfile)
        return content



class Worker(threading.Thread):
    def __init__(self, id, config):
        threading.Thread.__init__(self)
        self.id = id
        self.conn = MySQLdb.connect(host = config['host'],
                                    user=config['user'],passwd= config['passwd'] ,port = config['port'])
        self.conn.select_db(config['database'])

    def run(self):
	global finished
        print "id:%d" % (self.id)
        print "q.qsize:%d" % (q.qsize())
	
        while (finished != True or q.qsize() != 0):
            task_info = q.get()

            item_id = task_info[0]
            url = task_info[1]
            sql = "update url set scan_type=1, update_time = now() where id=%d" % item_id
            c = self.conn.cursor()
            #print sql
            res = c.execute(sql)
            self.conn.commit()
            print "begin to scan id:%d,url: %s" % (item_id , url)
            output = wpscan(url)
            #print output
           #time.sleep(2)
            print "end"
            sql = "update url set scan_type = 2,scan_output='%s',update_time = now() where id=%d" % \
                    (self.conn.escape_string(output) , item_id)

            #print sql

            c.execute(sql)
            self.conn.commit()



class Producer(threading.Thread):
    def __init__(self,  config ):
        threading.Thread.__init__(self)
        self.conn = MySQLdb.connect(host = config['host'],
                                    user=config['user'],passwd= config['passwd'] ,port = config['port'])
        self.conn.select_db(config['database'])

    def run(self):
        global finished
        sql = "select * from url where scan_type = 0 or scan_type = 1"
        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)

        cur.execute(sql)
        results = cur.fetchall()
        for item in results:
            self.enqueue((item['id'], item['url']))


        fin_lock.acquire()
        finished = True
        print "finished is True"
        fin_lock.release()

    def enqueue(self,task_info ):
        #print "queue size : %d" % q.qsize()
        while (q.qsize() >= QUEUE_CHUNK_NUM):
            print "enter sleep"
            time.sleep(10)

        #print "queue size : %d" % q.qsize()
        q.put(task_info)

fin_lock = threading.Lock()

QUEUE_CHUNK_NUM = 5000
q = Queue(maxsize= 3 * QUEUE_CHUNK_NUM)
THREAD_NUM = 30
finished = False


db_config = {}
#db_config['host'] = '192.168.11.5'
db_config['host'] = '192.168.100.97'
db_config['port'] = 3306
db_config['user'] = 'root'
db_config['passwd'] = 'root'
db_config['database'] = 'domain'

if __name__ == "__main__":
    #output = wpscan( 'www.anotherself.com')
    #print output


    #producer = Producer(host = '192.168.100.97' , user = 'root', passwd = 'root')
    producer = Producer(db_config)
    producer.start()


    workers = []
    for i in range(0 , THREAD_NUM):
        worker = Worker( i , db_config)
        worker.start()
        workers.append(worker)


    producer.join()

    for worker in workers:
        worker.join()

