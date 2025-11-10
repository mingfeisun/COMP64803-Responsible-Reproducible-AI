**What user are you logged in as by default?**



root





**If you start and then exit an interactive container, and then use the docker run -it ubuntu:xenial /bin/bash command again, is it the same container? How can you tell?**



No, the container is not the same. Each time the command is run, another instance of the container is created from the image. This is clear from the terminal, where the 12 container identification characters following root@<container\_id> differ, ie: root@1ce517b02565 vs root@5cb24284e694.





**Run the image you just built. Since we specified the default CMD, you can just do docker run -it mypython:latest. What do you observe?**



This launched a python 3.6 interactive interpreter (REPL) running inside the Ubuntu container, where anything I type executes in an isolated environment (to my machine). The container stops when I press Ctrl+D or exit().





**Write and build a Dockerfile that installs the packages fortune and fortunes-min and runs the fortune executable (located in /usr/games/fortune after you install it). Note that you won’t need to use the -it flags when you run the container as fortune doesn’t need STDIN. Submit your Dockerfile with this lab. Hint: if you’re having trouble writing your Dockerfile, try booting an interactive container and installing both packages. Translate what you did into a Dockerfile. How can you translate what you did interactively to a Dockerfile?**



See attached





**Paste the output of your docker images command after questions 1 and 2.**



Q1 Output:

Python 3.6.9 (default, Mar 10 2023, 16:46:00) 

\[GCC 8.4.0] on linux

Type "help", "copyright", "credits" or "license" for more information.

>>> 



Q2 Output:

You are always busy.



docker images:

REPOSITORY                     TAG       IMAGE ID       CREATED         SIZE

fortune                        latest    1b0ce44fe913   5 minutes ago   121MB       

mypython                       latest    50bbe0657c2f   15 hours ago    219MB  





**With httpd running in a detached container, run /bin/bash on the same container and paste the output of ps aux. Observe that there’s very few processes running as compared to running ps aux on your VM. Why is this the case?**



USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND

root           1  0.0  0.0   6212  4732 ?        Ss   14:32   0:00 httpd -DFOREGROUN

www-data       8  0.0  0.0 1997388 3884 ?        Sl   14:32   0:00 httpd -DFOREGROUN

www-data       9  0.0  0.0 1997388 3884 ?        Sl   14:32   0:00 httpd -DFOREGROUN

www-data      15  0.0  0.0 1997388 3884 ?        Sl   14:32   0:00 httpd -DFOREGROUN

root         104  0.0  0.0   4332  3584 pts/0    Ss   14:37   0:00 /bin/bash        

root         234  0.0  0.0   6396  3712 pts/0    R+   14:38   0:00 ps aux



running ps aux inside httpd container there are less processes as containers are lightweight and designed to run one primary process (+ its dependencies) compared to booting an entire OS and initialising system services. The container also doesn't require an independent kernel, and can rely on the host's kernel for process management \& networking etc.

