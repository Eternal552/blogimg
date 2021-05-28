# CTFDolpine A CTFd Dynamic Enviroment Challenge Plugin !  

## INSTALL  

```
cd ctfd/CTFd/plugins/  

mkdir CTFDolphine  

cd CTFDolphine  

git pull https://gitee.com/s0duku/CTFDolphine.git  

pip3 install -r requirements  

```

## RUN  

```
//under your CTFDolphine workpath to start service 

python3 DockDolphine.py // or you can run background by using 'nohup DockDolphine.py &'  

//once you start the service you can use it on your ctfd

```

## API

```

http://host/ctfdolphine/run/<image name> //start a docker image for current user
http://host/ctfdolphine/stop //stop current user's docker container  
http://host/ctfdolphine/stats // check current user's container state   
http://host/admin/ctfdolphine //our main page waiting for more update (only allow admin user)
 
```    
## 测试  

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202327_8494b546_4944119.png "QG4CO1[J4TW7F7KD]~N{F[4.png")    

### 创建题目  

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202343_f9dc4f95_4944119.png "{(96]N8}9@{IKEAK@X8]E{X.png")  

### 创建成功

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202441_5bc27051_4944119.png "10TY9E])BSTRTDID$_5VRYW.png")   

### 设置题目可见  

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202354_b5980cf5_4944119.png "EE91(~_X]~GUVT}0BM3SD@R.png")  

###  点击 run env 运行环境

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202407_a98c1e79_4944119.png "LNFKKWDX8]GO{XBW@RP}}OP.png")   

### 返回 镜像映射的端口号

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202429_42c8ec35_4944119.png "5W}P7QASUE`4AL30]0P62}F.png")  

### 访问端口

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202452_64209f1d_4944119.png "4G1`N8UWA%R)YAISGC]9G$L.png")  

### 用户二创建环境

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202508_1bba2406_4944119.png "F{`I%4}H6(9N3AM_Z`DI$OT.png")  

### docker ps 查看容器实例

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202520_19e8998c_4944119.png "`(6QC%G4Z~%P3I_ZV_Y6`YL.png")  

### 用户一关闭环境

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202537_63411090_4944119.png "D]3Y`JM$P23(7(GM9AO]T@E.png")  

### docker ps 查看容器实例

![输入图片说明](https://images.gitee.com/uploads/images/2021/0202/202545_363a7701_4944119.png "1NH7(5VSL)RD79UR$V{(NYL.png")



