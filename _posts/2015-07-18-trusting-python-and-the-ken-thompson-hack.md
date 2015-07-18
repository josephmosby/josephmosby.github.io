---
layout: post
title: Trusting Python&comma; and the Ken Thompson hack
---

I have always treated Python compilation as a black box. Code goes in, web services come out, everyone is happy. Then I went through [NAND2Tetris](http://www.nand2tetris.org/) and picked up a copy of [The C Programming Language](http://www.amazon.com/Programming-Language-Brian-W-Kernighan/dp/0131103628/ref=sr_1_1?s=books&ie=UTF8&qid=1437243255&sr=1-1&keywords=the+c+programming+language), and it's been tough to rest as easy ever since. 

Python (in its most common derivative, CPython) is not fed straight into a computer's processor. It's first "interpreted" into C code, which is then compiled by a C compiler into assembly language, which is then translated into 1's and 0's that the computer can actually understand. Let's take a look at this: 

	print('Hello, world!')

That's the incredibly simple Python code for printing "Hello, world!" Here's what that looks like in the Python source code:

	static PyObject *
    builtin_print(PyObject *self, PyObject *args, PyObject *kwds)
    {
        static char *kwlist[] = {"sep", "end", "file", "flush", 0};
        static PyObject *dummy_args;
        PyObject *sep = NULL, *end = NULL, *file = NULL, *flush = NULL;
        int i, err;

        if (dummy_args == NULL && !(dummy_args = PyTuple_New(0)))
            return NULL;
        if (!PyArg_ParseTupleAndKeywords(dummy_args, kwds, "|OOOO:print",
                                         kwlist, &sep, &end, &file, &flush))
            return NULL;
        if (file == NULL || file == Py_None) {
            file = _PySys_GetObjectId(&PyId_stdout);
            if (file == NULL) {
                PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
                return NULL;
            }

            /* sys.stdout may be None when FILE* stdout isn't connected */
            if (file == Py_None)
                Py_RETURN_NONE;
        }

        if (sep == Py_None) {
            sep = NULL;
        }
        else if (sep && !PyUnicode_Check(sep)) {
            PyErr_Format(PyExc_TypeError,
                         "sep must be None or a string, not %.200s",
                         sep->ob_type->tp_name);
            return NULL;
        }
        if (end == Py_None) {
            end = NULL;
        }
        else if (end && !PyUnicode_Check(end)) {
            PyErr_Format(PyExc_TypeError,
                         "end must be None or a string, not %.200s",
                         end->ob_type->tp_name);
            return NULL;
        }

        for (i = 0; i < PyTuple_Size(args); i++) {
            if (i > 0) {
                if (sep == NULL)
                    err = PyFile_WriteString(" ", file);
                else
                    err = PyFile_WriteObject(sep, file,
                                             Py_PRINT_RAW);
                if (err)
                    return NULL;
            }
            err = PyFile_WriteObject(PyTuple_GetItem(args, i), file,
                                     Py_PRINT_RAW);
            if (err)
                return NULL;
        }

        if (end == NULL)
            err = PyFile_WriteString("\n", file);
        else
            err = PyFile_WriteObject(end, file, Py_PRINT_RAW);
        if (err)
            return NULL;

        if (flush != NULL) {
            PyObject *tmp;
            int do_flush = PyObject_IsTrue(flush);
            if (do_flush == -1)
                return NULL;
            else if (do_flush) {
                tmp = _PyObject_CallMethodId(file, &PyId_flush, "");
                if (tmp == NULL)
                    return NULL;
                else
                    Py_DECREF(tmp);
            }
        }

        Py_RETURN_NONE;
    }

I understand very little of what's actually going on here. I do know that ultimately this code has to end up at some sort of terminal output unless I specify otherwise, and I do know that I'll probably do that by writing to a dedicated terminal output memory location which is probably specified by a C pointer, and this is the extent of my understanding. And we haven't even made it to assembly code yet. Or to binary instructions. 

I go on trusting the CPython interpreter because I have no choice. Perhaps the `PyArg_ParseTupleAndKeywords` function has a side effect of batching my printed output up and sending it back to a Python mailing list somewhere, for them to laugh at my coding mistakes. Maybe it's something more nefarious. 

I can look through the CPython source code and see that `PyArg_ParseTupleAndKeywords` does exactly what it says it's going to. But what if the _C compiler itself_ is batching my printed output up and sending it off? In 1984 Ken Thompson described [exactly that](http://c2.com/cgi/wiki?TheKenThompsonHack) with a hack that would allow a compiler to do all sorts of terrible things, including overwriting all evidence of its existence. You could detect it, of course, but you'd have to have a trusted compiler - something that most 2015 developers are not prepared to write. (myself included)

And so I have to trust my computer. I have to trust Intel, Apple, all of the component manufacturers, the `gcc` team, the CPython team, and everybody in between, because I am not prepared to compute otherwise. 