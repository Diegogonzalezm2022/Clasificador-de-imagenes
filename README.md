# Clasificador de imagenes

En este proyecto se quiere crear una red neuronal que pueda, dado un conjunto de imágenes, identificar cada una en una categoría entre varias dadas.

## Conjunto de datos

Para entrenar la red neuronal del clasificador de imagenes se ha escogido el conjunto de datos Skin Disease Dataset (https://www.kaggle.com/datasets/pacificrm/skindiseasedataset?resource=download ), que recoge múltiples imágenes de 22 enfermedades dermatológicas. Este dataset esta dividido en dos conjuntos de imágenes (test y train), frente a los tres necesarios para el desarrollo del clasificador, por lo que se elabora un script auxiliar para extraer varias imágenes del conjunto de entrenamiento para obtener un conjunto de validación (El script auxiliar se incluye en el repositorio, incluyendo las instrucciones necesarias para ejecutarlo y obtener un conjento de imagenes igual al usado durante la creación del proyecto). Para una mayor simplicidad en el entrenamiento de la red, se escoge un subconjunto de 10 de las enfermedades recogidas, de manera que se define la estructura de la red sobre el subconjunto y posteriormente se aplica sobre el conjunto completo.

Para cargar los datos en la red neuronal se crea una clase que hereda del Dataset de Pytorch (SkinDiseaseDataset), de manera que se pueden usar los dataloaders de Pytorch a pesar de que la estructura de los directorios sea diferente a la estándar. La implementación de la clase se incluye en el jupyter notebook.

## Entrenamiento y evaluación

Para el entrenamiento y evaluación de las redes neuronales, se definen un conjunto de funciones desarrolladas para entrenar y evaluar los modelos desarrollados, incluyéndose la creación de gráficos para mostrar el proceso de entrenamiento y los resultados de la evaluación de la red (matriz de confusión), de tal manera que el desarrollo de los distintos experimentos se simplifica a crear la red y definir los parámetros de entrenamiento. Este conjunto de funciones se incluye en el jupyter notebook, en el apartado de mismo nombre que este.

## Redes creadas

En los siguientes apartados se describen las distintas redes creadas y se muestra sus resultados sobre el conjunto de datos. Para unos resultados más detallados consultar el jupyter notebook.

### Experimento 1: Red simple

En primer lugar, se crea una red no convolutiva para servir de base para los futuros experimentos y tener una estimación inicial de los resultados de esperables. Esta red está formada por 4 capas, de un tamaño 8192-2048-512-10, usando la función sigmoide como función de activación
Tras entrenar la red durante cinco epocas, obtenemos un 13.04% de ratio de acierto, lo cuál es ligeramente mejor que una respuesta aleatoria (que oscilaría en el 10%). Sin embargo observando la matriza de confusión (consultar notebook) observamos que la red solo da una única respuesta para todas las imágenes, por lo que falla en la labor de identificación. Esto muestra la necesidad de utilizar una red convolutiva.

### Experimento 2: Red convolutiva

Se añade una capa convolutiva y una capa de pooling al modelo para así mejorar la identificación de las imágenes. Estas capas se añaden al principio de la red, antes de la capa no convolutiva.
Se obtiene un ratio de un 5.41%, peor que la no convolutiva y que responder aleatoriamente. Se sigue observando el mismo patrón de respuesta que en la red anterior.

### Experimento 3: Función tangente

Para intentar corregir el comportamiento de la red (escoger y esperar que la respuesta sea correcta) se sustituya la función de activación por la función tangente. De esta manera, la activación de las neuronas afecta en mayor medida al resultado y por tanto aumentando el resultado de la función de perdida, de tal manera que intentar responder siempre lo mismo no sea una estrategia viable.

Se obtiene un ratio de acierto de un 10.33%, que aún sigue siendo peor que la red no convolutiva, pero observando la matriz de confusión observamos que se corrige en cierta medida el patrón de respuestas (se pasa de una respuesta a dos).

### Experimento 4: Eliminación del pooling

Para mejorar el porcentaje de acierto de la red, se elimina el pooling para obtener un mayor detalle en la salida de la capa convolutiva. Sin embargo, para poder evitar ocupar demasiada memoria de gpu es necesario reducir el tamaño de las imágenes, reduciéndose a un cuarto de su estado original.

Por primera vez se consigue superar a la red no convolutiva en el porcentaje de acierto en la evaluación (14.47%). Además, se observa que el conjunto de respuestas es más variado.

### Experimento 5: Dropout

Se añaden capas de dropout, que desactivan un porcentaje de las neurones aleatoriamente, para así evitar la creación de sesgos e incentivizar el uso de todas la neuronas.

Se observa una mejoría en la perdida en los ratios de aciertos (15.90%). En la matriz de confusión vuelven a aparecer dos respuestas principales, pero se observa que se distribuyen más respuestas en otras categorías, por lo que el sesgo hacia unas respuestas frente a otras a disminuido.

### Experimento 6: Ajuste de parámetros

Se ajustan el ratio de aprendizaje, el tamaño del batch y el número de epocas para intentar mejorar el rendimiento de la red creada, que en este caso es la misma que en el experimento anterior.

Se observa una mejoría significativa frente a las redes convolutivas anteriores, siendo la perdida por primer vez menor que la de la red no convolutiva. Se observa un salto significativo en el ratio de acierto (39.59%) y en la matriz de confusión empieza a destacar la diagonal principal(donde aparecen los aciertos). Cabe destacar que se observa una disparidad significativa entre el los resultados del conjunto de entrenamiento y el de evaluación (un 78% de acierto frente a un 39), lo cual se puede achacar a la organización del dataset. Además observando la gráfica de entrenamiento se observa overfitting.

### Experimento 7: Transfer learning

Para intentar obtener una mejor tasa se aplica transfer learning, que consiste en seleccionar una red preentrenada y modificar su capa de salida para utilizarla durante el entrenamiento. La red escogida es regnet_y_128f, con los pesos obtenidos de aplicarse sobre el conjunto de imágenes IMAGENET1K_SWAG_E2E_V1, escogida por ser una de las que tiene un mayor ratio de acierto en clasificación de imagenes en la librería torchvision (https://docs.pytorch.org/vision/main/models.html#classification).

Se observan unos resultados muy similares al anterior experimento, por lo que no se obtienen nuevas conclusiones.

### Experimento 8

En este experimento se aplican las redes creadas anteriormente sobre el dataset de 22 clases para observar su rendimiento.

Se observa un ligero empeoramiento en ambas redes, esperable debido al aumento del tamaño del problema, además de una ligera ventaja de la red de transfer learning sobre la creada.

### Experimento 9: Reorganización de los datos

Para intentar solucionar el overfitting presente en los modelos anteriores, se reorganiza el dataset para reducir las diferencias que existan entre los distintos conjuntos de dato (train, test y validation). El script ejecutado para realizar esta reorganización se encuentra en el repositorio del proyecto. Adicionalmente, se aumenta el número de épocas ya que observando las gráficas de perdida y porcentaje de acierto se observa que los resultados sobre el conjunto de entrenamiento aún pueden mejorar.

Se observan resultados mejores a los anteriores (40.13% de acierto en la red cread y 33.5% en la de transfer learning), pero sigue existiendo un overfitting significativo.

### Experimento 10: Data augmentation

Puesto que sigue existiendo un overfitting significativo, se aplican técnicas de data augmentation sobre los datos para aumentar el conjunto y variedad de los datos de entrenamiento. Cabe destacar que las técnicas aplicadas actúan sobre la posición de la imagen (inversión vertical y horizontal), no aplicandose cambios sobre el color de estas. Esto se debe a que el color de la zona afectada puede ser importante para el diagnóstico de una enfermedad dermatológica (un grano blanco y un grano rojo pueden ser síntomas de enfermedades distintas), por lo que modificar los colores de la imagen puede causar que se pierdan detalles importantes para el diagnóstico, empeorando el rendimiento de la red.
Adicionalmente se sustituye la función de activación por la función ReLU para obtener un mayor rendimiento.

Se mejora la tasa de acierto significativamente (43.92% red creada y 36.78% transfer learning). Sin embargo, aún sigue existiendo un overfitting significativo.

## Conclusión

Durante el desarrollo de este proyecto no ha sido posible obtener una red que consiga clasificar las imágenes de forma fiable (lo máximo que se ha obtenido ha sido un 44% en evaluación), observándose un problema de overfitting persistente en los modelos desarrollados. Para poder mejorar el rendimiento del modelo, es necesario eliminar este problema, lo cuál podría conseguirse mediante un data set más amplio o aplicando más técnicas de data augmentation.