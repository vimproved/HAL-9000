#include <stdio.h>
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <unistd.h>

extern void *pps(void *fbuf, unsigned long insiz);
extern void mfree(void *mbuf, unsigned long bufs);

PyObject *parsepoll(void *inbuf, unsigned long insiz) {
	PyObject   *out;
	void   *conical;
	printf("test.\n");
	conical = pps(inbuf, insiz);
	if (((unsigned long) conical) == 0) {
		printf("Parsepoll has detected an invalid poll.\n");
		out = Py_BuildValue("k", 257); //I have to use 257 as an error value because building a value from any lower integer segfaults.
		return out;
	}
	printf("testb.\n");
	out     = Py_BuildValue("y#", (const char*)conical, (Py_ssize_t) *((unsigned long*) conical)+24); 
	printf("testc.\n");
	mfree(conical, *((unsigned long*) conical)+24);
	return out;
}
