lltypes
=======

A type system for Python backed by llvm and ctypes

This project is a low-level type system with a focus on plain-old-data (POD).  In other words, it provides 
Python objects that represent a "low-level type" (and a way for users of the library to create new ones easily 
--- preferrably via class syntax) that have at least the following methods: 

 * to_llvm  --- return a binary compatible llvm type (via llvmpy)
 * to_ctypes --- return a binary compatible ctypes object
 * to_dtype --- return a NumPy dtype object (or at least a python object, obj, 
                  that could be used with numpy.dtype(obj) to 
                  create the dtype to avoid a hard-dependency on NumPy).  
 
The llvm_array object should live in this project instead of llvmpy. 

This project can serve as a common type-system that bridges llvm types and ctypes and allows
other projects to wrap it to build their own type-system as needed.

This project will be successful if numba, and blaze-datashape (dynd-python) use it.
It will be wildly successful if llpython, parakeet, NumPy, and other projects use it. 

Out of scope for this project are (at least):

   * promotion rules
   * multiple dispatch notions 
