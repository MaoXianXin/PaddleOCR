# 护照OCR推理服务

## 系统环境配置

**使用的系统**

准备工作：
1、下载Ubuntu20.04.6镜像
Ubuntu 20.04.6 LTS (Focal Fossa)
下载链接: https://releases.ubuntu.com/focal/ubuntu-20.04.6-live-server-amd64.iso

2、使用1下载的iso文件，制作系统启动U盘，在设备上安装系统（建议先格式化硬盘，再安装）

3、Ubuntu系统安装完成，启动之后，下载并安装2080Ti显卡配套的驱动:
注：显卡驱动安装的依赖：gcc、make，需要确认并安装好。
(直接下载地址：https://us.download.nvidia.cn/XFree86/Linux-x86_64/550.107.02/NVIDIA-Linux-x86_64-550.107.02.run)
下载地址: https://www.nvidia.com/download/index.aspx
选项:

```
Product Type: GeForce
Product Series: GeForce RTX 20 Series
Product: GeForce RTX 2080Ti
Operating System: Linux 64-bit
Download Type: Production Branch
Language: English(US)
```

按照上述选项进行search后出来如下信息，然后下载就可以:
```
Linux X64 (AMD64/EM64T) Display Driver

Version:	550.107.02
Release Date:	2024.7.29
Operating System:	Linux 64-bit
Language:	English (US)
File Size:	293.02 MB
```

## 安装显卡操作步骤

### 挂载磁盘(可选)

```
# 查找U盘设备
sudo fdisk -l
# 输出中你会看到类似 /dev/sdb1 或者 /dev/sdc1 这样的设备名称（具体取决于你的U盘在系统中的挂载情况）。这些名称通常与 /dev/ 开头，后面的数字表明分区。找到对应的U盘设备

# 创建挂载目录
sudo mkdir /home/usb

# 挂载U盘
sudo mount /dev/sdb1 /home/usb

# 卸载U盘
sudo umount /home/usb
# 如果收到“设备忙”的提示，可以尝试以下命令强制卸载
sudo umount -l /home/usb
```

### 开始安装

```
# 注意需要先安装完vim、gcc和make才行
分别进入到vim_deb、ubuntu20_gcc_make_net目录下，再运行 sudo dpkg -i *.deb 进行安装

# 编辑文件blacklist.conf
sudo vim /etc/modprobe.d/blacklist.conf

# 在文件最后部分插入以下两行内容
blacklist nouveau
options nouveau modeset=0

# 更新系统
sudo update-initramfs -u

# 接下来关闭图形界面
sudo systemctl set-default multi-user.target
sudo reboot

# 验证nouveau是否已禁用
lsmod | grep nouveau
# 没有信息显示，说明nouveau已被禁用，接下来可以安装nvidia的显卡驱动


# 关闭图形界面重启后， 需要 ctrl+alt+F1 切换到命令行模式

# 给驱动run文件赋予执行权限
sudo chmod  a+x NVIDIA-Linux-x86_64-550.120.run

sudo ./NVIDIA-Linux-x86_64-550.120.run -no-x-check -no-nouveau-check -no-opengl-files 
# 只有禁用opengl这样安装才不会出现循环登陆的问题

# 安装完毕之后，挂载Nvidia驱动
modprobe nvidia

# 检查驱动是否安装成功
nvidia-smi

# 开启用户图形界面
sudo systemctl set-default graphical.target
sudo reboot
```

2080Ti显卡安装结果验证：使用 nvidia-smi 查看即可

4、安装Docker
下载链接: https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/

需要下载这个链接下的这几个文件:
```
containerd.io_1.7.19-1_amd64.deb
docker-buildx-plugin_0.16.1-1~ubuntu.20.04~focal_amd64.deb
docker-ce-cli_27.1.1-1~ubuntu.20.04~focal_amd64.deb
docker-ce_27.1.1-1~ubuntu.20.04~focal_amd64.deb
docker-compose-plugin_2.6.0~ubuntu-focal_amd64.deb
```

下载完后运行下面的指令进行安装

```
sudo dpkg -i ./containerd.io_1.7.19-1_amd64.deb \
  ./docker-buildx-plugin_0.16.1-1~ubuntu.20.04~focal_amd64.deb \
  ./docker-ce-cli_27.1.1-1~ubuntu.20.04~focal_amd64.deb \
  ./docker-ce_27.1.1-1~ubuntu.20.04~focal_amd64.deb \
  ./docker-compose-plugin_2.6.0~ubuntu-focal_amd64.deb
```

最后启动一下Docker，无错误信息即启动成功
```
sudo service docker start
```

安装完docker后运行下面的指令:

```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

5、安装Nvidia-Docker
下载链接: https://github.com/NVIDIA/libnvidia-container/tree/gh-pages/stable/ubuntu18.04/amd64
下载以下几个文件并安装

```
libnvidia-container-tools_1.13.5-1_amd64.deb
libnvidia-container1_1.13.5-1_amd64.deb
nvidia-container-toolkit-base_1.13.5-1_amd64.deb
nvidia-container-toolkit_1.13.5-1_amd64.deb
nvidia-docker2_2.13.0-1_all.deb
```

下载完后运行下面的指令进行安装

```
sudo dpkg -i ./libnvidia-container-tools_1.13.5-1_amd64.deb \
  ./libnvidia-container1_1.13.5-1_amd64.deb \
  ./nvidia-container-toolkit-base_1.13.5-1_amd64.deb \
  ./nvidia-container-toolkit_1.13.5-1_amd64.deb \
  ./nvidia-docker2_2.13.0-1_all.deb
```

重启系统后，运行下述指令验证Nvidia-Docker安装是否成功：
```
sudo docker run --gpus all nvidia/cuda:12.5.1-base-ubuntu20.04 nvidia-smi
```