---
layout: post
title: Forks and file descriptors - an intro to Unix concepts
---

I'm exploring MIT's course on Operating System Engineering in the hopes to get a better feel for how Linux works under the hood, and it's already answered a few questions about the things I was seeing in `ps` earlier. Though the OS course deals with a Unix variant (not Linux), the low-level architecture is similar enough that I think I can assume Linux operates the same way.

xv6, the Unix variant used in this course, has a kernel that interfaces with hardware and user-level programs. This creates the notion of "user space" and "kernel space," with a single process jumping back and forth between the two to complete its work. When the process needs to use one of the services from the kernel, it invokes a system call - a specific function in the kernel.

Unix provides these services (and many more, but this appears to be all xv6 offers):

1. `fork()`, which creates a process
2. `exit()`, which terminates the current process
3. `wait()`, which waits until a child process exits
4. `kill(pid)`, which kills a process with the given PID
5. `getpid()`, return current process's PID
6. `sleep(n)`, sleep for n seconds
7. `exec(filename, *argv)`, load a file and execute it with the given arguments
8. `sbrk(n)`, increase process memory by n bytes
9. `open(filename, flags)`, open a file with read or write flags
10. `read(fd, buf, n)`, read n bytes from an open file into a buffer `buf`
11. `write(fd, buf, n)`, write n bytes from a buffer `buf` into an open file
12. `close(fd)`, release open file fd
13. `dup(fd)`, duplicate fd
14. `pipe(p)`, create a pipe and return fd's in p
15. `chdir(dirname)`, change the current directory
16. `mkdir(dirname)`, create a new directory
17. `mknod(name, major, minor)`, create a device file
18. `fstat(fd)`, return info about an open file
19. `link(f1, f2)`, create another name (f2) for the file f1
20. `unlink(filename)`, remove a file

The shell uses each of the system calls to do its work. It's just a run-of-the-mill program like anything else. 

The xv6 textbook provides the following mini-example of a program using fork to do its work. I want to give it a shot running on my own machine. Here's how the proram is written in the textbook:

	int pid;

	pid = fork();

	if(pid > 0){

	printf("parent: child=%d\n", pid);

	pid = wait();

	printf("child %d is done\n", pid);

	} else if(pid == 0){

	printf("child: exiting\n");

	exit();

	} else {

	printf("fork error\n");

	}
 
 And here's how I had to tweak it to get it running on my Mac:

 	#include <stdio.h>
	#include <unistd.h>
	#include <stdlib.h>

	int main(int argc, char **argv) {
		int pid;

		pid = fork();
		if(pid > 0) {
	        printf("parent: child=%d\n", pid);
	        pid = wait(0);
	        printf("child %d is done\n", pid);
		} else if(pid == 0) {
	        printf("child: exiting\n");
	        exit(0);
		} else {
		    printf("fork error\n");
		}

		return 0;
	}

The `stdio.h` library makes sense, because that's what contains the `printf()` functions to dump things out to the console. I received an error when I tried to use `fork()` without `unistd.h`, so I'm assuming `fork()` sits there, and I received more errors when I tried to use `wait()` and `exit()` without `stdlib.h`. `fork()` contains the same memory contents of the parent process - in the parent process, `fork()` will return the child's PID, but in the child, it will return 0 - so we see the `if` statements trigger for the child and for the parent.

`exec()`, by contrast, doesn't return to the parent process. It replaces the calling process with a new process stored somewhere in the file system. Let's take a look at the textbook's pseudocode:

	char *argv[3];

	argv[0] = "echo";
	argv[1] = "hello";
	argv[2] = 0;
	exec("/bin/echo", argv);
	printf("exec error\n");

Try as I might, I couldn't get this program into a usable shape where it would run. After two nights banging my head against it, I decided to scrap it - mostly because I get the gist of what it's going for. Here was where I finished up:

	#include <stdio.h>
	#include <stdlib.h>
	#include <unistd.h>

	int main() {
        char args[3];
        args[0] = "echo";
        args[1] = "hello";
        args[2] = "0";
        exec("/bin/echo", args);
        printf("exec error\n");
	}

I think that the probably may ultimately have something to do with the differing implementations of a Mac OS (where I'm testing this) versus a true Linux platform. At any rate, this helps me understand what my shell is doing! It's doing a combo of these two programs to execute any program I type into the shell. It first takes my command from the command line, then `fork`s the command line process, calls my command using `exec`, waits for the command to finish, then returns control using `wait()`. And that's why certain processes don't immediately jump back over to shell control (things like `vi` for example), because the `fork`ed process hasn't given control back until I close `vi`. 

Ooh, and this also helps `systemd` make more sense. I suspect that `systemd` takes control of PID 1 and then immediately loops through anything in the `/etc/systemd/system/` folder to start launching services based on the configuration files there, `fork`ing processes as it goes.

Next up on our list of functionality is I/O, where we start with file descriptors. According to the text, a file descriptor is an integer tied to some kernel-managed file object. User-level programs deal with the file object through the `read()` and `write()` system calls. The `read(fd, buf, n)` call takes in a file descriptor integer and reads `n` bytes into buffer `buf`. Subsequent calls to `read()` will start where `n` stopped. If we called `read(12, buf, 512)`, we would read 512 bytes from `fd` 12 into buffer `buf` on the first read. If we called it again, we would start at byte #512 then read another 512 bytes (ending at 1024). `write(fd, buf, n)` follows a similar pattern, writing `n` bytes from buffer `buf` to file descriptor `fd`.

Here is the pseudocode given for a simple `cat`-like program:

	char buf[512];
	int n;

	for(;;) {
		// with file descriptor 0, read 512 bytes from file
		n = read(0, buf, sizeof buf);

		if(n == 0) {
			// if we've reached the end
			break;
		}

		if(n < 0) {
			// if n less than 0, error
			fprintf(2, "read error");
			exit();
		}

		if(write(1, buf, n) != n) {
			// write to output object 1, log if error
			fprintf(2, "write error");
			exit();
		}
	}

So I read from `fd` 0 to a buffer, then write from that buffer to an output object. That could be a terminal output:

	cat myfile.txt

or piped to a command:

	cat myfile.txt | awk --something something--

or written to another file:

	cat myfile.txt > myfile2.txt

`cat` doesn't have to care, it's reading and writing to any descriptor that's given to it. 

Rounding out the file descriptor system calls is `dup()`. `dup()` takes in a file descriptor integer and returns another file descriptor that points to the same file. 

The file descriptor mechanism is way more powerful than I originally gave it credit for. It's a simple little trick, but it's brilliant - because things can write to a "file", even if it's not a file at all. The user processes can treat them all the same way.

Okay, I'm going to put a stop to things there before moving on to pipes! 