# Documentation CDS Working Stations
# How to connect and use it?


In this documentation, we would like to show how to connect and how to use the workstations made available for the bachelor program "Computational and Data Science" at the University of Applied Sciences of the Grisons. 

Three workstations are available for use:

1. Helium: helium.fhgr.ch
2. Iridium: iridum.fhgr.ch
3. Krypton: krypton.fhgr.ch


## How to connect to the workstations
To connect to the workstations, you first need to establish a VPN connection. The VPN connection is set up through the software Pulse Secure. For further information concerning Pulse Secure, please refer to the documentation of the IT of the University.

We connect to the workstation through an SSH or Secure Shell connection. On Linux or Mac we use for this purpose the terminal. On Windows you can use Putty or any Bash command line program. 

In Bash the command for making an SSH connection, for example to helium is:
```
ssh username@helium.fhgr.ch
```
You will be asked for you **password**. The password is the one you got from the University to login to Moodle or VPN. 

## Interact with the workstation
The objective in this document is, to run your code for some calculations. This could be code for machine learning, deep learning, or simulation. On the workstation you do not have root privileges, such as sudo or su. Therefore you cannot install packages or software using apt.

There are two options to install packages/modules that are required by your program: Apptainer or Anaconda. In the case of Anaconda, we need to install Anaconda first. As we do not have root privileges, we will insall Anaconda to the home directory. So, all users are self-responsible for updating and setting up their Anaconda installation. 


### Installation of Anaconda
To install Anaconda, we first need to download the program. You can find the latest version for Linux at https://repo.anaconda.com/archive/. At the time of writing of this document, the download link for the latest version was https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh 

 As an example, one way to download Anaconda to one of the workstations is:
```
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
```
Once the download is finished, we can install the program with the following command: 
```
bash Anaconda3-2022.10-Linux-x86_64.sh
```
You need to **accept** the license agreement and usually you can accept the suggested installation path, which is by default set to your home directory. The installation will take some time. Say **yes** to initialize (init) Anaconda. Before being able to use Anaconda, you need to logout from the workstation and reconnect. 

### Setting up your anaconda environment
For all projects you should set a new Anaconda environment. The environment can be set up manually or by importing an existing one from your computer. How to use Anaconda, is beyond the scope of this doucment. Please refer to the Anaconda documentation at https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment.


## Running your Code on a workstation
### Files and Directories
Now, you have set up an Anaconda environment containing a Python environment and are therefore almost ready to run your first code. 

As you might have realized by now, you do not have a graphical user interface (GUI) on the workstations. So you must organize your files and folders using bash commands, such as 'ls', 'mkdir' or 'rm'. 

We create a directorie (aka. folder on Windows) for our project. With the following command we can create a test directory:
```
mkdir test
```

With the command 
```
ls
```
we can print all files and directories in the actual location. When we enter the workstation, we always start in the home. 

To move from the home for example to the test folder, we can do this with the command change directory: 
```
cd test
```

A file can be created with the text editor vim. I can create a test python file with following command: 
```
vim test.py
```
The file is initially empty. To write something inside the newly created file, I need to push the keyboard button <kbd>i</kbd>. Now I can put some text in the file. For example:
```
print("Hello Kitty")
```
To save the lines I need first to push the keyboard <kbd>ESC</kbd> and the <kbd>:</kbd><kbd>w</kbd><kbd>q</kbd>

Using the 'ls' command (as mentioned above) you can verfiy that a new file has been created in the current directory. 

### Screen Connection
As most calculations are running longer than a few minutes, it is important to open a virtual terminal on the workstation. If you do not set up a virtual terminal, your running task will be terminated if you lose your network connection or the SSH session times out.

To open a new virtual session, we use the command
```
screen
```

Now, a new virtual session is opened, we are almost ready to run our first code. Always when I create a new screen session, I need to first activate my anaconda environment. When this is done, I can run my Python code:
```
python test.py
```

In the terminal you cannot use <kbd>CTRL</kbd><kbd>C</kbd> to copy text. This key combination is used to **stop** commands in a terminal. 
To exit the virtual terminal without stopping the running process, we use the keyboard command <kbd>CTRL</kbd><kbd>A</kbd><kbd>D</kbd>. 

We access the running virtual terminal with command 
```
screen -r
```
If you finished a job, the best is to close the session with exit. 


## Copy Code
Most of the time, we develop the code on our local computers. We can copy our anaconda environment or our files with the following command to the working stations:
```
scp path_my_laptop/file_name username@helium.fhgr.ch:/home/project_file/.
```


## Conclusion
With these steps you know the most important steps to get started with a terminal.
