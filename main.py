from rich_table.rich_table import richTable
import streamlit as st
import pandas as pd
df = pd.DataFrame(
    [
        {"index": 0, "Item": "A", "rating": 4, "sold": True},
        {"index": 1, "Item": "B", "rating": 5, "sold": False},
        {"index": 2, "Item": "C", "rating": 3, "sold": True},
    ]
)



if __name__ == "__main__":
    st.subheader("Sample Data")
    st.dataframe(df)
    st.subheader("Add group header")
    header_conf = {'group1':  # Group header's name.
                   [{'field': 'Item',  # Column name for input dataframe.
                     # Column name shows in the table.
                     'headerName': 'Item Name'
                     },
                    {'field': 'rating',  # Column name for input dataframe.
                       # Column name shows in the table.
                       'headerName': 'rating Score'
                     }]}
    rt = richTable(df, header_conf=header_conf)
    rt.show()

    st.subheader("Pin colmuns")
    header_conf = {'group1':  # Group header's name.
                   [{'field': 'Item',  # Column name for input dataframe.
                    # Column name shows in the table.
                     'headerName': 'Item Name'
                     },
                    {'field': 'rating',  # Column name for input dataframe.
                     # Column name shows in the table.
                     'headerName': 'rating Score',
                     }]}
    rt = richTable(df, header_conf=header_conf, pinned_cols=['index'])
    rt.show()


    st.subheader("Format number colmun")
    header_conf = {'group1':  # Group header's name.
                [{'field': 'Item',  # Column name for input dataframe.
                    # Column name shows in the table.
                    'headerName': 'Item Name'
                    },
                    {'field': 'rating',  # Column name for input dataframe.
                    # Column name shows in the table.
                    'headerName': 'rating Score',
                    'formatter': '￥'
                    }]}
    rt = richTable(df, header_conf=header_conf)
    rt.show()




st.subheader("Cell font styling")
header_conf = {'group1':  # Group header's name.
               [{'field': 'Item',  # Column name for input dataframe.
                 # Column name shows in the table.
                 'headerName': 'Item Name'
                 },
                {'field': 'rating',  # Column name for input dataframe.
                   # Column name shows in the table.
                 'headerName': 'rating Score',
                 'formatter': '￥'
                 }]}
rt = richTable(df, header_conf=header_conf,
               backgroundColor='red',
               fontWeight='bold',
               color='white',
               pinned_cols=['index'])
rt.show()

st.subheader("background's Color grade ")
header_conf = {'group1':  # Group header's name.
               [{'field': 'Item',  # Column name for input dataframe.
                 # Column name shows in the table.
                 'headerName': 'Item Name'
                 },
                {'field': 'rating',  # Column name for input dataframe.
                   # Column name shows in the table.
                 'headerName': 'rating Score',
                 'formatter': '￥'
                 }]}
rt = richTable(df, header_conf=header_conf, pinned_cols=['index'])
rt.show(with_color=True)
