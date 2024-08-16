import streamlit as st
from datetime import datetime
import pandas as pd

class input_field:
    def __init__(self):
        # st.session_state を使って支出や収入を保持する
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'spending_input' not in st.session_state:
            st.session_state.spending_input = 0.0

    def get_goal(self):
        """貯金目標額を設定する関数"""
        self.goal = st.number_input("貯金目標額を入力してください:", min_value=0.0, format="%f")

    def get_income(self):
        """収入を追加する関数"""
        income = st.number_input("収入を入力してください:", min_value=0.0, format="%f", key="income_input")
        if st.button("収入を追加"):
            # 収入をタプルで保持 (日付, 金額, ジャンル)
            st.session_state.transactions.append((datetime.today(), income, "Income"))
            self.save_to_csv()  # 収入が追加されたらCSVに自動保存
            st.success(f"¥{income} の収入が追加されました。")

    def add_spending(self):
        """支出を追加する関数"""
        # 日付の入力
        date = st.date_input("日付を入力してください:", value=datetime.today())
        
        # 支出ジャンルの選択
        genre = st.selectbox("ジャンルを選択してください:", ["Food", "Insurance", "Transport", "Utility Bills", "Shopping", "Entertainment", "Rent", "Wifi", "Phone Bills", "Other"])
        
        # 支出金額の入力
        expense = st.number_input("使ったお金を入力してください:", min_value=0.0, format="%f", key="spending_input")
        
        if st.button("支出を追加"):
            # 支出の詳細をタプルで保持 (日付, 金額 (負の数), ジャンル)
            st.session_state.transactions.append((date, -expense, genre))
            self.save_to_csv()  # 支出が追加されたらCSVに自動保存
            st.success(f"¥{expense} の支出が追加されました。")
            # フィールドリセット
            st.session_state.spending_input = 0.0

    def save_to_csv(self):
        """集めたデータをCSVファイルに保存する関数"""
        df = pd.DataFrame(st.session_state.transactions, columns=["Date", "Amount", "Genre"])
        df.to_csv("transactions.csv", index=False)
        st.success("データがCSVファイルに保存されました。")

# インスタンスを作成
infi = input_field()

st.title("MoneyApp")

# 貯金目標の設定
infi.get_goal()

# 収入の追加
st.header("収入の入力")
infi.get_income()

# 支出の追加
st.header("支出の入力")
infi.add_spending()

# 入力された内容を表示
st.write("収入・支出:")
st.write(st.session_state.transactions)
