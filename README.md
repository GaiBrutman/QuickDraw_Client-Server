# QuickDraw_Client-Server
#### A PyTorch implementation of the Google "Quick, Draw!" experiment , with a Client-Server framework

#### Model and server written in python with [PyTorch](https://pytorch.org). Client written with [Processing](http://processing.org).


## Get started

#### Clone the repository
```
git clone https://github.com/GaiBrutman/QuickDraw_Client-Server.git
```

#### Dataset
The categories file should be a .txt file, with the categories separated by newlines, like this:
```
airplane
ant
apple
axe
banana
```
*The categories do not have to be sorted.

The train, validation and test datasets should be in separated .csv files, looking like this:

| Label    | px_0     | px_1     |...       |px_782    |px_783    |
| -------- |:--------:|:--------:|:--------:|:--------:| --------:|
| 3        | 0        | 124      | ...      | 23       | 255      |
| 9        | 43       | 205      | ...      | 238      | 255      |
| 4        | 123      | 141      | ...      | 66       | 255      |

#### Pretrained Model
A Pretrained model is included in 'models/quickdraw_model55.pth', a matching categories file can be found in 'quick_draw_categories.txt'


#### Training:
Run this command to start simple training, train arguments can be changed (check python -h).

```
python train.py -cp <CATEGORIES_FILE> -tr <TRAIN_DARA_FILE> -vl <VAL_DARA_FILE> -ts <WHERE_TO_SAVE>
```

Continue training with saved model.
```
python train.py -cp <CATEGORIES_FILE> -tr <TRAIN_DARA_FILE> -vl <VAL_DARA_FILE> -ts <WHERE_TO_SAVE> -sm <MODEL_FILE_PATH>
```

#### Testing:

Evaluate the saved model with a test dataset.
```
evaluate.py -cp <CATEGORIES_PATH> -ts <TEST_DARA_FILE> -sm <MODEL_FILE_PATH>
```

Evaluate and show the performance of the model on every class.
```
evaluate.py -cp <CATEGORIES_PATH> -ts <TEST_DARA_FILE> -sm <MODEL_FILE_PATH> -ec
```

#### Server:
Run this command to start the server.

```
server.py -cp <CATEGORIES_PATH> -sm <MODEL_FILE_PATH>
```

#### Client:
You need to have Processing to run the Client.
To run with processing, open 'Client/Client.pde' and press the Run button.

*With Processing, you can export the client application to a folder with an executable


