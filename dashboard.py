import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

####################################### HEADER ###############################
st.header('BIKE SHARE DASHBOARD :bicyclist:')

######################################load dataset###########################
day_df = pd.read_csv('./dataset/day.csv')
hour_df = pd.read_csv('./dataset/hour.csv')



########################## MENGURUTKAN DATAFRAME SESUAI DENGAN DTEDAY #######################
# datetime_columns = ['dteday']
# day_df.sort_values(by='dteday', inplace=True)
# day_df.reset_index(inplace=True)
# hour_df.sort_values(by='dteday', inplace=True)
# hour_df.reset_index(inplace=True)

# for column in datetime_columns:
#     day_df[column] = pd.to_datetime(day_df[column])
#     hour_df[column] = pd.to_datetime(hour_df[column])


################### MEMBUAT KOMPONEN FILTER ##########################################
# min_date = hour_df['dteday'].min()
# max_date = hour_df['dteday'].max()

# with st.sidebar:
#     # ambil start date dan end date dari date input
#     start_date, end_date = st.date_input(
#         label= 'Rentang Waktu', min_value=min_date,
#         max_value=max_date,
#         value=[min_date, max_date]
#     )

################################## BAGIAN 1 #########################################
st.subheader('Jumlah Pesepeda Tahun 2011 - 2012')

col1, col2, col3 = st.columns(3)

with col1:
    total_pesepeda = day_df['cnt'].sum()
    st.metric('Total Pesepeda', value=total_pesepeda)

with col2:
    total_registered = day_df['registered'].sum()
    st.metric('Total Pesepeda Registered', value=total_registered)

with col3:
    total_casual = day_df['casual'].sum()
    st.metric('Total Pesepeda Casual', value=total_casual)

#################################### PIE CHART ###########################################
rc_df = (hour_df['casual'].sum(), hour_df['registered'].sum())
nama_rc = ('casual', 'registered')
fig, ax = plt.subplots()
plt.title('Persebaran Pesepeda Casual dan Registered')
ax.pie(
    rc_df, 
    labels=nama_rc,
    autopct='%1.2f%%', #menampilkan persentase dengan 2 desimal
    colors=['#ff9999', '#66b3ff'], # waarna tiap kategori
    explode=(0.1, 0), 
    shadow=True,# menambahkan bayangan
    startangle=100 #sudut awal pie chart
)

plt.show()
st.pyplot(fig)

################################## MUSIM DAN CUACA YANG PALING DISUKAI ###################################
st.subheader('Musim dan Cuaca yang paling disukai')
col1, col2 = st.columns(2)
season_mapping = { 1 : 'Musim Semi',
                  2 : 'Musim Panas',
                  3 : 'Musim Gugur',
                  4 : 'Musim Salju'}
day_df['season'] = day_df['season'].map(season_mapping)

with col1:
    fig, ax = plt.subplots()
    fav_season = day_df.groupby(by='season')['cnt'].sum()
    ax = sns.barplot(x=fav_season.index, y = fav_season.values)

    #tambah label ditiap bar
    for idx, value in enumerate(fav_season.values):
        plt.text(x=idx,y=value, s=f'{value}', ha='center')

    plt.xlabel('Musim')
    plt.ylabel('Jumlah pesepeda')
    plt.title('Jumlah Pesepeda ditiap musim')
    plt.show()
    st.pyplot(fig)

weathersit_dict = {1 : 'Cerah',
                    2 : 'Berkabut',
                    3 : 'Hujan/Salju Ringan',
                    4 : 'Hujan/Salju Lebat'\
                        }
hour_df['weathersit'] = hour_df['weathersit'].map(weathersit_dict)

with col2:
    
    fig, ax = plt.subplots()
    fav_weather = hour_df.groupby(by='weathersit')['cnt'].sum().sort_values(ascending=False)
    x = fav_weather.index
    y = fav_weather.values

    ax = sns.barplot(x=x,y=y)
    for index, value in enumerate(y):
        plt.text(x = index, y = value, s=f'{value}', ha='center')
    plt.xticks(rotation=10) 
    plt.xlabel('Cuaca')
    plt.ylabel('Jumlah Pesepeda')
    plt.title('Persebaran Pesepeda Berdasarkan Cuaca')  
    plt.show()
    st.pyplot(fig)


############################### JAM DAN HARI YANG PALING BANYAK PESEPEDA ########################
st.subheader('Jam dan Hari yang disukai pesepeda')
col1, col2 = st.columns(2)

with col1 :
    fig, ax = plt.subplots()
    bike_hour = hour_df.groupby(by='hr')['cnt'].sum()
    x = bike_hour.index
    y = bike_hour.values
    plt.grid(True)
    plt.plot(x,y)
    plt.xticks(range(0,24))
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Pesepeda')
    plt.title('Persebaran Pesepeda Tiap Jam')
    plt.show()
    st.pyplot(fig)

weekday_dict = {
    0 : 'Minggu',
    1 : 'Senin',
    2 : 'Selasa',
    3 : 'Rabu',
    4 : 'Kamis',
    5 : 'Jumat',
    6 : 'Sabtu'
}
# hour_df['weathersit'] = hour_df['weathersit'].map(season_mapping)
day_df['weekday'] = day_df['weekday'].map(weekday_dict)

with col2 :
    fig, ax = plt.subplots()
    fav_day = day_df.groupby(by='weekday')['cnt'].sum().sort_values(ascending=False)
    x = fav_day.index
    y = fav_day.values

    ax = sns.barplot(x=x,y=y)
    for index, value in enumerate(y):
        plt.text(x = index, y = value, s=f'{value}', ha='center')

    plt.xlabel('Hari')
    plt.ylabel('Jumlah Pesepeda')
    plt.title('Persebaran Pesepeda Berdasarkan Hari')  
    plt.show()
    st.pyplot(fig)







