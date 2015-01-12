---
layout: post
title: A brief word on __main__
tags:
- pymod
---

Okay, `__main__` is technically a Python module. Technically, it's the scope of the program that's currently being executed.

I wanted to find something interesting about `__main__`, I really did. But there's nothing out there. All you really need this for is this:

	if __name__ == "__main__":
		main()

That little snippet will execute a `main()` function if your program is currently being executed (i.e., not a module of another program). And that's it. It's good to know it's there, and now that we know, we can move on.