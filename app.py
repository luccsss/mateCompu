from flask import Flask, render_template, request, send_file
import random
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_matrix', methods=['POST'])
def generate_matrix():
    data = request.json
    n = int(data['n'])
    randomize = data['randomize']

    if randomize:
        # Generar matriz aleatoria
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    else:
        # Usar la matriz proporcionada por el usuario
        matrix = data['matrix']

    # Crear el grafo basado en la matriz
    G = nx.Graph()
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] == 1:
                G.add_edge(i, j)

    # Graficar el grafo
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')

    # Guardar la imagen en un buffer
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    # Enviar la imagen como respuesta
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
