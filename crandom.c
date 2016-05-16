#include <Python.h>
#include <time.h>
#include <stdlib.h>
//#include "_randommodule.c"

PyObject* randommodule;
PyObject* random_function;


long get_python_random_int(size_t below){
  /* Use Python.random to generate random int. 
   */
  PyObject* py_below =  Py_BuildValue("i",below); //passes ownership to us
  PyObject* py_call_args = PyTuple_Pack(1,py_below); //passes ownership, borrows py_below ownership
  PyObject* py_random_call_object = PyObject_CallObject(random_function,py_call_args); //passes ownership, borrows ownerships of args
  
  long rand_val = PyInt_AsLong(py_random_call_object); // borrows ownership of arg

  Py_DECREF(py_below);
  Py_DECREF(py_call_args);
  Py_DECREF(py_random_call_object);

  return rand_val;
};

long get_random_int(size_t below){
  /* Use standard library rand to generate random int.
   */
  return rand()%below;
}


static PyObject* choice_dict(PyObject* self,PyObject* args){
  /* Return a uniformly random element from a Python dict in linear time. 
   */
  const PyDictObject *dict;
  if (!PyArg_ParseTuple(args, "O!", &PyDict_Type ,&dict))
    return NULL;

  size_t used = dict->ma_used;
  size_t table_size = dict->ma_mask+1;

  //printf("Refcount: %u \n",dict->ob_refcnt );
  //printf("ma_used: %u \n",dict->ma_used );
  //printf("Table size (ma_mask+1): %u \n",table_size );
  
  // Check for empty dict, raise ValueError
  if (used==0){
    PyErr_SetString(PyExc_ValueError,"Cannot sample from empty dictionary.");
    return NULL;
  }

  PyObject* key=NULL;
  while (key==NULL){   
    key=dict->ma_table[get_random_int(table_size)].me_key;
  }
  
  //The return value must be owned. The ownership is transferred to receiver. 
  Py_INCREF(key);
  return key;
}

static char choice_dict_docs[] =
    "Returns a uniformly random key from a dict object.\n";

static PyMethodDef crandom_funcs[] = {
    {"choice_dict", (PyCFunction)choice_dict, 
     METH_VARARGS, choice_dict_docs},
    {NULL}
};

void init_crandom(void)
{
  //For generating random numbers
  srand(time(NULL));

  //We can also use Python's own random number genrator.
  //It is much slower to use this.
  randommodule=PyImport_ImportModule("random");
  random_function=PyObject_GetAttrString(PyDict_GetItemString(PyModule_GetDict(randommodule),"_inst"),"_randbelow");

  //debug
  //printf(PyString_AsString(PyObject_Str(random_function)));
  //printf("\n");

  Py_InitModule3("_crandom", crandom_funcs,
		 "Functions for randomly sampling dictionaries.");
}
