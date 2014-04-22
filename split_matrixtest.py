import numpy
import numpy.matlib
import scipy.linalg
import scipy.sparse
import sys
import json

#print "starting..."

with open(sys.argv[1], "r") as f:
    #print "loading json data..."
    data = json.load(f)
    
    n = len(data)
    
    #print "%i words..." % n
    
    alpha = 0.85
    
    dt = numpy.dtype(float)
    
    _H = scipy.sparse.dok_matrix((n, n), dtype=dt)
    
    u = numpy.matrix(1.0/n * numpy.ones(n))
    
    #print "mapping words to indices..."
  
    keyMap = {}
    
    for i, headword in enumerate(data):
        keyMap[headword] = i
        keyMap[i] = headword
    
    #print "generating H..."
      
    for i, headword in enumerate(data):
        forward = data[headword]["forward"]
        if forward:
            o = len(forward) # no. of forward links
            for word in forward:
                _H[keyMap[headword], keyMap[word]] = 1.0/o
                
    H = _H.tocsr()
    
    #print "generating Acol..."
    
    _A = scipy.sparse.dok_matrix((n, 1))
    
    for headword in data:
        forward = data[headword]["forward"]
        if not forward:
            _A[keyMap[headword], 0] = 1.0/n
            
    Acol = _A.tocsr()
    
    #print "generating Ecol..."
    
    Ecol = u.T
    
    epsilon = 0.0000000001
    
    #print "computing r..."
    
    rs = [u]
    k = 1
    while True:
        a = rs[k-1] * alpha * H
        b = alpha * numpy.matrix((rs[k-1] * Acol) * numpy.ones((1, n)))
        c = numpy.matrix((rs[k-1] * (1 - alpha) * Ecol) * numpy.ones((1, n)))
       
        tmp = a + b + c

        rs.append(tmp)
        l1norm = scipy.linalg.norm(rs[k] - rs[k-1], 1)
        #print l1norm, k
        if l1norm < epsilon:
            break
        k += 1

    r = rs[k].tolist() 
    
    #print r
    s = sum(r[0])
    #print "sum: %f" % s
    
    #print "done! (%i iterations)" % k
    
    for i in range(len(r[0])):
        print r[0][i] * 10000, keyMap[i]
    
    sys.exit(0)
