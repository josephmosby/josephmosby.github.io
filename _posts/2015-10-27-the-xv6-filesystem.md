---
layout: post
title: The xv6 filesystem
---

The file system of an operating system is one of those things I haven't thought about in years, ever since I went through the painful process of reformatting USB sticks when different versions of Windows used different file systems. But I've never really thought about how those things have to be implemented. 

On xv6, files are either data files, which are "uninterpreted byte arrays," and directories, which are references to data files or other directories. So a directory is nothing more than a special file that points to other files. Cool. Directories form a tree starting at the root, and a path is a set of directories going out from the root. If a path doesn't start with a root, paths start from the current working directory of a given process. 

That means `chdir()` is a system call that changes the current working directory of a process, and `mkdir()` is the system call that creates a new directory. `mknod()` is a similar call that creates a kernel device (such as a keyboard). When a process opens the kernel device file, the kernel will redirect the `read()` and `write()` to the kernel device instead of to a specific data file.

The `fstat()` call gives information about a specific object that a file descriptor points to. `fstat(fd)` takes in a file descriptor and returns a C `struct` called `stat`, which has an implementation that looks something like this:

	#define T_DIR 1 // directory
	#define T_FILE 2 // file
	#define T_DEV 3 // device

	struct stat {
		short type; // type of file
		int dev; // file system's disk device
		uint ino; // inode number
		short nlink; // number of links to file
		uint size; // size of file in bytes
	}

The name of the file is not included in this information table, because names are distinct from the actual file. An "inode" is the only unique identifier of a file that the kernel sees: names are just "links" back to an individual inode. Thus the following system calls will create two names for a file with the same inode:

	open("a", O_CREATE|O_WRONLY);
	link("a", "b");

Calling `fstat()` on either of the file descriptors attached to "a" or "b" will demonstrate that they're tied back to the same file with the same inode number. `unlink()` will do the opposite of `link()`. It deletes the name, but will not delete the file itself.

In xv6, these types of operations are implemented as user-level programs, rather than baking the system calls into the shell itself. `mkdir` is not a direct call to the system, but a user program that calls the `mkdir()` system call. Same with `rm`. `cd` is a notable exception, because it changes the working directory of the shell itself rather than a child process of the shell.

And that's it for the xv6 system calls! I can treat the xv6 kernel as something abstracted away now that I have all of the system calls for interacting with it. 