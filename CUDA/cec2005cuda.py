#!/usr/bin/python
#
# CEC 2005 benchmark functions on CUDA
# Copyright (C) 2011   Robert Nowotniak
#

import sys, time
import pycuda.driver as cuda
import pycuda.gpuarray
import numpy as np
from pycuda.compiler import SourceModule

cuda.init()

dev = cuda.Device(1)
print dev.name()
ctx = dev.make_context()

nfunc = 1;
nreal = 50;

dtype = np.double

print 'devices:', cuda.Device.count()

src = ''.join(open('cec2005.cu').readlines())


#
# Allocation and initialization of common data structures for the benchmark functions
#
initialized_parameters = None
def initialize(function_number, threads = 1, grid = (1,1)):
    total_threads = threads * grid[0] * grid[1]
    # initialize only once for subsequent calls of the same benchmark function
    global initialized_parameters
    if initialized_parameters == (function_number, threads, grid):
        return
    initialized_parameters = (function_number, threads, grid)

    print '--- Allocating memmory, initializing benchmark function(s) ---'

    global module
    # compile the kernel source for given dimension and proper blocksize
    module = SourceModule(src, arch='sm_13', no_extern_c = True, options= \
            ['--use_fast_math', '--ptxas-options=-v', \
            '-D NREAL=%d'%nreal, '-D NFUNC=%d'%nfunc, '-D BLOCKSIZE=%d'%threads])

    # PRNG initialization
    global rngStates, initRNG
    rngStates = cuda.mem_alloc(40 * total_threads)  # sizeof(curandState) = 40 bytes
    cuda.memcpy_htod(module.get_global('rngStates')[0], np.intp(rngStates)) # set pointer in kernel code
    initRNG = module.get_function('initRNG')
    initRNG(np.uint32(time.time()), block=(threads,1,1), grid = grid)

    # rw data structures (separate for each thread)
    global g_trans_x, g_temp_x1, g_temp_x2, g_temp_x3, g_temp_x4, \
            g_norm_x,  g_basic_f, g_weight, g_norm_f

    # constant (same for each thread)
    global sigma, lambd, bias, o, g, l, o_gpu, o_rows, g_gpu, g_rows, l_gpu
    
    # constant scalars
    cuda.memcpy_htod(module.get_global('nreal')[0], np.int32(nreal))
    cuda.memcpy_htod(module.get_global('nfunc')[0], np.int32(nfunc))
    cuda.memcpy_htod(module.get_global('C')[0], np.double(2000))
    cuda.memcpy_htod(module.get_global('global_bias')[0], np.double(0))

    # rw arrays (memmory allocation only, no initialization)
    g_trans_x = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x1 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x2 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x3 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x4 = np.zeros(nreal * total_threads).astype(dtype)
    g_norm_x  = np.zeros(nreal * total_threads).astype(dtype)
    g_basic_f = np.zeros(nfunc * total_threads).astype(dtype)
    g_weight  = np.zeros(nfunc * total_threads).astype(dtype)
    g_norm_f  = np.zeros(nfunc * total_threads).astype(dtype)

    # constant arrays
    sigma = np.zeros(nfunc).astype(dtype)
    lambd = np.ones(nfunc).astype(dtype)
    bias = np.zeros(nfunc).astype(dtype)

    # 2d arrays
    o = np.zeros((nfunc,nreal)).astype(dtype)
    g = np.eye(nreal,nreal).astype(dtype)

    if function_number == 1:
        # wczytanie 'o' mozna bedzie pewnie zamienic na 1-linijkowy kod (o = np.matrix(''.join... itp
        fpt = ''.join(open('input_data/sphere_func_data.txt', 'r').readlines()).strip().split()
        for i in xrange(nfunc):
            for j in xrange(nreal):
                o[i,j] = dtype(fpt.pop(0))
        bias[0] = -450.0
    elif function_number == 2:
        fpt = ''.join(open('input_data/schwefel_102_data.txt', 'r').readlines()).strip().split()
        for i in xrange(nfunc):
            for j in xrange(nreal):
                o[i,j] = dtype(fpt.pop(0))
        bias[0] = -450.0
    elif function_number == 3:
        fpt = ''.join(open('input_data/elliptic_M_D%d.txt' % nreal, 'r').readlines()).strip().split()
        for i in xrange(nreal):
            for j in xrange(nreal):
                g[i,j] = dtype(fpt.pop(0))

        fpt = ''.join(open('input_data/high_cond_elliptic_rot_data.txt', 'r').readlines()).strip().split()
        for i in xrange(nfunc):
            for j in xrange(nreal):
                o[i,j] = dtype(fpt.pop(0))
        bias[0] = -450.0
    elif function_number == 4:
        fpt = ''.join(open('input_data/schwefel_102_data.txt', 'r').readlines()).strip().split()
        for i in xrange(nfunc):
            for j in xrange(nreal):
                o[i,j] = dtype(fpt.pop(0))
        bias[0] = -450.0
    elif function_number == 5:
        global A, B
        fpt = open('input_data/schwefel_206_data.txt', 'r')
        o = np.matrix(fpt.readline().strip(), dtype)[0,:nreal]
        A = np.matrix(np.matrix(';'.join(fpt.readlines()))[:nreal,:nreal], dtype)
        B = np.zeros(nreal).astype(dtype)
        if nreal % 4 == 0:
            index = nreal / 4
        else:
            index = nreal / 4 + 1
        for i in xrange(index):
            o[0,i] = -100
        index = (3 * nreal) / 4 - 1
        for i in xrange(index, nreal):
            o[0,i] = 100
        for i in xrange(nreal):
            for j in xrange(nreal):
                B[i] += A[i,j] * o[0,j]
        A = cuda.to_device(A)
        B = cuda.to_device(B)
        cuda.memcpy_htod(module.get_global('A')[0], np.intp(A))
        cuda.memcpy_htod(module.get_global('B')[0], np.intp(B))
        bias[0] = -310.0
    elif function_number == 6:
        fpt = ''.join(open('input_data/rosenbrock_func_data.txt', 'r').readlines()).strip().split()
        for i in xrange(nfunc):
            for j in xrange(nreal):
                o[i,j] = dtype(fpt.pop(0)) - 1
        bias[0] = 390

    # 6 1-dimensional arrays
    arrays = ['g_trans_x', 'g_temp_x1', 'g_temp_x2', 'g_temp_x3', 'g_temp_x4', 'g_norm_x']
    for var in arrays:
        globals()[var] = cuda.to_device(globals()[var]) # send to device and save the pointer
        cuda.memcpy_htod(module.get_global(var)[0], np.intp(globals()[var])) # set pointer in kernel code

    # 6 1-dimensional arrays
    arrays = ['g_basic_f', 'g_weight', 'sigma', 'g_norm_f']
    for var in arrays:
        globals()[var] = cuda.to_device(globals()[var])
        cuda.memcpy_htod(module.get_global(var)[0], np.intp(globals()[var]))
    #lambd = cuda.to_device(lambd)
    cuda.memcpy_htod(module.get_global('lambda')[0], lambd)
    cuda.memcpy_htod(module.get_global('bias')[0], bias)

    # 2 2-dimensional arrays (o, g)
    # MAYBE IT SHOULD BE CASTED to 1-d ARRAY for performance?

    print 'o:', o
    #o_gpu = cuda.to_device(np.zeros(nfunc).astype(np.intp))
    #o_rows = []
    for i in xrange(o.shape[0]):
        cuda.memcpy_htod(module.get_global('o')[0] + i * 50 * 8, o[i,:])
        #row = cuda.to_device(o[i,:])
        #cuda.memcpy_htod(int(o_gpu) + np.intp().nbytes * i, np.intp(row))
        #o_rows.append(row)
        #cuda.memcpy_htod(int(o_gpu) + np.intp().nbytes * i, np.intp(row))
    #cuda.memcpy_htod(module.get_global('o')[0], np.intp(o_gpu))

    # watch out! 'g' is nreal x nreal
    #g = np.linspace(21,21 + nreal*nreal-1,nreal*nreal).reshape((nreal,nreal))
    print 'g:',g
    #g_gpu = cuda.to_device(np.zeros(nreal).astype(np.intp))
    #g_rows = []
    for i in xrange(g.shape[0]):
        cuda.memcpy_htod(module.get_global('g')[0] + i * 50 * 8, g[i,:])
        #row = cuda.to_device(g[i,:])
        #g_rows.append(row)
        #cuda.memcpy_htod(int(g_gpu) + np.intp().nbytes * i, np.intp(row))
    #cuda.memcpy_htod(module.get_global('g')[0], np.intp(g_gpu))

    # 'l' (3d array) -- flatten to 1d
    l = np.zeros((nfunc,nreal,nreal)).astype(dtype)
    #l = np.linspace(3, 3 + nfunc*nreal*nreal-1,nfunc*nreal*nreal).reshape((nfunc,nreal,nreal))
    for i in xrange(nfunc):
        l[i,:,:] = np.eye(nreal)
    print 'l:',l
    print 'l flatten:', l.flatten()
    #l_gpu = cuda.to_device(l.flatten().astype(dtype))
    #print l_gpu
    cuda.memcpy_htod(module.get_global('l_flat')[0], l);

    print '--- initialization done ---'


