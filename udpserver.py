from socket import*
server_port = 12000
server_socket = socket(AF_INET,SOCK_DGRAM)  #创建socket
server_socket.bind(('',server_port))    #绑定端口号
while True:
    print("等待连接中·······")
    confirm2 = 0    #赋初值为0
    confirm,clientAddress = server_socket.recvfrom(2048)    #接受client发送的链接请求 接收到1为正确
    confirm2 = int(confirm.decode())    #将上行接受到的数据转为int类型以便if语句判断
    #判断连接
    if confirm2 == 1:
        server_socket.sendto(b"1",clientAddress)    #正确接受后 给client返回一个1
        print("-----连接成功-----")
    else:
        print("-----连接失败-----")
    
    while True:
        select,clientAddress = server_socket.recvfrom(2048)     #接受client发送的操作选项
        select_decode = int(select.decode("utf-8"))     #将上行接受到的操作数转换为int类型以便if语句判断
    
         #client下载文件
        if select_decode == 1:
            print("接受文件名中·······")
            fileName,clientAddress = server_socket.recvfrom(2048)   #接受server传来的文件名
            fileName_decode = fileName.decode("utf-8")     #用utf-8解码上行接受到的文件名
            print("寻找",fileName_decode,"文件")
            try:    #尝试打开该文件名的文件
                f = open(fileName_decode,"rb")      #以读的方式打开该文件
                server_socket.sendto(b"1",clientAddress)    #给client发送1表示找到该文件
                data = f.read()     #将文件数据赋值给data
                f.close()   #关闭文件
                print("开始发送")
                server_socket.sendto(data,clientAddress)    #给client发送文件数据
                print("-----发送完成-----")
            except Exception as ret:    #打开失败
                print("-----找不到该文件-----")
                server_socket.sendto(b"0",clientAddress)    #给client发送0表示没找到该文件
        #client上传文件
        elif select_decode == 2:
            print("接受文件名中······")
            fileName2,clientAddress = server_socket.recvfrom(2048)  #接受client要上传的文件名
            fileName2_decode = fileName2.decode("utf-8")    #用utf-8解码上行接受到的文件名  
            recv_data,client = server_socket.recvfrom(2048)     #接受文件数据
            with open(fileName2_decode,"wb")as f:   #以写的方式打开文件
                print("开始接收")
                f.write(recv_data)     #将文件数据写入文件
                print("-----接受成功-----")
        #client结束程序
        elif select_decode == 3:
            print("-----client断开连接-----")
            break


