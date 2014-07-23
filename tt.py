import pexpect

child = pexpect.spawn("/bin/sh" , ['-c' , '/home/toor/workspace/batch-exp/start_whatweb.sh "http://www.mgpyh.com"'] ,timeout = 1200)
child.logfile = open("/tmp/mylog", "w")
child.expect(pexpect.EOF)
