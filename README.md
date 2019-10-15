# Fotossíntese

Implementação de um Photoshop para a cadeira de Processamento Digital de Imagens (PDI) na UFC.

### Depedências

`$ pip3 install -r requirements.txt`  
`$ sudo apt-get install python3-tk` 

### Exec

`$ python3 front.py`

### Filtros implementados

- Negativo
- Logarítmico
- Correção de gamma
- Picewise
- Equalização de histograma
- Média aritmética
- Média geométrica
- Média harmônica
- Média contraharmônica
- Gaussiano
- Mediana
- Convolução
- Laplaciano
- Sobel
- Sepia
- Chroma-Key
- Sharpen
- Highboost
- Passa alta
- Passa baixa
- Passa faixa

### Conversões implementadas

- RGB - > grayscale utilizando média ponderada
- RGB - > grayscale utilizando média simples
- RGB < - > HSV

### Transformações espaciais

- Interpolação pelo vizinho mais próximo (nearest neighbor)
	- Escala (Grayscale Image)
	
- Interpolação bilinear
	- Escala (RGB e Grayscale Image)
	- Rotação (RGB e Grayscale Image)

### Outros

- Histograma
- Espectro de Fourier