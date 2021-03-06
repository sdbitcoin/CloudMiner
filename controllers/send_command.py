import asyncore
#from TaskMaster 
import TaskMaster
from time import sleep

@auth.requires_login()
def index(): #return dict(message="hello from send_command.py")
    #if request.args:
    #    print ' '.join(request.args)
    if not request.args or len(request.args)<2:
        session.error_message = 'SEND_COMMAND should be called with appropiate parameters, check manual for further info'
        redirect(URL(c='error'))
        #raise HTTP(303, test='testing!!!', Location=URL(c='error'))
    command = request.args[0]
    if (command=='start' or command=='stop' or command=='test') and len(request.args)<3:
        session.error_message = 'SEND_COMMAND: start/stop/test commands need two parameters, check manual for further info'
        redirect(URL(c='error'))
    machine_id=request.args[1]
    rows = db(db.machine.id==machine_id).select(db.machine.ip,
                                                    db.machine.port)
    row = rows[0]
    #print row
    ip = row.ip
    port = int(row.port)
    if command=='start':
        miner_id=request.args[2]
        task = 'start '+miner_id
    elif command=='stop':
        worker_id=request.args[2]
        task = 'stop '+worker_id
        pass
    elif command=='test':
        miner_id=request.args[2]
        task = 'test '+miner_id
        pass
    elif command=='quit':
        task = 'quit'
        pass
    else:
        session.error_message = 'SEND_COMMAND: \'' + command + '\' command not recognized'
        redirect(URL(c='error'))
    send_task((ip,port),task)
    sleep(2)
    print 'send_task((',ip,',',port,'),\'',task,'\')'
    redirect(URL(c='machine_cp'))

def test_send():
    send_task(('127.0.0.1',51485),'start 1111')


# ##########################################################
# ## auxiliary functions
# ###########################################################

def send_task(addr, task):
    print 'inicializa el TaskMaster'
    connector = TaskMaster.TaskMaster(addr)
    print 'TaskMaster manda el comando: ' + str(task)
    connector.send_command(task)
    asyncore.loop()
    print 'CALLBACK: ' , connector.get_callback()
