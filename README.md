# API de identificação de áreas construídas em imagens JPG

![Bridge on forest](https://images.unsplash.com/photo-1562939568-91cdb83881ca?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&h=300&q=80)

## Caracterização do problema
- Problemas climáticos;
- Maior devastação na Amazônia nos últimos X anos;
- Falta de recursos humanos e tecnológicos para fiscalização de auto-declaração de posse;
- Atraso em processos relacionados com auto-declaração de posse;

## Objetivo
- Criar uma API que dado uma imagem, retorna a porcentagem da mesma com construções.

## Setup on Windows with Anaconda Python 3.7
```bash
git clone https://github.com/matterport/Mask_RCNN.git
cd Mask_RCNN
conda create -n tf tensorflow
conda activate tf
conda install -c conda-forge numpy
conda install -c conda-forge scipy
conda install -c conda-forge Pillow
conda install -c conda-forge cython
conda install -c conda-forge matplotlib
conda install -c conda-forge scikit-image
conda install -c conda-forge keras
conda install -c conda-forge opencv-python
conda install -c conda-forge h5py
conda install -c conda-forge imgaug
conda install -c anaconda ipython
pip search pycocotools
pip install pycocotools-windows
tf_upgrade_v2 --infile mrcnn/model.py --outfile mrcnn/model-edited.py
```

A última linha faz a atualização do código de `model.py`. Após atualização, caso seja bem sucedida, apague `model.py` e renomeie `model-edited.py` para `model.py` garantindo que a versão do <i>tensorflow<i> instalada no ambiente virtual seja compatível.

## Metodologia

- Usaremos Mask-RCNN com pesos pré-treinados. O mais famoso conjunto de pesos pré-treinados para esse modelo é o MS COCO. 
- Para implementar Mask-RCNN seguindo o repositório do Matterport temos que realizar os seguintes passos:
    - Adquirir os dados
    - Criar as máscaras
    - Criar uma classe para carregamento das configurações para treinamento
    - Criar uma classe para carregamento das informações do conjunto de dados, por exemplo, imagens, labels, classes, máscaras, ...
    - Treinar o modelo
    - Validar o modelo
    - Criar API backend (flask)
    - Deploy API backend no Pythonanywhere
    - Criar exemplo simples de frontend (node-express com nunjucks)
    - Deploy exemplo simples de frontend no Heroku

## Possíveis aquisições de dados
- Imagens de satélite ([Nasa](https://api.nasa.gov/) e [Landsat](https://www.usgs.gov/land-resources/nli/landsat/landsat-data-access?qt-science_support_page_related_con=0#qt-science_support_page_related_con))
- [Planet: Understanding the Amazon from Space Challenge dataset](https://www.kaggle.com/c/planet-understanding-the-amazon-from-space)
- [Google Earth](https://www.google.com.br/intl/pt-BR/earth/)
- [Spacenet dataset](https://spacenetchallenge.github.io/datasets/datasetHomePage.html)

## Dificuldades encontradas na aquisição de dados
- Imagens de baixa qualidade
- Criação manual de máscaras
- Limitação no número de requisões para API gratuita
- Extração manual (não fornece API)

Devido às limitações acima, escolheu-se o [Spacenet dataset](https://spacenetchallenge.github.io/datasets/datasetHomePage.html). Este contém imagens de alta qualidade já com máscaras. São 3401 imagens e o download é simples. Além disso é opensource.

## Aquisição de dados
Após instalar o CLI da AWS, digite:

```bash
aws s3 cp s3://spacenet-dataset/spacenet/SN6buildings/tarballs/SN6buildingsAOI11Rotterdamtrain.tar.gz .
```

São aproximadamente 40 Gbs de dados compactados. São aproximadamente 24 horas para download e descompactação dos dados. Devido a quantidade de imagens e limitação da minha máquina i7 8gb sem GPU, dados foram transferidos para o Google Drive na intenção de fazer treinamentos no Google Colab. O tempo para upload dos dados foi de 4 dias inteiros.

## Exploração dos dados
- São 3401 imagens de satélites tiradas sobre Rotterdan. As imagens estão em formato .tif
- Há 3401 arquivos .geojson se referindo à construções nas imagens
- Exemplos das imagens originais estão na pasta `spacenet/TIF-RGB`
- Exemplos dos arquivos geojson originais estão na pasta `spacenet/GEOJSON`
![](/assets/mask-example.png)
- As imagens da pasta `spacenet/TIF-RGB` são 900x900x3, enquanto suas máscaras são 900x900x4.
- O notebook de exploração do dataset é `spacenet_eda.ipynb`. 

## Pré-processamento
- As imagens possuem dimensões grandes para treinamento. Como utilizaremos pesos pré-treinados, um número menor de imagens é suficiente para obter resultados expressivos. Por exemplo, considerando o dataset Ballon, apenas 62 imagens são suficientes para obter-se uma boa acurácia considerando os pesos pré-treinados MS COCO.
- As imagens da pasta <i>spacenet/TIF-RGB</i> em formato .tif foram convertidas para .png e colocadas na pasta <i>spacenet/PNG-RGB</i>. O código para conversão é `tif2png.py`.
- As conversões facilitam a implementação do método <i>load_image</i> da classe <i>Dataset</i>.

## Balanceamento de classes
- No caso de conjuntos de imagens, cada padrão se comporta como se fosse uma classe. Por exemplo, se tiverem muitas construções retangulares e muito poucas redondas, o modelo pode não identificar assertivamente construções redondas. Por isso em treinamentos com imagens são necessárias várias. O conjunto de pesos considerado (MS COCO) foi treinado com 330 mil imagens. Mais informações sobre este conjunto podem ser encontradas [aqui](https://cocodataset.org/#home). 

## Criação das máscaras 
- Os arquivos da pasta <i>spacenet/GEOJSON</i> em formato .geojson foram convertidas para .png e colocadas na pasta <i>spacenet/PNG-MASK</i>. O código para conversão é `geojson2png.py` e foi obtido do repositório do [Mstfakts](https://github.com/Mstfakts/Building-Detection-MaskRCNN). Como depende da biblioteca <i>geoio</i> o processo foi feito pelo Google Colab.
- As conversões facilitam a implementação do método <i>load_image</i> da classe <i>Dataset</i>.

## Criação da classe Config
***##TODO***

## Criação da classe Dataset
***##TODO***
## Treinamento
***##TODO***

## Validação

- AP (Average precision) é a métrica mais popular para medir acurácia quando lidamos com modelos de detecção de objetos como Faster R-CNN, SSD, etc.
- precision = true positive / (true positive + false positive)
- recall = true positive /  (true positive + false negative)
- F1 = precision * recall / ( precision + recall )
- Ver Fonte: https://medium.com/@jonathan_hui/map-mean-average-precision-for-object-detection-45c121a31173

## Backend em Python Flask
***##TODO***

## Deploy no backend no PythonAnywhere
***##TODO***

## Exemplo simples de Frontend em Express-Nunjucks
***##TODO***

## Deploy no frontend no Heroku
***##TODO***

## Agradecimentos
- Obrigado <a href="https://unsplash.com/@serjosoza?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">sergio souza</a> por compartilhar seu trabalho no <a href="https://unsplash.com/s/photos/amazon-rainforest?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>
- Obrigado ao professor Eder Balbino pelo material didático que orientou o trabalho.
- Obrigado ao [Mstfakts](https://github.com/Mstfakts/Building-Detection-MaskRCNN) por compartilhar seu código.
- Obrigado à [Matterport](https://github.com/matterport/Mask_RCNN) por criar e compartilhar o modelo de MaskRCNN de maneira tão simples e elegante.

## Referências
- https://www.analyticsvidhya.com/blog/2019/07/computer-vision-implementing-mask-r-cnn-image-segmentation/
- 
- SpaceNet on Amazon Web Services (AWS). “Datasets.” The SpaceNet Catalog.  Last modified April 30, 2018.
Accessed on 06/07/2020. https://spacenetchallenge.github.io/datasets/datasetHomePage.html.