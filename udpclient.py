from socket import*
server_ip = input("请输入server的ip:") 
client_port = 12000 
client_socket = socket(AF_INET,SOCK_DGRAM)  #创建socket
client_socket.sendto(b"1",(server_ip,client_port))  #向server发送一个1请求连接
confirm,serverAddress = client_socket.recvfrom(2048)    #接受来自server返回的数据到confirm
confirm2 = 0    #赋初值为0
confirm2 = int(confirm.decode())    #将接受到的数据转换为int类型
if confirm2 == 1:   #当接受为1时表示连接server成功
    print("连接到sever")
else:
    print("连接失败")
#功能目录
print("1:下载文件")
print("2:上传文件")
print("3:结束程序")

while True:
    select = input("请输入选项:")   #输入功能对应的操作选项
    select_int = int(select)   #将上行输入的操作数转化为int类型用于if语句判断 
    client_socket.sendto(select.encode(),(server_ip,client_port))   #将输入的操作数发送给server以便其运行对应功能
    #下载文件
    if select_int == 1:
        fileName = input("文件名字：")  #输入文件名
        client_socket.sendto(fileName.encode(),(server_ip,client_port))    #将文件名发送给server
        client_T,sendAddress = client_socket.recvfrom(2048)    #接受server传回的反馈 0表示没有该文件 1则找到文件
        re = int(client_T.decode()) #将上行的数据转换成int类型以便if语句判断

        if re==0:
            print("-----找不到该文件-----")
        else:
            recv_data,serverAddress = client_socket.recvfrom(2048)  #接受文件数据
            with open(fileName,"wb")as f:   #以写的方式打开文件
                print("开始接收")
                f.write(recv_data)  #将接受到的文件数据写入文件
                print("-----接受成功-----")
    #上传文件        
    elif select_int == 2:
        fileName2 = input("请输入文件名")   #输入文件名
        client_socket.sendto(fileName2.encode(),(server_ip,client_port))    #将文件名发送给server
        print("寻找",fileName2,"文件")
        #尝试打开文件
        try:
            f = open(fileName2,"rb")    #以读的方式打开该文件
            data = f.read()     #将文件的数据赋给data
            f.close()   #关闭文件
            print("开始发送")
            client_socket.sendto(data,(server_ip,client_port))  #将文件数据发送给server
            print("-----发送完成-----")
        #打开失败
        except Exception as ret:
            print("-----找不到该文件-----")
    #结束程序
    elif select_int == 3:
        client_socket.close()   #关闭socket
        break   #退出循环
