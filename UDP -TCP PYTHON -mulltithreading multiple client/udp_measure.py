import os
from datetime import datetime
class UdpJitterStat:

    def __init__(self,UDP_IP,UDP_PORT):
        self.UDP_IP=UDP_IP
        self.UDP_PORT=UDP_PORT
        self.s_cr_time = 0
        self.s_st_time = 0
        self.filename_jitter = "UDP_JITTER "+str(self.UDP_IP)+" "+str(self.UDP_PORT)+" "+ datetime.now().strftime("%m-%d-%H-%M-%S")
        self.save_path_jitter = os.path.realpath(os.path.join(os.getcwd() , os.path.dirname(self.filename_jitter))).replace(
            "\\" ,
            "/") + "/%s.csv"
        self.prev_seq = 0
        self.info_config = str("UDP_IP , UDP_PORT" , )
        print(self.info_config , file=open(self.save_path_jitter % self.filename_jitter , 'a'))
        self.info_config = str([self.UDP_IP ,self.UDP_PORT])
        print(self.info_config , file=open(self.save_path_jitter % self.filename_jitter , 'a'))
        self.D1 = 0
        self.D2 = 0
        self.recv_seq = 0
        self.loss=0


    def run(self,data):
        if int(data.decode().split("'")[1])-1==self.prev_seq:
            self.s_st_time = float(data.decode().split("',")[1].split(':')[2])
            # cr_time = datetime.now().strftime("%H:%M:%S.%f")
            self.s_cr_time = float(datetime.now().strftime("%H:%M:%S.%f").split(':')[2])
            self.D2=self.s_cr_time-self.s_st_time
            self.recv_seq=int(data.decode().split("'")[1])
            print(str(self.D2-self.D1), file=open(self.save_path_jitter % self.filename_jitter , 'a'))
            # appendfile.write(str(D2 - D1) + '\n')
            self.D1=self.D2
            self.prev_seq=self.recv_seq

        else:
            self.prev_seq=int(data.decode().split("'")[1])
            self.D1=float(datetime.now().strftime("%H:%M:%S.%f").split(':')[2])-float(data.decode().split("',")[1].split(':')[2])
            if self.prev_seq>2:
                self.loss+=1
                print("packet_loss: "+str(self.loss) , file=open(self.save_path_jitter % self.filename_jitter , 'a'))

