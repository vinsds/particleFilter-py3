#include "Python.h"
#include "normpdf.h"

double CnormPDF(double x, float m, float v)
{
	double numexp = (-1)*pow(x - m, 2);
	double denexp = 2 * v*v;
	return (1.0 / (v*sqrt(2.0 * pi)))*pow(e,(numexp/denexp));
}


static PyObject* pdf(PyObject* self, PyObject* args)
{
    double x = 0.0;
    float m = 0.0;
    float v = 0.0;

    //DFF double, float, float
    if (!PyArg_ParseTuple(args, "dff", &x, &m, &v))
        return NULL;

    // "d" return type value
    return Py_BuildValue("d", CnormPDF(x, m, v));
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}

static PyMethodDef myMethods[] = {
    {"pdf", pdf, METH_VARARGS, "normPDF function."},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef myPdf = {
	PyModuleDef_HEAD_INIT,
	"myPdf",
	"normPDF",
	-1,
	myMethods
};

PyMODINIT_FUNC PyInit_myPdf(void)
{
    return PyModule_Create(&myPdf);
}
