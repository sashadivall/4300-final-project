import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Connect to MySQL
def get_data():
    conn = pymysql.connect(
        host='ds4300-project-rds.c50kw8mmmhl2.us-east-2.rds.amazonaws.com',
        user='admin',
        password='DS4300Password',
        database='project_db'
    )
    query = "SELECT * FROM bank_data" 
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App Layout
def main():
    st.title("Your Financial Data Dashboard")

    # Load data from MySQL
    data = get_data()

    # Convert the date column to datetime
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.to_period('M')  
    data['year'] = data['date'].dt.to_period('A')  
    # Group by month and aggregate the balance (sum or average)
    monthly_data = data.groupby('month')['balance'].mean().reset_index()  # Use .mean() for average
    yearly_data = data.groupby('year')['balance'].mean().reset_index()  # Use .mean() for average


    data_cut = data[['balance','withdrawls','deposits']]


    # Display basic statistics (optional)
    st.write("Basic Statistics:")
    st.write(data_cut.describe())

    # --- Two Column Layout Below ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("## Balance through the years")
        st.markdown("Calculated by taking the average balance each year")
        st.metric(label="Latest Balance", value=f"${data['balance'].iloc[-1]:,.0f}")
        st.markdown(" ")
      
        st.markdown("## Balance by Category")
        st.markdown("Balances summed by different categories of spend")


        category_sums = data.groupby('category')['balance'].sum()
        top_category = category_sums.idxmax()
        top_balance = category_sums.max()

        st.write(f"The category with the highest total balance is :green[**{top_category}**] with a total of :green[**${top_balance:,.2f}**]")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.markdown("## Withdrawals vs Deposits through the years")
        st.markdown("Comparing the sums of deposits vs withdrawals per year")




        

    with col2:

        #   Plot balance over time (one point per month)
        st.write("Balance Over Time (Yearly):")
        plt.figure(figsize=(10, 6))
        plt.plot(yearly_data['year'].astype(str), yearly_data['balance'], marker='o')
        plt.title('Balance Over Time (Yearly)')
        plt.xlabel('Year')
        plt.ylabel('Balance')
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        plt.tight_layout()

        # Show plot in Streamlit
        st.pyplot(plt)

        balance_by_category = data.groupby('category')['balance'].sum()

        fig, ax = plt.subplots()
        ax.pie(balance_by_category, labels=balance_by_category.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Make it a circle
        st.pyplot(fig)

        # Group by 'year' and sum 'deposit' and 'withdrawal'
        yearly_data2 = data.groupby('year')[['deposits', 'withdrawls']].sum()

     # Plot the stacked bar chart
        yearly_data2.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Withdrawals vs. Deposits per Year')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        plt.legend(title='Transaction Type')
        plt.tight_layout()
        st.pyplot(plt)


        


if __name__ == "__main__":
    main()
