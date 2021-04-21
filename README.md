## GPW Stocks scraping, analysis and Avellaneda Stoikov Microstructure
## Introduction

In this experiment, we will try to download the data from GPW stock exchange using Python, do a preliminary data analysis of 11 Bit Studios and CD Projekt Red SA.

This experiment has 5 main steps:
  1. Webscrap the data.
  2. Clean and analyze the stocks prices.
  3. Try to predict the prices.
  4. Test the predictions with Avellaneda Toikov model.

`webscraping` directory contains the webscraper connected to GPW. 

`microstructure` directory contains the [Avellaneda Stoikov](https://www.researchgate.net/publication/24086205_High_Frequency_Trading_in_a_Limit_Order_Book) model.

`eda_olhd.ipynb` contains analysis of 11 Bit Studios and Cd Projekt Red SA.
## Steps
1. To download the data you have to run `bot.ipynb` in `webscraping` directory.
2. You can run the Avellaneda Stoikov model `ohf_microstructure_df_ver.py`, by changing  `data = pd.read_csv(<data_directory>, sep=';')` variable.
## Building the model
I've used LSTM Neural Network
```
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

optimizer='nadam', loss='mean_squared_error'
```
I've tested some gradient optimizations like Adam, Nadam and RMSprop Using Adam model was overfitting the data RMSE == 83,3 predictions was really bad. Nadam and RMSprop are almost identical, but Nadam is slighty better in this case.

For more detail please open `eda_olhd.ipynb`
## Result Analysis
The predictions from the model wasn't good, the 
```
Root Mean Square Error = 34.046665
```
I've tested the real and predicted stocks prices of CD Projekt Red from last 100 days with Avellaneda Toikov model.
## Real Stock Prices
![](/images/CDR_micro_real_data_inv.png)
![](/images/CDR_micro_real_data.png)
## Predicted Stock Prices
![](/images/CDR_micro_predicted_inventory.png)
![](/images/CDR_micro_predicted.png)

We can see that in both cases, model turned out to be a plus from the action. The returns on predicted stocks are higher, but that becouse the predicted prices was much higher then the real one, at the start.
![](/real_pred_price.png)
## Next Steps
The next steps of this experiment:
1. Try to make better model for predictions
2. Analyze more companys
3. Try to predict future stocks prices, test them on Avellaneda Toikov model and check it with reallity
