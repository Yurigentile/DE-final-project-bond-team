from transform_table_location_id import transform_location
import pandas as pd

def test_transform_table_location_id():
    input_address_df = pd.DataFrame([
            {
                "address_id": 1,
                "address_line_1": "34177 Upton Track",
                "address_line_2": "Tremaine Circles",
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962"
            },
            {
                "address_id": 2,
                "address_line_1": "75653 Ernestine Ways",
                "address_line_2": None,
                "district": "Buckinghamshire ",
                "city": "North Deshaun",
                "postal_code": "02813",
                "country": "Faroe Islands",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962"
            },
            {
                "address_id": 100,
                "address_line_1": "Nobody references this address in counterparty",
                "address_line_2": "Absolutely",
                "district": "Nowhere",
                "city": "Gone",
                "postal_code": "00000",
                "country": "Unknown",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962"
            }
        ])
    expected_df =pd.DataFrame([{
                "location_id": 1,
                "address_line_1": "34177 Upton Track",
                "address_line_2": "Tremaine Circles",
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                
            },
            {
                "location_id": 2,
                "address_line_1": "75653 Ernestine Ways",
                "address_line_2": None,
                "district": "Buckinghamshire ",
                "city": "North Deshaun",
                "postal_code": "02813",
                "country": "Faroe Islands",
                "phone": "1373 796260",
               
            },
            {
                "location_id": 100,
                "address_line_1": "Nobody references this address in counterparty",
                "address_line_2": "Absolutely",
                "district": "Nowhere",
                "city": "Gone",
                "postal_code": "00000",
                "country": "Unknown",
                "phone": "1373 796260",
              
            }
        ])
    

    transformed_df = transform_location(input_address_df)
    pd.testing.assert_frame_equal(transformed_df,expected_df)