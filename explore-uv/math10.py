import numpy as np

b1 = np.array([[-3], [-3], [-4]])
a1 = np.array([[-8], [ 8], [ 5]])
#lala
def vector_projection(b, a):
    """
    Calcula la proyección de b sobre a, el error y la longitud del error.
    También calcula el escalar x donde p = x * a y la matriz de proyección P.
    :param b: Vector a proyectar (numpy array)
    :param a: Vector base (numpy array)
    :return: proyección, error, longitud del error, escalar x, matriz de proyección P
    """
    a_dot_a = np.dot(a.T, a)  # Producto punto de a consigo mismo
    if a_dot_a == 0:
        raise ValueError("El vector base a no puede ser el vector cero.")
    
    x = np.dot(a.T, b) / a_dot_a  # Escalar x
    projection = x * a  # Proyección de b sobre a
    error = b - projection  # Error
    error_length = np.linalg.norm(error)  # Longitud del error
    P = np.dot(a, a.T) / a_dot_a  # Matriz de proyección
    
    return projection, error, error_length, x, P
def least(a,b):
    return a.T @ a, a.T @ b