def solve_gmres(A, b, rtol, maxiter):
    x, info = sp.sparse.linalg.gmres(A,b, rtol = rtol, maxiter = maxiter)
    residual_norm = np.linalg.norm(b - A@x)
    return residual_norm

A_data = np.array([[9, 1, 7, 9], 
                   [5, 2, 4, 4], 
                   [8, 4, 2, 1], 
                   [2, 5, 1, 5]])
b_data = np.array([9, 4, 7, 6])
RTOL = 1e-10
MAX_ITER = 10

norma_residuum = solve_gmres(A_data, b_data, RTOL, MAX_ITER)
print(f"{norma_residuum:.20f}")

A =[[5, 0, 2 ,2], [7, 1 ,6 ,9],[1, 9 ,1 ,0], [1, 8, 3 ,3], [3, 0, 9 ,6], [0, 4 ,6 ,0]]
b = [7,0,0,7,7,9]

Q, R = sp.linalg.qr(A, mode = 'economic')
c = Q.T@b

x = sp.linalg.solve_triangular(R, c)

print(x[2])

A = np.array([[0, 0, 9, 7], 
                   [4, 7, 2, 8], 
                   [3, 6, 5, 4], 
                   [1, 3, 3, 1]])

a, s, b = np.linalg.svd(A)

print(min(s))
