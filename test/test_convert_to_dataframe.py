from src.convert_to_dataframe import convert_json_to_dataframe
import pandas as pd


data = {
  "Duration":{
    "0":60,
    "1":60,
    "2":60,
    "3":45,
    "4":45,
    "5":60
  },
  "Pulse":{
    "0":110,
    "1":117,
    "2":103,
    "3":109,
    "4":117,
    "5":102
  },
  "Maxpulse":{
    "0":130,
    "1":145,
    "2":135,
    "3":175,
    "4":148,
    "5":127
  },
  "Calories":{
    "0":409,
    "1":479,
    "2":340,
    "3":282,
    "4":406,
    "5":300
  }
}
def xtest_data_type_converted_json():
    dataframe = convert_json_to_dataframe(data)
    assert type(dataframe) == pd.core.frame.DataFrame

def test_multiple_json():
    datadict = {"data1" : data, "data2" : data}
    dataframe = convert_json_to_dataframe(datadict)
    assert type(dataframe["data1"]) == pd.core.frame.DataFrame
    assert type(dataframe["data2"]) == pd.core.frame.DataFrame