# Actual benchmark functions

def f1(x):
    x = np.matrix(x, dtype)
    initialize(1, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f1')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def f2(x):
    x = np.matrix(x, dtype)
    initialize(2, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f2')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def f3(x):
    x = np.matrix(x, dtype)
    initialize(3, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f3')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def f4(x):
    x = np.matrix(x, dtype)
    initialize(4, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f4')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def f5(x):
    x = np.matrix(x, dtype)
    initialize(5, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f5')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def f6(x):
    x = np.matrix(x, dtype)
    initialize(6, threads = x.shape[0])
    bench = module.get_function('calc_benchmark_func_f6')
    res = np.zeros(x.shape[0], dtype)
    bench(cuda.In(x), cuda.Out(res), block=(x.shape[0],1,1))
    return res

def test_time(blocksize = 100, blocks = 1, repeat = 1):
    global module
    nreal = 50
    x = (np.random.random(nreal * blocksize * blocks) - 0.5) * 200
    initialize(6, threads = blocksize, grid = (1,blocks))
    bench = module.get_function('test_time')
    res = np.zeros(blocks * blocksize, dtype)
    t = bench(cuda.In(x), cuda.Out(res), np.int32(repeat),block=(blocksize,1,1), grid = (1,blocks), time_kernel = True)
    return t


if __name__ == '__main__':

    cuda.Context.pop()
    sys.exit(0)

    #x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype)
    nreal = 2
    # x = np.array([-39.3119, 58.8999], dtype) # opt for 2d
    # x = np.array([-39.3119, 58.8999, -46.3224, -74.6515, -16.7997, -80.5441, -10.5935,  24.9694, 89.8384, 9.1119]) # opt for 10D
    # x = np.array([-39.3119,58.8999,-46.3224,-74.6515,-16.7997,-80.5441,-10.5935,24.9694,89.8384,9.1119,-10.7443,-27.8558,-12.5806,7.593,74.8127,68.4959,-53.4293,78.8544,-68.5957,63.7432,31.347,-37.5016,33.8929,-88.8045,-78.7719,-66.4944,44.1972,18.3836,26.5212,84.4723,39.1769,-61.4863,-25.6038,-81.1829,58.6958,-30.8386,-72.6725,89.9257,-15.1934,-4.3337,5.343,10.5603,-77.7268,52.0859,40.3944,88.3328,-55.8306,1.3181,36.025,-69.9271]) # opt for 50D

    # x = np.zeros(nreal, dtype)

    result = f6(np.matrix([78,-49]))
    #result = f1(np.matrix([[0,0]]))
    print 'result: ', result

    # print 'result:', f1(x)
    # print 'result (should be ~ 3055):', f2([0,0])

    sys.exit()

